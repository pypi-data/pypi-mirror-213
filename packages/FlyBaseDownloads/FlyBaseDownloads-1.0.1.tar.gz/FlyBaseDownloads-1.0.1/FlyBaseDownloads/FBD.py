#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 12:42:17 2023

@author: javiera.quiroz
"""

import pandas as pd
import fnmatch
import gzip
from ftplib import FTP
import re
import csv



class FBD():
    
    def __name__(self):
        self.__name__ = 'FlyBase Downloads'
    
    def __init__(self):
        self.main_url = 'ftp://ftp.flybase.net/releases/current/precomputed_files/'
    
    class Downloads():
        
        def __init__(self, url):
            
            self.url = url
            
        def download_file(self):
            
            url = self.url
            
            ftp = FTP(url.split('/')[2])
            ftp.login()
            ruta_directorio = '/'.join(url.split('/')[3:-1])


            ftp.cwd(ruta_directorio)

            archivos_remotos = ftp.nlst()

            archivos_filtrados = list(fnmatch.filter(archivos_remotos, url.split('/')[-1]))

            archivos = []
            for archivo in archivos_filtrados:
                with open('../' + archivo, 'wb') as archivo_local:
                    ftp.retrbinary('RETR ' + archivo, archivo_local.write)

                    archivos.append(archivo)

            ftp.quit()
            if len(archivos) > 0:
                return archivos
            else:
                print('Failed to download the file')
                return []
            
        
        
        
        def open_file(self, ruta_archivo, header):
            def df_r(df):
                if re.search(r"FB\w{9}", df.columns[0]):
                    df_columns = pd.DataFrame(df.columns).T

                    df.columns = range(len(df.columns))
                    
                    # Unir la fila de columnas con el resto del DataFrame
                    df = pd.concat([df_columns, df], ignore_index=True, axis = 0)
                
                if re.search('## Finished', df.iloc[-1,0]):
                    df = df.iloc[:-1, :]
                
                return df
            a = []

            if re.search(r'gz', ruta_archivo):
                
                try: 
                    with gzip.open('../' + ruta_archivo, 'rt') as archivo:
                       df = pd.read_csv(archivo, sep='\t', header=header)
                       a.append(df)
                    return df_r(a[0])
                
                except: 
                    try:
                        with gzip.open('../' + ruta_archivo, 'rt') as archivo:
                            df = csv.reader(archivo, delimiter='\t')
                            a.append(pd.DataFrame(df))
                    
                        df = a[0]
                        columns = df.iloc[header, :].tolist()
            
                        # Elimina la fila del encabezado del DataFrame
                        df = df.iloc[header + 1:, :]
                        
                        # Asigna los nuevos nombres de columna al DataFrame
                        df.columns = columns
                        df = df.dropna(axis='columns')
                      
      
                        return df_r(df)
                    except:
                        print('Failed to download the file') 
            
                    
    
    class Synonyms():
        
        def __init__(self, fbd_instance):
            self.db = fbd_instance
        
            self.main_url = self.db.main_url
            self.syn_url = 'synonyms/fb_synonym_*.tsv.gz'
            self.header = 3
            
        
        def get(self):
            
            url = self.main_url + self.syn_url
            
            descargas = self.db.Downloads(url)
            
            archivos = []
            
            archivos = descargas.download_file()
            
            return descargas.open_file(archivos[0], self.header)
        
    class Genes():
        
        def __init__(self, fbd_instance):
            self.db = fbd_instance
        
            self.main_url = self.db.main_url
            self.gen_url = 'genes/'
            
        def Genetic_interaction_table(self):
            self.un_url = 'gene_genetic_interactions_fb_*.tsv.gz'
            self.header = 3
            return self.get()
            
        def RNASeq_values(self):
            self.un_url = 'gene_rpkm_report_fb_*.tsv.gz'
            self.header = 5
            return self.get()
            
        def RNASeq_values_matrix(self):
            self.un_url = 'gene_rpkm_matrix_fb_*.tsv.gz'
            self.header = 4
            return self.get()       
            
        def Single_Cell_RNA_Gene_Expression(self):
            self.un_url = 'scRNA-Seq_gene_expression_fb_*.tsv.gz'
            self.header = 7
            return self.get()
            
        def Physical_interaction_MITAB(self):
            self.un_url = 'physical_interactions_mitab_fb_*.tsv.gz'
            self.header = 0
            return self.get()
                    
        def Functional_complementation(self):
            self.un_url = 'gene_functional_complementation_*.tsv.gz'
            self.header = 4
            return self.get()
        
        def FBgn_toDB_Accession_IDs(self):
            self.un_url = 'fbgn_NAseq_Uniprot_*.tsv.gz'
            self.header = 4
            return self.get()
        
        def FBgn_toAnnotation_ID(self):
            self.un_url = 'fbgn_annotation_ID_*.tsv.gz'
            self.header = 3
            return self.get()
        
        def FBgn_toGLEANR_IDs(self):
            self.un_url = 'fbgn_gleanr_*.tsv.gz'
            self.header = 3
            return self.get()
        
        def FBgn_to_FBtr_to_FBpp(self):
            self.un_url = 'fbgn_fbtr_fbpp_*.tsv.gz'
            self.header = 4
            return self.get()
        
        def FBgn_to_FBtr_to_FBpp_expanded(self):
            self.un_url = 'fbgn_fbtr_fbpp_expanded_*.tsv.gz'
            self.header = 4
            return self.get()
        
        def FBgn_exons2affy1(self):
            self.un_url = 'fbgn_exons2affy1_overlaps.tsv.gz'
            self.header = 0
            return self.get()
        
        def FBgn_exons2affy2(self):
            self.un_url = 'fbgn_exons2affy2_overlaps.tsv.gz'
            self.header = 0
            return self.get()
            
        def Genes_Sequence_Ontology(self):
            self.un_url = 'dmel_gene_sequence_ontology_annotations_fb_*.tsv.gz'
            self.header = 4
            return self.get()
        
        def Genes_map(self):
            self.un_url = 'gene_map_table_*.tsv.gz'
            self.header = 3
            return self.get()
            
        
        def Best_gene_summaries(self):
            self.un_url = 'best_gene_summary*.tsv.gz'
            self.header = 8
            return self.get()
                    
        def Automated_gene_summaries(self):
            self.un_url = 'automated_gene_summaries.tsv.gz'
            self.header = 1
            return self.get()
        
        def Gene_Snapshots(self):
            self.un_url = 'gene_snapshots_*.tsv.gz'
            self.header = 4
            return self.get()

            
        def Unique_protein_isoforms(self):
            self.un_url = 'dmel_unique_protein_isoforms_fb_*.tsv.gz'
            self.header = 3
            return self.get()
        
        #FALTA JSON NON-CODING
        
        def Enzyme(self):
            self.un_url = 'Dmel_enzyme_data_fb_*.tsv.gz'
            self.header = 4
            return self.get()
    
            
        
        def get(self):
            
            url = self.main_url + self.gen_url + self.un_url
            descargas = self.db.Downloads(url)
            
            archivos = []
            
            archivos = descargas.download_file()
            
            if len(archivos) > 0:
                return descargas.open_file(archivos[0], self.header)
        
    class Gene_groups():
        
        def __init__(self, fbd_instance):
            self.db = fbd_instance
        
            self.main_url = self.db.main_url
            self.gen_url = 'genes/'
            
        def get(self):
            
            url = self.main_url + self.gen_url + self.un_url
            descargas = self.db.Downloads(url)
            
            archivos = []
            
            archivos = descargas.download_file()
            
            if len(archivos) > 0:
                return descargas.open_file(archivos[0], self.header)
            
        def Gene_group(self):
            self.un_url = 'gene_group_data_fb_*.tsv.gz'
            self.header = 6
            return self.get()
        
        def Gene_groups_HGNC(self):
            self.un_url = 'gene_groups_HGNC_fb_*.tsv.gz'
            self.header = 6
            return self.get()
            
        def Pathway_group(self):
            self.un_url = 'pathway_group_data_fb_*.tsv.gz'
            self.header = 6
            return self.get()
            
    class Alleles_Stocks():
        
        def __init__(self, fbd_instance):
            self.db = fbd_instance
        
            self.main_url = self.db.main_url
            self.gen_url = ''
            
        def get(self):
            
            url = self.main_url + self.gen_url + self.un_url
            descargas = self.db.Downloads(url)
            
            archivos = []
            
            archivos = descargas.download_file()
            
            if len(archivos) > 0:
                return descargas.open_file(archivos[0], self.header)
            
        def Stock(self):
            self.gen_url = 'stocks/'
            self.un_url = 'stocks_*.tsv.gz'
            self.header = 0
            return self.get()
            
        def Allele_genetic_interactions(self):
            self.gen_url = 'alleles/'
            self.un_url = 'allele_genetic_interactions_*.tsv.gz'
            self.header = 3
            return self.get()
                
        def Phenotypic(self):
            self.gen_url = 'alleles/'
            self.un_url = 'genotype_phenotype_data_*.tsv.gz'
            self.header = 4
            return self.get()
        
        def FBal_to_FBgn(self):
            self.gen_url = 'alleles/'
            self.un_url = 'fbal_to_fbgn_fb_*.tsv.gz'
            self.header = 1
            return self.get()
        
    class Homologs():
        
        def __init__(self, fbd_instance):
            self.db = fbd_instance
        
            self.main_url = self.db.main_url
            self.gen_url = 'orthologs/'
            
        def get(self):
            
            url = self.main_url + self.gen_url + self.un_url
            descargas = self.db.Downloads(url)
            
            archivos = []
            
            archivos = descargas.download_file()
            
            if len(archivos) > 0:
                return descargas.open_file(archivos[0], self.header)
            
        def Drosophila_Paralogs(self):
            self.un_url = 'dmel_paralogs_fb_*.tsv.gz'
            self.header = 4
            return self.get()
        
        def Human_Orthologs(self):
            self.un_url = 'dmel_human_orthologs_disease_fb_*.tsv.gz'
            self.header = 3
            return self.get()
        
    class Human_disease():
        
        def __init__(self, fbd_instance):
            self.db = fbd_instance
        
            self.main_url = self.db.main_url
            self.gen_url = 'human_disease/'
            
        def get(self):
            
            url = self.main_url + self.gen_url + self.un_url
            descargas = self.db.Downloads(url)
            
            archivos = []
            
            archivos = descargas.download_file()
            
            if len(archivos) > 0:
                return descargas.open_file(archivos[0], self.header)
            
        def Disease_model_annotations(self):
            self.gen_url = 'human_disease/'
            self.un_url = 'disease_model_annotations_fb_*.tsv.gz'
            self.header = 4
            return self.get()
        
        def Human_Orthologs(self):
            self.gen_url = 'orthologs/'
            self.un_url = 'dmel_human_orthologs_disease_fb_*.tsv.gz'
            self.header = 3
            return self.get()
        
    class Organisms():
        
        def __init__(self, fbd_instance):
            self.db = fbd_instance
        
            self.main_url = self.db.main_url
            self.org_url = 'species/organism_list_fb*.tsv.gz'
            self.header = 4
            
        
        def Species_list(self):
            
            url = self.main_url + self.org_url
            
            descargas = self.db.Downloads(url)
            
            archivos = []
            
            archivos = descargas.download_file()
            
            return descargas.open_file(archivos[0], self.header)
            

        