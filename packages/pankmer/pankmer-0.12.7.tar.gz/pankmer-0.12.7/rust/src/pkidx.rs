// Imports =====================================================================
use std::{fs, str, io};
use std::fs::File;
use std::io::{Read, Write};
use std::path::PathBuf;
use niffler;
use pyo3::prelude::*;
use rayon::iter::{IntoParallelRefIterator, ParallelIterator};
use rustc_hash::FxHashMap as HashMap;
use serde::{Serialize, Deserialize};
use crate::{K, Kmer, ScoreList, ScoreToIDX, PKTbl, PKGenomes, IDXMap, MemBlocks};
use crate::helpers::print_err;
use crate::mem_blocks::generate_mem_blocks;
use crate::get_kmers::get_kmers;
use crate::score_list_io::{load_scores_partial, load_scores, dump_scores};
use crate::metadata::PKMeta;

// Constants ===================================================================

const GZIP_LEVELS: [niffler::Level; 10] = [
    niffler::Level::Zero,
    niffler::Level::One,
    niffler::Level::Two,
    niffler::Level::Three,
    niffler::Level::Four,
    niffler::Level::Five,
    niffler::Level::Six,
    niffler::Level::Seven,
    niffler::Level::Eight,
    niffler::Level::Nine
];


// Structs =====================================================================
#[derive(Serialize, Deserialize, Debug)]
pub struct PKIdx {
    pub kmers: PKTbl,
    pub genomes: PKGenomes,
    pub k: usize,
    pub scores: ScoreList,
    pub score_map: ScoreToIDX,
    pub kmer_cutoff: Kmer
}

// Functions ===================================================================
#[pyfunction]
pub fn run_index(genomes_input: &str, genomes: PKGenomes, outdir: &str, fraction: f64,
             gzip_level: usize,
             kmersize: usize, split_memory: u64, split_disk: usize,
             threads: usize, index: &str, input_is_tar: bool) -> PyResult<(PKTbl, MemBlocks)> {
    let tar_file = match input_is_tar {
        true => String::from(genomes_input),
        false => String::from("")
    };
    print_err("Generating subindex scheme");
    let all_core_blocks: MemBlocks = generate_mem_blocks(split_memory, threads as u64)?;
    let n_blocks = all_core_blocks.len();
    let disk_segment_size = n_blocks / split_disk;
    let mut positions_dictionary: PKTbl = HashMap::default();
    for core_blocks in all_core_blocks.chunks(disk_segment_size) {
        print_err("Indexing genomes (segment).");
        let post_dict = index_genomes(core_blocks, &genomes, kmersize,
            fraction, gzip_level, &outdir, threads, index, &tar_file).expect("couldn't index genomes");
        print_err("Finished Indexing (segment).");
        print_err("Concatenating files (segment).");
        let pd = concat_files(post_dict, core_blocks, &outdir, gzip_level)?;
        positions_dictionary.extend(&pd);
        print_err("Finished concatenating (segment).");
    }
    Ok((positions_dictionary, all_core_blocks))
}

fn run_core_cohort(args: (&Vec<Kmer>, &PKGenomes, usize, f64, usize, &str, &str, &str)) -> (String, PKTbl) {
    let (limits, genomes, kmersize, kmer_fraction, gzip_level, outdir, index, tar_file) = args;
    let lower = limits[0];
    let upper = limits[1];
    let kmer_bitsize = (2 * K + 7) / 8;
    let score_bitsize = (genomes.len() + 7) / 8;
    let key = format!("{lower}_{upper}");
    let kmers_post = create_index(genomes, kmersize, kmer_fraction, gzip_level, upper, lower,
        kmer_bitsize, score_bitsize,  &outdir, &tar_file).expect("Failed to run core cohort");
    (key, kmers_post)
}

fn index_genomes(all_core_blocks: &[Vec<u64>], genomes: &PKGenomes, kmersize: usize, kmer_fraction: f64,
                 gzip_level: usize, outdir: &str, threads: usize, index: &str,
                 tar_file: &str) -> PyResult<HashMap<String, PKTbl>> {
    let mut core_block_args: Vec<(&Vec<Kmer>, &PKGenomes, usize, f64, usize, &str, &str, &str)> = Vec::new();
    let rayon_num_threads: usize = rayon::current_num_threads();
    let results = match threads >= rayon_num_threads {
        true => {
            print_err(&format!("{threads} threads requested, using {rayon_num_threads} (entire global thread pool)"));
            for limits in all_core_blocks.iter() {
                core_block_args.push((limits, genomes, kmersize, kmer_fraction, gzip_level, &outdir, &index, &tar_file));
            }
            core_block_args.par_iter().map(|args| run_core_cohort(*args)).collect::<Vec<(String, PKTbl)>>()
        },
        false => {
            print_err(&format!("{threads} threads requested, using {threads} (partial global thread pool)"));
            let mut results: Vec<(String, PKTbl)> = Vec::new();
            let cb_len = all_core_blocks.len();
            for (i, limits) in all_core_blocks.iter().enumerate() {
                core_block_args.push((limits, genomes, kmersize, kmer_fraction, gzip_level, &outdir, &index, &tar_file));
                if (i+1)%threads==0 || (i+1)==cb_len {
                    results.extend(core_block_args.par_iter().map(|args| run_core_cohort(*args)).collect::<Vec<(String, PKTbl)>>());
                    core_block_args.clear();
                }
            }
            results
        }
    };
    let mut post_dict: HashMap<String, PKTbl> = HashMap::default();
    for result in results {
        post_dict.insert(result.0, result.1);
    }
    Ok(post_dict)
}

fn concat_files(post_dict: HashMap<String, PKTbl>, all_core_blocks: &[Vec<u64>], outdir: &str, gzip_level: usize) -> PyResult<PKTbl> {
    let mut positions_dict: PKTbl = HashMap::default();
    let mut num: usize = 0;
    let mut scores: ScoreList = match load_scores(outdir, "") {
        Ok(score_list) => score_list,
        Err(_) => ScoreList::new()
    };
    let mut score_to_idx: ScoreToIDX = ScoreToIDX::default();
    for (idx, score) in scores.iter().enumerate() {
        score_to_idx.insert(score.clone(), idx);
    }
    let mut kmers_out_path = PathBuf::from(&outdir);
    kmers_out_path.push("kmers.bgz");
    let mut indices_out_path = PathBuf::from(&outdir);
    indices_out_path.push("indices.bgz");
    let mut kmers_out = match fs::OpenOptions::new().append(true).open(&kmers_out_path) {
        Ok(buf) => buf,
        Err(_) => File::create(&kmers_out_path)?
    };
    // let mut kmers_out = match fs::OpenOptions::new().append(true).open(&kmers_out_path) {
    //     Ok(buf) => niffler::get_writer(Box::new(buf), niffler::compression::Format::Gzip, GZIP_LEVELS[gzip_level]).expect("Can't open file for writing"),
    //     Err(_) => niffler::to_path(&kmers_out_path, niffler::compression::Format::Gzip, GZIP_LEVELS[gzip_level]).expect("Can't open file for writing")
    // };
    let mut indices_out = match fs::OpenOptions::new().append(true).open(&indices_out_path) {
        Ok(buf) => niffler::get_writer(Box::new(buf), niffler::compression::Format::Gzip, GZIP_LEVELS[gzip_level]).expect("Can't open file for writing"),
        Err(_) => niffler::to_path(&indices_out_path, niffler::compression::Format::Gzip, GZIP_LEVELS[gzip_level]).expect("Can't open file for writing")
    };
    let mut scores_out_path = PathBuf::from(outdir);
    scores_out_path.push(format!("scores.pks"));
    let scores_outpath = scores_out_path.into_os_string().into_string().unwrap();
    for limits in all_core_blocks {
        let mut idx_map: IDXMap = IDXMap::default();
        let lower = limits[0];
        let upper = limits[1];
        let key  = format!("{lower}_{upper}");
        let temp_dict = post_dict.get(&key).unwrap();
        let mut sorted_temp: Vec<(&Kmer, &usize)> = temp_dict.iter().collect();
        sorted_temp.sort_unstable();
        for (kmer, cur) in sorted_temp {
            num = cur + num;
            positions_dict.insert(*kmer, num);
        }
        num += 1;
        let scores_partial = load_scores_partial(&outdir, lower, upper);
        for (i, s) in scores_partial.iter().enumerate() {
            match score_to_idx.get(s) {
                Some(x) => { (idx_map.insert(i as u64, *x)); },
                None => {
                    idx_map.insert(i as u64, scores.len());
                    score_to_idx.insert(s.clone().to_vec(), scores.len());
                    scores.push(s.to_vec());
                }
            };
        }

        let mut kmers_in_path: PathBuf = PathBuf::from(&outdir);
        kmers_in_path.push(format!("{lower}_{upper}_kmers.bgz"));
        let mut kmers_in = File::open(&kmers_in_path)?;
        io::copy(&mut kmers_in, &mut kmers_out);
        // let (mut k, _format) = niffler::from_path(&kmers_in_path).expect("File not found");
        // let mut k_vec: Vec<u8> = Vec::new();
        // k.read_to_end(&mut k_vec)?;
        // kmers_out.write_all(&k_vec).unwrap();
        fs::remove_file(&kmers_in_path)?;

        let mut indices_in_path: PathBuf = PathBuf::from(&outdir);
        indices_in_path.push(format!("{lower}_{upper}_indices.bgz"));
        let (mut i, _format) = niffler::from_path(&indices_in_path).expect("File not found");
        let mut i_vec: Vec<u8> = Vec::new();
        i.read_to_end(&mut i_vec)?;
        for i_bytes in i_vec.chunks(8) {
            let idx = u64::from_be_bytes(i_bytes.try_into().unwrap());
            let i_remapped = idx_map.get(&idx).unwrap().to_be_bytes();
            indices_out.write_all(&i_remapped).unwrap();
        }
        fs::remove_file(&indices_in_path)?;
    }
    dump_scores(scores, &scores_outpath).expect("could not write scores.pks");
    Ok(positions_dict)
}

fn create_index(genomes: &PKGenomes, kmersize: usize, kmer_fraction: f64,
                gzip_level: usize,
                upper: Kmer, lower: Kmer, kmer_bitsize: usize,
                score_bitsize: usize, outdir: &str, tar_file: &str) -> PyResult<PKTbl> {
    let idx: PKIdx = get_kmers(kmersize, kmer_fraction, upper, lower,
                                genomes.to_vec(), tar_file);
    let mut scores_out_path = PathBuf::from(outdir);
    scores_out_path.push(format!("{lower}_{upper}_scores.pks"));
    let scores_outpath = scores_out_path.into_os_string().into_string().unwrap();
    let mut kmers_out_path = PathBuf::from(&outdir);
    kmers_out_path.push(format!("{lower}_{upper}_kmers.bgz"));
    let mut indices_out_path = PathBuf::from(&outdir);
    indices_out_path.push(format!("{lower}_{upper}_indices.bgz"));
    let mut kmers_out = niffler::to_path(kmers_out_path, niffler::compression::Format::Gzip, GZIP_LEVELS[gzip_level]).expect("Can't open file for writing");
    let mut indices_out = niffler::to_path(indices_out_path, niffler::compression::Format::Gzip, GZIP_LEVELS[gzip_level]).expect("Can't open file for writing");                     
    let kmers: PKTbl = idx.kmers;
    let kmer_none: bool = kmers.is_empty();
    let mut sorted_kmers: Vec<(Kmer, usize)> = kmers.into_iter().collect();
    sorted_kmers.sort_unstable();
    let kmer_end: Kmer = match kmer_none {
        true => 0,
        false => sorted_kmers[sorted_kmers.len()-1].0
    };
    let mut count: usize = 0;
    let mut kmers_post: PKTbl = HashMap::default();
    for (kmer, i) in sorted_kmers {
        kmers_out.write_all(&kmer.to_be_bytes()[8-kmer_bitsize..]).unwrap();
        indices_out.write_all(&i.to_be_bytes()).unwrap();
        if count%10000000 == 0 && count != 0 {
            kmers_post.insert(kmer, count);
            count = 0;
        }
        count += 1;
    }
    dump_scores(idx.scores, &scores_outpath).expect("could not write scores.pks");
    if !kmer_none && !kmers_post.contains_key(&kmer_end) {
        kmers_post.insert(kmer_end, count-1);
    }
    Ok(kmers_post)
}
