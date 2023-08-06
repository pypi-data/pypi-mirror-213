// Imports =====================================================================
use pyo3::prelude::*;
use bio::io::fasta;
use niffler;
use rayon::iter::{IntoParallelRefIterator, ParallelIterator};
use rustc_hash::FxHashMap as HashMap;
use tar::Archive;
use crate::helpers::{print_err, genome_name};
use crate::PKGenomes;

// Functions ===================================================================

fn measure_genome(f: &str) -> (&str, usize) {
    let (reader, _format) = niffler::from_path(f).expect(&format!("File not found: {}", f));
    print_err(&format!("Measuring {0}.", genome_name(f).expect("Error inferring genome name")));
    let mut size: usize = 0;
    for result in fasta::Reader::new(reader).records() {
        let record = result.expect("Error during fasta record parsing");
        size += record.seq().len();
    }
    (f, size)
}

#[pyfunction]
pub fn measure_genomes(genomes: PKGenomes, tar_file: &str) -> PyResult<HashMap<String, usize>> {
    let mut genome_sizes: HashMap<String, usize> = HashMap::default();
    if tar_file.len() > 0 {
        let (tar, _format) = niffler::from_path(tar_file).expect(
            &format!("File not found: {}", tar_file));
        for f in Archive::new(tar).entries().expect("Can't read tar file") {
            let f = f.expect("Error reading tar archive");
            let genome_path = f.header().path().expect("Error reading tar archive");
            if !((&genome_path).ends_with("fasta")
                 || (&genome_path).ends_with("fa")
                 || (&genome_path).ends_with("fna")
                 || (&genome_path).ends_with("fastq")
                 || (&genome_path).ends_with("fq")
                 || (&genome_path).ends_with("fasta.gz")
                 || (&genome_path).ends_with("fa.gz")
                 || (&genome_path).ends_with("fna.gz")
                 || (&genome_path).ends_with("fastq.gz")
                 || (&genome_path).ends_with("fq.gz")) { continue; }
            let genome_str = format!("{0:?}", &genome_path);
            print_err(&format!("Measuring {0}.", genome_name(&genome_str).expect("Error inferring genome name")));
            let (reader, _format) = niffler::get_reader(Box::new(f)).expect("Can't read from tar archive");
            let mut size: usize = 0;
            for result in fasta::Reader::new(reader).records() {
                let record = result.expect("Error during fasta record parsing");
                size += record.seq().len();
            }
            genome_sizes.insert(genome_str, size);
        }
    } else {
        for (file, size) in genomes.par_iter().map(|f| measure_genome(f)).collect::<Vec<(&str, usize)>>() {
            genome_sizes.insert(file.to_string(), size);
        }
    }
    Ok(genome_sizes)
}
