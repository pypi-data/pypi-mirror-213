# FlyBaseDownloads

Python package to facilitate the data download from FlyBase. Most of the available data from their official wiki can be downloaded. One of the purposes of this library is to organize the data as closely as possible to the source, **FlyBase**. Despite not being the official package, it is organized by data class/type and provides direct downloads of the current bulk data files from the FTP site.
For more information, visit the [official FlyBase wiki](https://wiki.flybase.org/wiki/FlyBase:Downloads_Overview).


# Bulk data files

In order to simplify the download of FlyBase files, the names have been kept as close as possible. To access the data, follow these steps:

1. Install the library using the pip command.

> pip install FlyBaseDownloads

2. Import the library into your file.

> import FlyBaseDownloads as FBD

3. Access the different classes of the library described below.



## Synonyms

To download the file, execute the following command.
> Synonyms = FBD.Synonyms.get()

The file reports current symbols and synonyms for the following objects in FlyBase: genes (FBgn), alleles (FBal), balancers (FBba), aberrations (FBab), transgenic constructs (FBtp), insertions (FBti), transcripts (FBtr), and proteins (FBpp).

Columns Description

| Column heading           | Content Description          |
|----------------------|--------------------|
| primary_FBid   | Primary FlyBase identifier for the object |
| organism_abbreviation   | Abbreviation (from the Species Abbreviations list) indicating the species of origin |
| current_symbol   | Current symbol used in FlyBase for the object |
| current_fullname   | Current full name used in FlyBase for the object|
| fullname_synonym(s)   | 	Non-current full name(s) associated with the object (pipe separated values) |
| symbol_synonym(s)   | Non-current symbol(s) associated with the object (pipe separated values) |


## Genes

To facilitate its usage, it is suggested to access the data using the following command.

> Genes = FBD.Genes

Then, enter the specific method according to the desired data

#### Genetic interaction table

To download the file, execute the following command.
> Genetic_interaction_table = Genes.Genetic_interaction_table()

#### RNA-Seq RPKM values

To download the file, execute the following command.
> RNASeq_values = Genes.RNASeq_values()

#### RNA-Seq RPKM values matrix

To download the file, execute the following command.
> RNASeq_values_matrix = Genes.RNASeq_values_matrix()

#### Single Cell RNA-Seq Gene Expression

To download the file, execute the following command.
> SingleCellRNASeq_Gene_Expression = Genes.Single_Cell_RNA_Gene_Expression()

#### Physical interaction MITAB file

To download the file, execute the following command.
> Physical_interaction_MITAB = Genes.Physical_interaction_MITAB()

#### Functional complementation table

To download the file, execute the following command.
> Functional_complementation = Genes.Functional_complementation()

#### FBgn to DB Accession IDs

To download the file, execute the following command.
> FBgn_toDB_Accession_IDs = Genes.FBgn_toDB_Accession_IDs()

#### FBgn to Annotation ID

To download the file, execute the following command.
> FBgn_toAnnotation_ID = Genes.FBgn_toAnnotation_ID()

#### FBgn to GLEANR IDs

To download the file, execute the following command.
> FBgn_toGLEANR_IDs = Genes.FBgn_toGLEANR_IDs()

#### FBgn to FBtr to FBpp IDs

To download the file, execute the following command.
> FBgn_to_FBtr_to_FBpp = Genes.FBgn_to_FBtr_to_FBpp()

#### FBgn to FBtr to FBpp IDs (expanded)

To download the file, execute the following command.
> FBgn_to_FBtr_to_FBpp_exp = Genes.FBgn_to_FBtr_to_FBpp_expanded()

#### FBgn exons to Affy1 

To download the file, execute the following command.
> FBgn_exons2affy1 = Genes.FBgn_exons2affy1()

#### FBgn exons to Affy2

To download the file, execute the following command.
> FBgn_exons2affy2 = Genes.FBgn_exons2affy2()

#### Genes Sequence Ontology (SO) data

To download the file, execute the following command.
> Genes_Sequence_Ontology = Genes.Genes_Sequence_Ontology()

#### Genes map table

To download the file, execute the following command.
> Genes_map = Genes.Genes_map()

#### Best gene summaries

To download the file, execute the following command.
> Best_gene_summaries = Genes.Best_gene_summaries()

#### Gene Snapshots

To download the file, execute the following command.
> Gene_Snapshots = Genes.Gene_Snapshots()

#### Unique protein isoforms

To download the file, execute the following command.
> Unique_protein_isoforms = Genes.Unique_protein_isoforms()

#### Enzyme data

To download the file, execute the following command.
> Enzyme = Genes.Enzyme()


