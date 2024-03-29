# variant_data_viewer/global_variables.py
""" Holds the large lists of global variable lists and dictionaries. """

# VARIABLES -------------------------------------------------------------------

# Data Model Settings ---------------------------------------------------------

VCF_FILE_SETTINGS = {
    "excel_extension": ".xlsx",
    "filename_addon": "(sorted)",
    "IGV_port": 60151,
    "text_output_folder": "texts/",
}

# Controller Settings ---------------------------------------------------------

DISPOSITIONS = [
    "None",
    "Low VAF Variants",
    "VUS",
    "Oncogenic",
    "FLT3 ITDs",
    "Hotspot Exceptions",
]

# View Settings ---------------------------------------------------------------

VALIDATION = {
    "cutoffs": {
        "p_value_max_red": 0.05,
        "p_value_max_green": 0.005,
        "p_value_max_gold": 0.001,
        "vaf_threshold_min_yellow": 0.01,
        "vaf_threshold_min_red": 0.005,
        "locus_read_depth_min_red": 500,
        "strand_read_depth_min_yellow": 10,
        "strand_read_depth_min_red": 2,
        "odds_ratio_min": 0.2,
        "odds_ratio_max": 5.0,
        "bi_prop_min": 0.25,
        "bi_prop_max": 0.75,
        "internal_frequency_yellow": 0.15,
    },
    "p_values": [
        "VCF: Binom P Value",
        "VCF: Fisher P Value",
        "Mpileup Qual: Filtered Variant Binomial P Value",
        "Mpileup Qual: Filtered Variant Fishers P Value",
        "Mpileup Qual: Unfiltered Variant Binomial P Value",
        "Mpileup Qual: Unfiltered Variant Fishers P Value",
        "VCF: STBP",
    ],
    "strand_read_depth": [
        "VCF: FSAF",
        "VCF: FSAR",
        "Mpileup Qual: Filtered Variant Forward Read Depth",
        "Mpileup Qual: Filtered Variant Reverse Read Depth",
        "Mpileup Qual: Unfiltered Variant Forward Read Depth",
        "Mpileup Qual: Unfiltered Variant Reverse Read Depth",
        "Mpileup Qual: Filtered Reference Forward Read Depth",
        "Mpileup Qual: Filtered Reference Reverse Read Depth",
        "Mpileup Qual: Unfiltered Reference Forward Read Depth",
        "Mpileup Qual: Unfiltered Reference Reverse Read Depth",
        "VCF: FAO",
    ],
    "locus_read_depth": [
        "Mpileup Qual: Read Depth",
        "VCF: FDP",
    ],
    "minimum_vaf": [
        "VCF: AF",
        "Mpileup Qual: Filtered VAF",
        "Mpileup Qual: Unfiltered VAF",
    ],
    "web_links": {
        "Variant Annotation: Transcript": "https://useast.ensembl.org/Homo_sapiens/Transcript/Summary?t={}",
        "COSMIC: ID": "https://cancer.sanger.ac.uk/cosmic/search?q={}",
        "ClinVar: ClinVar ID": "https://www.ncbi.nlm.nih.gov/clinvar/variation/{}/",
        "dbSNP: rsID": "https://www.ncbi.nlm.nih.gov/snp/{}",
        "UniProt (GENE): Accession Number": "https://www.uniprot.org/uniprotkb/{}/entry",
        "Variant Annotation: Gene": "",
    },
    "binomial_proportions": [
        "Mpileup Qual: Unfiltered Variant Binomial Proportion",
        "VCF: STB",
        "Mpileup Qual: Filtered Variant Binomial Proportion",
    ],
    "fisher_odds_ratios": [
        "VCF: Fisher Odds Ratio",
        "Mpileup Qual: Filtered Variant Fishers Odds Ratio",
    ],
}

TOOLTIPS = {
    "Disposition": "What to call this variant.",
    "Original Input: Chrom": "Chromosome on which this gene is found.",
    "Original Input: Pos": "Base pair position of the gene on the chromosome.",
    "Original Input: Reference allele": "Expected finding at this base pair \
        location.",
    "Original Input: Alternate allele": "Specimen finding at this base pair \
        location.",
    "Variant Annotation: Gene": "Gene currently selected from the variant list.",
    "Variant Annotation: cDNA change": "Alteration in the DNA at this location.",
    "Variant Annotation: Protein Change": "Resultant alteration in the protein \
        at this location.",
    "Variant Annotation: RefSeq": "",
    "VCF: AF": "Allele fraction of reads with this variant.",
    "VCF: FAO": "Variant read depth at this base pair location, reported by \
        Genexus.",
    "VCF: FDP": "Total read depth at this base pair location, reported by \
        Genexus",
    "VCF: HRUN": "Homopolymer run count, reported by Genexus.",
    "VCF: Filter": "Final filter disposition as given by the Genexus.\n \
        Preferred value: 'PASS'",
    "VCF: Genotype": "Genotype distinction made by the Genexus analyzer.\n \
        1/1 = homozygous, 0/1 = heterozygous, 0/0 = ???, ./. = ???",
    "COSMIC: ID": "COSMIC website ID for this variant.",
    "COSMIC: Variant Count": "Times this variant has been reported to COSMIC.",
    "COSMIC: Variant Count (Tissue)": "JSON-style dictionary breakdown of \
        tissue types \n reported to COSMIC for this variant.",  # Very long text, needs wordwrap
    "ClinVar: ClinVar ID": "ClinVar website ID for this variant.",
    "ClinVar: Clinical Significance": "Clinical significance as reported by \
        ClinVar website.",
    "gnomAD3: Global AF": "Frequency of this variant being found in the human \
        population, as reported by GnomAD website.",
    "PhyloP: Vert Score": "Vertebrate score for gene conservancy, as reported \
        by web resources.",
    "CADD: Phred": "Combine Annotation Dependent Depletion score, rating \
        pathogenicity.\nRange: 0 = Benign, 48 = Pathogenic",
    "PolyPhen-2: HDIV Prediction": "Score assessing the possible change in \
        phenotype of the protein structure, based on AA change.",
    "SIFT: Prediction": "SNP mutagenesis prediction score based on AA change, \
        as reported by SIFT website.",
    "VCF: FSAF": "Forward Variant Read Depth, reported by Genexus\nValid \
        value: > 10",
    "VCF: FSAR": "Reverse Variant Read Depth, reported by Genexus\nValid \
        value: > 10",
    "VCF: FSRF": "Forward Reference Read Depth, reported by Genexus.",
    "VCF: FSRR": "Reverse Reference Read Depth, reported by Genexus.",
    "VCF: Fisher Odds Ratio": "Fisher's odds ratio calculation, based on \
        Genexus read depth data.",
    "VCF: Fisher P Value": "Statistical p-value.\nLess than 0.05 is preferred.",
    "VCF: Binom Proportion": "Binomial proportion caclucation, based on \
        Genexus read depth data.",
    "VCF: Binom P Value": "Statistical p-value.\nLess than 0.05 is preferred.",
    "Mpileup Qual: Read Depth": "Total read depth, as reported by M-Pileup data.\
        \nValid: > 500",
    "Mpileup Qual: Start Reads": "Count of read start signals (strand \
        termination), as reported in the M-Pileup data.",
    "Mpileup Qual: Stop Reads": "Cout of read stop signals (strand initiation), \
        as reported in the M-Pileup data.",
    "Mpileup Qual: Filtered Reference Forward Read Depth": "Forward Reference \
        Read Depth, reported by M-Pileup, @Q20\nValid value: > 10",
    "Mpileup Qual: Filtered Reference Reverse Read Depth": "Reverse Reference \
        Read Depth, reported by M-Pileup, @Q20\nValid value: > 10",
    "Mpileup Qual: Unfiltered Reference Forward Read Depth": "Forward Reference \
        Read Depth, reported by M-Pileup, @Q1\nValid value: > 10",
    "Mpileup Qual: Unfiltered Reference Reverse Read Depth": "Reverse Reference \
        Read Depth, reported by M-Pileup, @Q1\nValid value: > 10",
    "Mpileup Qual: Filtered Variant Forward Read Depth": "Forward Variant Read \
        Depth, reported by M-Pileup, @Q20\nValid value: > 10",
    "Mpileup Qual: Filtered Variant Reverse Read Depth": "Reverse Variant Read \
        Depth, reported by M-Pileup, @Q20\nValid value: > 10",
    "Mpileup Qual: Filtered Variant Binomial Proportion": "Binomial proportion \
        caclucation, based on filtered M-Pileup read depth data.",
    "Mpileup Qual: Filtered Variant Binomial P Value": "Statistical p-value.\
        \n Less than 0.05 is preferred.",
    "Mpileup Qual: Filtered Variant Fishers Odds Ratio": "Fisher's odds ratio \
        calculation, based on filtered M-Pileup read depth data.",
    "Mpileup Qual: Filtered Variant Fishers P Value": "Statistical p-value.\
        \nLess than 0.05 is preferred.",
    "Mpileup Qual: Unfiltered Variant Forward Read Depth": "Forward Variant \
        Read Depth, reported by M-Pileup, @Q1\nValid value: > 10",
    "Mpileup Qual: Unfiltered Variant Reverse Read Depth": "Reverse Variant \
        Read Depth, reported by M-Pileup, @Q1\nValid value: > 10",
    "Mpileup Qual: Unfiltered Variant Binomial Proportion": "Binomial \
        proportion caclucation, based on unfiltered M-Pileup read depth data.",
    "Mpileup Qual: Unfiltered Variant Binomial P Value": "Statistical p-value.\
        \nLess than 0.05 is preferred.",
    "Mpileup Qual: Unfiltered Variant Fishers Odds Ratio": "Fisher's odds ratio \
        calculation, based on unfiltered M-Pileup read depth data.",
    "Mpileup Qual: Unfiltered Variant Fishers P Value": "Statistical p-value.\
        \nLess than 0.05 is preferred.",
    "Mpileup Qual: Filtered VAF": "VAF according to filtered (Q20) mpileup \
        data.",
    "Mpileup Qual: Unfiltered VAF": "VAF according to unfiltered (Q1) mpileup \
        data.",
    "VCF: LEN": "Length of the variant, as reported by Genexus.",
    "VCF: QD": "???",
    "VCF: STB": "Proprietary strand bias calculation, as reported by Genexus.",
    "VCF: STBP": "Statistical p-value.\nLess than 0.05 is preferred.",
    "VCF: SVTYPE": "Unused data field from the Genexus report.",
    "VCF: TYPE": "Type of variant, as reported by Genexus.",
    "VCF: QUAL": "Quality determination tag, as reported by Genexus.",
    "Variant Annotation: Coding": "Reported coding region variant, as reported \
        by Genexus.",
    "Variant Annotation: Sequence Ontology": "Type of variant/mutation \
        encountered.\n Possible Types: MIS, INT, FSI, IND, SYN, SPL ",
    "Variant Annotation: Transcript": "Ensembl transcript designation code.",
    "Variant Annotation: All Mappings": "JSON-style dictionary breakdown of \
        tissue types present in ??? knowledgebase for this variant.",
    "UniProt (GENE): Accession Number": "UniProt web resource for the affected \
        protein and biological functions.",
    "dbSNP: rsID": "ID number for the free dbSNP web resource listing of this \
        variant.",
    "MDL: Sample Count": "Instance count of samples with this variant in ",
    "MDL: Variant Frequency": "",
    "MDL: Sample List": "JSON-style dictionary breakdown of tissue types \
        present in ??? knowledgebase for this variant.",
}

TEXTBOXES = [
    "MDL: Sample List",
    "Variant Annotation: All Mappings",
    "COSMIC: Variant Count (Tissue)",
    "test_tissue",
]

DATA_FIELDS = [
    "Original Input: Chrom",
    "Original Input: Pos",
    "Original Input: Reference allele",
    "Original Input: Alternate allele",
    "Variant Annotation: Gene",
    "Variant Annotation: cDNA change",
    "Variant Annotation: Protein Change",
    "Variant Annotation: RefSeq",
    "VCF: AF",
    "VCF: FAO",
    "VCF: FDP",
    "VCF: HRUN",
    "VCF: Filter",
    "VCF: Genotype",
    "COSMIC: ID",
    "COSMIC: Variant Count",
    "COSMIC: Variant Count (Tissue)",
    "ClinVar: ClinVar ID",
    "ClinVar: Clinical Significance",
    "gnomAD3: Global AF",
    "PhyloP: Vert Score",
    "CADD: Phred",
    "PolyPhen-2: HDIV Prediction",
    "SIFT: Prediction",
    "VCF: FSAF",
    "VCF: FSAR",
    "VCF: FSRF",
    "VCF: FSRR",
    "VCF: Fisher Odds Ratio",
    "VCF: Fisher P Value",
    "VCF: Binom Proportion",
    "VCF: Binom P Value",
    "Mpileup Qual: Read Depth",
    "Mpileup Qual: Start Reads",
    "Mpileup Qual: Stop Reads",
    "Mpileup Qual: Filtered Reference Forward Read Depth",
    "Mpileup Qual: Filtered Reference Reverse Read Depth",
    "Mpileup Qual: Unfiltered Reference Forward Read Depth",
    "Mpileup Qual: Unfiltered Reference Reverse Read Depth",
    "Mpileup Qual: Filtered Variant Forward Read Depth",
    "Mpileup Qual: Filtered Variant Reverse Read Depth",
    "Mpileup Qual: Filtered Variant Binomial Proportion",
    "Mpileup Qual: Filtered Variant Binomial P Value",
    "Mpileup Qual: Filtered Variant Fishers Odds Ratio",
    "Mpileup Qual: Filtered Variant Fishers P Value",
    "Mpileup Qual: Filtered VAF",
    "Mpileup Qual: Unfiltered Variant Forward Read Depth",
    "Mpileup Qual: Unfiltered Variant Reverse Read Depth",
    "Mpileup Qual: Unfiltered Variant Binomial Proportion",
    "Mpileup Qual: Unfiltered Variant Binomial P Value",
    "Mpileup Qual: Unfiltered Variant Fishers Odds Ratio",
    "Mpileup Qual: Unfiltered Variant Fishers P Value",
    "Mpileup Qual: Unfiltered VAF",
    "VCF: LEN",
    "VCF: QD",
    "VCF: STB",
    "VCF: STBP",
    "VCF: SVTYPE",
    "VCF: TYPE",
    "VCF: QUAL",
    "Variant Annotation: Coding",
    "Variant Annotation: Sequence Ontology",
    "Variant Annotation: Transcript",
    "Variant Annotation: All Mappings",
    "UniProt (GENE): Accession Number",
    "dbSNP: rsID",
    "MDL: Sample Count",
    "MDL: Variant Frequency",
    "MDL: Sample List",
    "amp_ID",
    "Cytoband",
    "MANE_transcript (GRCh38)",
    "Genexus_transcript (GRCh37)",
    "Genexus_Exon(s)",
    "Genexus_codons",
    "tier",
    "test_tissue",
    "Disposition",
]

# Model Settings --------------------------------------------------------------

ADDON_LIST = [
    "amp_ID",
    "Cytoband",
    "MANE_transcript (GRCh38)",
    "Genexus_transcript (GRCh37)",
    "Genexus_Exon(s)",
    "Genexus_codons",
    "tier",
    "test_tissue",
]

# VCF File Settings -----------------------------------------------------------

VCF_FIELDS = [
    "Original Input: Chrom",
    "Original Input: Pos",
    "Original Input: Reference allele",
    "Original Input: Alternate allele",
    "Variant Annotation: Gene",
    "Variant Annotation: cDNA change",
    "Variant Annotation: Protein Change",
    "Variant Annotation: RefSeq",
    "VCF: AF",
    "VCF: FAO",
    "VCF: FDP",
    "VCF: HRUN",
    "VCF: Filter",
    "VCF: Genotype",
    "COSMIC: ID",
    "COSMIC: Variant Count",
    "COSMIC: Variant Count (Tissue)",
    "ClinVar: ClinVar ID",
    "ClinVar: Clinical Significance",
    "gnomAD3: Global AF",
    "PhyloP: Vert Score",
    "CADD: Phred",
    "PolyPhen-2: HDIV Prediction",
    "SIFT: Prediction",
    "VCF: FSAF",
    "VCF: FSAR",
    "VCF: FSRF",
    "VCF: FSRR",
    "VCF: Fisher Odds Ratio",
    "VCF: Fisher P Value",
    "VCF: Binom Proportion",
    "VCF: Binom P Value",
    "Mpileup Qual: Read Depth",
    "Mpileup Qual: Start Reads",
    "Mpileup Qual: Stop Reads",
    "Mpileup Qual: Filtered Reference Forward Read Depth",
    "Mpileup Qual: Filtered Reference Reverse Read Depth",
    "Mpileup Qual: Unfiltered Reference Forward Read Depth",
    "Mpileup Qual: Unfiltered Reference Reverse Read Depth",
    "Mpileup Qual: Filtered Variant Forward Read Depth",
    "Mpileup Qual: Filtered Variant Reverse Read Depth",
    "Mpileup Qual: Filtered Variant Binomial Proportion",
    "Mpileup Qual: Filtered Variant Binomial P Value",
    "Mpileup Qual: Filtered Variant Fishers Odds Ratio",
    "Mpileup Qual: Filtered Variant Fishers P Value",
    "Mpileup Qual: Filtered VAF",
    "Mpileup Qual: Unfiltered Variant Forward Read Depth",
    "Mpileup Qual: Unfiltered Variant Reverse Read Depth",
    "Mpileup Qual: Unfiltered Variant Binomial Proportion",
    "Mpileup Qual: Unfiltered Variant Binomial P Value",
    "Mpileup Qual: Unfiltered Variant Fishers Odds Ratio",
    "Mpileup Qual: Unfiltered Variant Fishers P Value",
    "Mpileup Qual: Unfiltered VAF",
    "VCF: LEN",
    "VCF: QD",
    "VCF: STB",
    "VCF: STBP",
    "VCF: SVTYPE",
    "VCF: TYPE",
    "VCF: QUAL",
    "Variant Annotation: Coding",
    "Variant Annotation: Sequence Ontology",
    "Variant Annotation: Transcript",
    "Variant Annotation: All Mappings",
    "UniProt (GENE): Accession Number",
    "dbSNP: rsID",
    "MDL: Sample Count",
    "MDL: Variant Frequency",
    "MDL: Sample List",
]

# InfoTrack DB Lookup Module --------------------------------------------------

INFOTRACK_REF_FOLDER = "reference"
INFOTRACK_REF_FILENAME = "infotrack_data_dump.tsv"
INFOTRACK_REF_COLUMNS = [
    "mol_num",
    "sample_name",
    "observed_variant_id",
    "run_id",
    "interpt_id",
    "genes",
    "coding",
    "amino_acid_change",
    "frequency",
    "genotype",
    "allele_coverage",
    "coverage",
    "include_in_report",
    "tier",
    "time_stamp",
    "confirm_status",
    "variant_allele",
    "ref_allele",
    "ref_var_strand_counts",
    "strand",
    "genetic_call",
    "test_tissue",
]

# Bed File Lookup Module ------------------------------------------------------

BED_REF_FOLDER = "reference"
BED_REF_FILENAME = "Genexus_bed_working.xlsx"
BED_REF_COLUMNS = [
    "Chrom",
    "bp_start",
    "bp_end",
    "amp_ID",
    "N_A",
    "amp_info",
    "Gene",
    "Cytoband",
    "Refseq (GRCh38)",
    "MANE_transcript (GRCh38)",
    "Genexus_transcript (GRCh37)",
    "Genexus_Exon(s)",
    "Genexus_codons",
]

# MAIN LOOP -------------------------------------------------------------------

def main() -> None:
    """Testing function for module."""

    pass

    return None

if __name__ == "__main__":
    main()
