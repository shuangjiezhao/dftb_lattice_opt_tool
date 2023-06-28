# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 11:27:34 2023

@author: image
"""

import numpy as np
from ase import io
import ase
import os
from ase.geometry.analysis import Analysis
import shutil
import pandas as pd
import re

class lattice_opt:
    def __init__(self):
        self.gradient_number = None
        self.step_length = None
        self.folder_name = None
        self.folder_path = None
        self.output = None
        self.subdir_layernum = None
    
    def save_parameters(self,gradient_number,step_length,folder_name,folder_path,output,subdir_layernum):
        self.gradient_number = gradient_number
        self.step_length = step_length
        self.folder_name = folder_name
        self.folder_path = folder_path
        self.output = output
        self.subdir_layernum = subdir_layernum

#pre-set DFTB angular momenta
    def pre_set_momenta(self):
        angular_m_dic = {
            'C': 'C = "p"',
            'H': 'H = "s"',
            'O': 'O = "p"',
            'N': 'N = "p"',
            'Si': 'Si = "p"',
            'S': 'S = "p"',
            'B': 'B = "p"',
            'P': 'P = "d"',
            'F': 'F = "p"'
        }
        return angular_m_dic
    
    #add more if you want
    def add_momenta(self,angular_m_dic,symbol,shell):
        angular_m_dic[symbol] = f'{symbol} = "{shell}"'
        return angular_m_dic
    
    #delete what you want
    def delete_momenta(self,angular_m_dic,symbol):
        angular_m_dic.pop(symbol,None)
        return angular_m_dic
    
#read path of geometry files
    def read_path(self,pwd):
        fullpath = os.walk(pwd)
        geo_path_list = []
        for i in fullpath:
            if i[1] == [] and self.output in i[2]:
                geo_path_list.append(os.path.join(i[0],self.output))
        return geo_path_list

    
#read and get geometry ready based on lattice gradient
    def lattice_sep(self,geo): #n is interger,geo is ase Atoms
        n = self.gradient_number
        step_len = self.step_length
        vector = geo.get_cell()
        geo_collect = []
        for i in range(-n,n+1,1):
            geo_copy = geo.copy()
            vector_opt = list([j*(1+i*step_len) for j in vector[0:2]])
            vector_opt.append(vector[2])
            print(vector_opt)
            geo_copy.cell = vector_opt
            geo_collect.append(geo_copy)
        return geo_collect

#create different folders based on gradient and name of first folder
    def folders_make(self,geo_path_list):
        n = self.gradient_number
        step_len = self.step_length
        name = self.folder_name
        subdir_layernum = self.subdir_layernum
        for i in geo_path_list:
            segment = re.split('/|\\\\',i)[0:-1]
            segment.reverse()
            path = f'{self.folder_path}/{name}/'
            for i in segment[subdir_layernum::-1]:
                path = os.path.join(path,i)     
            for j in range(-n,n+1,1):
                os.makedirs(os.path.join(path,str(j*step_len)))
        return
                
#assign geometry into correct folders
    def assign_geo(self,geo_collect_all,geo_path_list):
        n = self.gradient_number
        step_len = self.step_length
        subdir_layernum = self.subdir_layernum
        #give geometry collection of every original geometry, how many gradients, and the whole list of path of original geometry
        for i,j in zip(geo_collect_all,geo_path_list):
            segment = re.split('/|\\\\',j)[0:-1]
            subpath = '/'.join(segment[-subdir_layernum-1::])
            a = -int(n)
            for m in i:
                io.write(f'{self.folder_path}/{self.folder_name}/{subpath}/{a*step_len}/dftb_in.gen',m)
                a+=1
        return       

#maybe first generate an array that contains hsd for all original geometry, then second write them into every subdirectory?
#generate hsd for every original geometry
    def generate_hsd(self,geo_list,path_hsd_template,angular_m_dic,layer_sep_index):
#layer_sep_index should be a list for the index of last atom belonging to the first layer,should be the same sequence as geo_list
        hsd = pd.read_fwf(path_hsd_template)
        hsd_content = hsd.values
        species_position = np.argwhere(hsd_content == 'MaxAngularMomentum = {')[0][0]+1
        moved_atom = np.argwhere(hsd_content == 'MaxSteps = 30000')[0][0]-1
        hsd_collect = []
        for geo,sep in zip(geo_list,layer_sep_index):   #geo_list is the collection of original geometry
            hsd_content = hsd.values
            species = set(geo.get_chemical_symbols())
            for symbol,species_index in zip(species,range(int(species_position),int(species_position)+len(species))):
                 hsd_content = np.insert(hsd_content,species_index,angular_m_dic[symbol])  
            
            if sep == None:
                hsd_content = np.insert(hsd_content,moved_atom,'MovedAtoms = 1:-1')
            else:
                hsd_content = np.insert(hsd_content,moved_atom,f'MovedAtoms = 1:{sep}')
             
            hsd_collect.append(hsd_content)
            
        return hsd_collect
            



#assign dftb_in.hsd into correct folders
    def assign_hsd(self,geo_collect_all,hsd_collect,geo_path_list):
        n = self.gradient_number
        step_len = self.step_length
        subdir_layernum = self.subdir_layernum
        for i,j,k in zip(geo_collect_all,geo_path_list,hsd_collect):
            segment = re.split('/|\\\\',j)[0:-1]
            subpath = '/'.join(segment[-subdir_layernum-1::])

            a = -int(n)
            
            for m in i:
                with open (f'{self.folder_path}/{self.folder_name}/{subpath}/{a*step_len}/dftb_in.hsd','w') as hsd_file:
                    hsd_file.write('Geometry = GenFormat {'+'\n')
                    for line in k:
                        hsd_file.write(str(line)+'\n')
                a+=1
        return
    
#assign submit file into correct folders
    def assign_submit(self,geo_collect_all,path_submit_template,geo_path_list):
        n = self.gradient_number
        step_len = self.step_length
        subdir_layernum = self.subdir_layernum
        for i,j in zip(geo_collect_all,geo_path_list):
            segment = re.split('/|\\\\',j)[0:-1]
            subpath = '/'.join(segment[-subdir_layernum-1::])
            
            a = -int(n)
            for m in i:
                shutil.copy2(path_submit_template,f'{self.folder_path}/{self.folder_name}/{subpath}/{a*step_len}')
                a+=1
        return