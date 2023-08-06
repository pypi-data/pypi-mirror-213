#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 17:35:44 2023

@author: javiera.quiroz
"""

from FlyBaseDownloads.FBD import FBD 

db = FBD()

#Synonyms
Synonyms = FBD().Synonyms(db)

#Genes

Genes = FBD().Genes(db)

#Gene_groups
Gene_groups = FBD.Gene_groups(db)

#Alleles_Stocks
Alleles_Stocks = FBD.Alleles_Stocks(db)

#Homologs
Homologs = FBD.Homologs(db)

#Human_disease
Human_disease = FBD.Human_disease(db)

#Organisms
Organisms = FBD.Organisms(db)