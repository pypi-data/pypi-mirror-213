#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 21:32:56 2023

@author: muthyala.7
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 21:42:41 2023

@author: muthyala.7
"""
import torch 
import pandas as pd 
import numpy as np 
import warnings
import itertools
import time
from itertools import combinations
import pdb
class feature_space_construction:

  '''
  ##############################################################################################################
  Define global variables like number of operators and the input data frame and the operator set given

  ############################################################################################################## 
  '''
  def __init__(self,operators,df,no_of_operators=3,device='cpu',list1=None):
    print(f'Starting Feature Space Construction in {device}')
    self.no_of_operators = no_of_operators
    self.df = df
    self.operators = operators
    self.device = torch.device(device)
    self.dimensionality = list1
    #Manipulate the dataframe by selecting only the numerical datatypes and popping out the target column
    self.df = self.df.select_dtypes(include=['float64','int64'])
    # Compute the variance of each column
    variance = self.df.var()

    # Get the names of the zero variance columns
    zero_var_cols = variance[variance == 0].index

    # Drop the zero variance columns from the dataframe
    self.df = self.df.drop(zero_var_cols, axis=1)

    self.df.rename(columns = {f'{self.df.columns[0]}':'Target'},inplace=True)
    self.Target_column = torch.tensor(self.df.pop('Target')).to(self.device)

    # Get the column values and convert it to tensor 
    self.df_feature_values = torch.tensor(self.df.values).to(self.device)
    #Create a dataframe for appending new datavalues 
    self.new_features_values = pd.DataFrame()

    #Get the column headers 
    self.columns = self.df.columns.tolist()
    
    #Creating empty tensor for single operators
    self.feature_values = torch.empty(self.df.shape[0],0).to(self.device)
    self.feature_names = []
    #creating empty tensor for combinations
    self.feature_values1 = torch.empty(self.df.shape[0],0).to(self.device)
    self.feature_names1 = []
  '''
  ###############################################################################################################

  Construct all the features that can be constructed using the single operators like log, exp, sqrt etc..

  ###############################################################################################################
  '''

  def single_variable(self,operators_set): 
    #Check for the validity of the operator set given
    self.feature_values = torch.empty(self.df.shape[0],0).to(self.device)
    self.feature_names = []
    for op in operators_set:

      if op in ['exp','sin','cos','sqrt','cbrt','log','ln','^-1','^2','^3','exp(-1)']:
        continue
      else:
        raise TypeError('Invalid Operator found in the given operator set')
    
    #Looping over operators set to get the new features/predictor variables 

    for op in operators_set:
        self.feature_values_11 = torch.empty(self.df.shape[0],0).to(self.device)
        feature_names_12 =[]
        if op == 'exp':
            exp = torch.exp(self.df_feature_values)
            self.feature_values_11 = torch.cat((self.feature_values_11,exp),dim=1)
            feature_names_12.extend(list(map(lambda x: '(exp('+ x + "))", self.columns)))
        elif op =='ln':
            ln = torch.log(self.df_feature_values)
            self.feature_values_11 = torch.cat((self.feature_values_11,ln),dim=1)
            feature_names_12.extend(list(map(lambda x: '(ln('+x + "))", self.columns)))
        elif op =='log':
            log10 = torch.log10(self.df_feature_values)
            self.feature_values_11 = torch.cat((self.feature_values_11,log10),dim=1)
            feature_names_12.extend(list(map(lambda x: '(log('+x + "))", self.columns)))
        elif op =='cbrt':
            cbrt = torch.pow(self.df_feature_values,1/3)
            self.feature_values_11 = torch.cat((self.feature_values_11,cbrt),dim=1)
            feature_names_12.extend(list(map(lambda x: '(cbrt('+x + "))", self.columns)))
        elif op == 'sqrt':
            sqrt = torch.pow(self.df_feature_values,1/2)
            self.feature_values_11 = torch.cat((self.feature_values_11,sqrt),dim=1)
            feature_names_12.extend(list(map(lambda x: '(sqrt('+x + "))", self.columns)))
        elif op =='sin':
            sin = torch.sin(self.df_feature_values)
            self.feature_values_11 = torch.cat((self.feature_values_11,sin),dim=1)
            feature_names_12.extend(list(map(lambda x: '(sin('+x + "))", self.columns)))
        elif op =='cos':
            cos = torch.cos(self.df_feature_values)
            self.feature_values_11 = torch.cat((self.feature_values_11,cos),dim=1)
            feature_names_12.extend(list(map(lambda x: '(cos('+x + "))", self.columns)))
        elif op == '^2':
            square = torch.pow(self.df_feature_values,2)
            self.feature_values_11 = torch.cat((self.feature_values_11,square),dim=1)
            feature_names_12.extend(list(map(lambda x: '(('+x + ")^2)", self.columns)))
        elif op =='^3':
            cube = torch.pow(self.df_feature_values,3)
            self.feature_values_11 = torch.cat((self.feature_values_11,cube),dim=1)
            feature_names_12.extend(list(map(lambda x: '(('+x + ")^3)", self.columns)))
        elif op =='^-1':
            reciprocal = torch.reciprocal(self.df_feature_values)
            self.feature_values_11 = torch.cat((self.feature_values_11,reciprocal),dim=1)
            feature_names_12.extend(list(map(lambda x: '(('+x + ")^(-1))", self.columns)))
        elif op =='exp(-1)':
            expreciprocal = torch.reciprocal(exp)
            self.feature_values_11 = torch.cat((self.feature_values_11,expreciprocal),dim=1)
            feature_names_12.extend(list(map(lambda x: '(exp('+x + ")^(-1))", self.columns)))
        self.feature_values = torch.cat((self.feature_values,self.feature_values_11),dim=1)
        self.feature_names.extend(feature_names_12)
            
    
        
    #Check for empty lists 
    if len(self.feature_names) == 0:
        return self.feature_values, self.feature_names
    else:
        # create Boolean masks for NaN and Inf values
        #self.feature_values =  torch.cat(self.feature_values3,dim=1)
        nan_columns = torch.any(torch.isnan(self.feature_values), dim=0)
        inf_columns = torch.any(torch.isinf(self.feature_values), dim=0)
        nan_or_inf_columns = nan_columns | inf_columns
    
        # Remove columns from tensor
        self.feature_values = self.feature_values[:, ~nan_or_inf_columns]
    
        # Remove corresponding elements from list
        self.feature_names = [elem for i, elem in enumerate(self.feature_names) if not nan_or_inf_columns[i]]
        return self.feature_values, self.feature_names #self.new_features_values
  


  '''
  ################################################################################################

  Defining method to perform the combinations of the variables with the initial feature set
  ################################################################################################
  '''
  def combinations(self,operators_set):
      #creating empty tensor for combinations
      self.feature_values1 = torch.empty(self.df.shape[0],0).to(self.device)
      self.feature_names1 = []
    #Checking for the operator set
      for op in operators_set:
        if op in ['+','-','*','/']:
          continue
        else:
          raise TypeError("Valid set of operators +,-,*,/, abs please check the operators set")
          break
      
      #Defining the set of combinations to be performed

      #getting list of cobinations without replacement using itertools 
      combinations1 = list(combinations(self.columns,2))
      combinations2 = torch.combinations(torch.arange(self.df_feature_values.shape[1]),2)
      comb_tensor = self.df_feature_values.T[combinations2,:]
      #Reshaping to match
      x_p = comb_tensor.permute(0,2,1)
      for op in operators_set:
          self.feature_values11 = torch.empty(self.df.shape[0],0).to(self.device)
          feature_names_11 = []
          if op =='+':
              sum = torch.sum(x_p,dim=2).T
              self.feature_values11 = torch.cat((self.feature_values11,sum),dim=1)
              feature_names_11.extend(list(map(lambda comb: '('+'+'.join(comb)+')', combinations1)))
          elif op =='-':
              sub = torch.sub(x_p[:,:,0],x_p[:,:,1]).T
              self.feature_values11 = torch.cat((self.feature_values11,sub),dim=1)
              feature_names_11.extend(list(map(lambda comb: '('+'-'.join(comb)+')', combinations1)))
          elif op == '/':
              div1 = torch.div(x_p[:,:,0],x_p[:,:,1]).T
              div2 = torch.div(x_p[:,:,1],x_p[:,:,0]).T
              self.feature_values11 = torch.cat((self.feature_values11,div1,div2),dim=1)
              feature_names_11.extend(list(map(lambda comb: '('+'/'.join(comb)+')', combinations1)))
              feature_names_11.extend(list(map(lambda comb: '('+'/'.join(comb[::-1])+')', combinations1)))
          elif op == '*':
              mul = torch.multiply(x_p[:,:,0],x_p[:,:,1]).T
              self.feature_values11 = torch.cat((self.feature_values11,mul),dim=1)
              feature_names_11.extend(list(map(lambda comb: '('+'*'.join(comb)+')', combinations1)))
          self.feature_values1 = torch.cat((self.feature_values1,self.feature_values11),dim=1)
          self.feature_names1.extend(feature_names_11)
              
      #Checking whether the lists are empty
      if len(self.feature_names1) == 0:
          return self.feature_values1, self.feature_names1
      else:
          #Removing Nan and inf columns from tenosr and corresponding variable name form the list
          #self.feature_values1 = torch.cat(self.feature_values2,dim=1)
          nan_columns = torch.any(torch.isnan(self.feature_values1), dim=0)
          inf_columns = torch.any(torch.isinf(self.feature_values1), dim=0)
          nan_or_inf_columns = nan_columns | inf_columns
    
          # Remove columns from tensor
          self.feature_values1 = self.feature_values1[:, ~nan_or_inf_columns]
    
          # Remove corresponding elements from list
          self.feature_names1 = [elem for i, elem in enumerate(self.feature_names1) if not nan_or_inf_columns[i]]
    
          #Returning the dataframe created
          return self.feature_values1,self.feature_names1 #created_space
  

  '''
  ##########################################################################################################

  Creating the space based on the given set of conditions

  ##########################################################################################################

  '''

  def feature_space(self):
    #based on the dimension we will be performing the feature space creation
    if self.no_of_operators+1 > 9: print('****************************************************** \n','Currently TorchSisso supports Feature Space Expansion till complexity of 7, provided input argument > 7. Featureee Expansion with complexity of 7 will be returned \n', '*******************************************************')
    start_time = time.time()
    basic_operators = [op for op in self.operators if op in ['+', '-', '*', '/']]
    other_operators = [op for op in self.operators if op not in ['+', '-', '*', '/']]
    
    values, names = self.combinations(basic_operators)
    values1, names1 = self.single_variable(other_operators)
    #Merging two dataframes
    space_created = torch.cat((self.df_feature_values,values,values1), dim=1).to(self.device)
    self.columns = self.columns + names + names1 
    del values, values1, names, names1
    print('First Feature Space building is completed with features count: ',int(space_created.shape[1]))
    print('Time for phi1 creation is: ',round(time.time() - start_time,3),' seconds')
    #Update the columns according to the new phi created for the next phase features
    self.df_feature_values = (space_created).to(self.device)
    #Creating the phi2 based on the space created 
    start_time = time.time()
    values, names = self.combinations(basic_operators)
    values1, names1 = self.single_variable(other_operators)
    space_created_2 = torch.cat((space_created,values,values1), dim=1).to(self.device)
    del space_created,values,values1
    self.columns = self.columns + names + names1 
    del names, names1
    #######################
    #code to remove duplicate columns from dataframe
    #########################
    #Converting tensor to numpy and then dataframe to remove duplicates
    space = pd.DataFrame(space_created_2.cpu(),columns = self.columns)
    space = space.round(7)
    space = space.T.drop_duplicates().T
    space = space.dropna(axis=1, how='any')
    self.columns = space.columns.tolist()
    self.df_feature_values = torch.tensor(space.values).to(self.device)
    del space_created_2,space
    print('Second Feature Space building is completed with features count: ',int(self.df_feature_values.shape[1]))
    print('Time taken to create and remove redundant features in phi2 is ', round(time.time() - start_time,3), ' seconds')

    if self.no_of_operators >3: 
      for i in range(4,self.no_of_operators+1):
        if i == 4:
          start = time.time()
          values, names = self.combinations(basic_operators)
          values1,names1 = self.single_variable(other_operators)
          space_created_3 = torch.cat((self.df_feature_values,values,values1),dim=1).to(self.device)
          #space_created_3 = torch.cat((values,self.df_feature_values),dim=1).to(self.device)
          del values,values1
          self.columns = self.columns + names + names1
          del names,names1
          #self.columns = names + self.columns
          space1 = space_created_3.cpu().numpy()
          del space_created_3
          space = pd.DataFrame(space1,columns = self.columns)
          del space1
          space = space.dropna(axis=1, how='any')
          space = space.round(7)
          # Transpose the dataframe
          space = space.T.drop_duplicates().T
          self.columns = space.columns.tolist()
          self.df_feature_values = torch.tensor(space.values).to(self.device)
          del space
          print('Third Feature Space building is completed',self.df_feature_values.shape[1])
          print('Time taken to build the phi3 is',  round(time.time()-start,3) ,'seconds')
          if self.no_of_operators+1 == 5:
            return self.df_feature_values,self.Target_column,self.columns  #space
          else:
            continue
        if i == 5:
          start = time.time()
          values, names = self.combinations(basic_operators)
          values1,names1 = self.single_variable(other_operators)
          space_created_4 = torch.cat((self.df_feature_values,values,values1),dim=1).to(self.device)
          del values,values1
          self.columns = self.columns + names + names1
          del names,names1
          space1 = space_created_4.cpu().numpy()
          del space_created_4
          space = pd.DataFrame(space1,columns = self.columns)
          del space1
          space = space.dropna(axis=1, how='any')
          space = space.round(7)
          # Transpose the dataframe
          space = space.T.drop_duplicates().T
          self.df_feature_values = torch.tensor(space.values).to(self.device)
          self.columns = space.columns.tolist()
          self.df_feature_values = torch.tensor(space.values).to(self.device)
          del space
          print('Third Feature Space building is completed',space.shape[1])
          print('Time taken to build the phi4 is',  round(time.time()-start,3) ,'seconds')
          if self.no_of_operators+1 == 6:
            return self.df_feature_values,self.Target_column,self.columns
          else:
            continue
        if i == 6:
          start = time.time()
          values, names = self.combinations(basic_operators)
          values1,names1 = self.single_variable(other_operators)
          space_created_5 = torch.cat((self.df_feature_values,values,values1),dim=1).to(self.device)
          del values,values1
          self.columns = self.columns + names + names1
          del names, names1
          space1 = space_created_5.cpu().numpy()
          space = pd.DataFrame(space1,columns = self.columns)
          del space1
          space = space.dropna(axis=1, how='any')
          space = space.round(7)
          # Transpose the dataframe
          space = space.T.drop_duplicates().T
          self.df_feature_values = torch.tensor(space.values).to(self.device)
          self.columns = space.columns.tolist()
          del space
          print('Third Feature Space building is completed',space.shape[1])
          print('Time taken to build the phi5 is',  round(time.time()-start,3) ,'seconds')
          if self.no_of_operators+1 == 7:
            return self.df_feature_values,self.Target_column,self.columns
          else:
            continue
        if i == 7:
          start = time.time()
          values, names = self.combinations(basic_operators)
          values1,names1 = self.single_variable(other_operators)
          space_created_6 = torch.cat((self.df_feature_values,values,values1),dim=1).to(self.device)
          del values,values1
          self.columns = self.columns + names + names1
          del names, names1
          space1 = space_created_6.cpu().numpy()
          space = pd.DataFrame(space1,columns = self.columns)
          del space1
          space = space.dropna(axis=1, how='any')
          space = space.round(7)
          # Transpose the dataframe
          space = space.T.drop_duplicates().T
          self.df_feature_values = torch.tensor(space.values).to(self.device)
          self.columns = space.columns.tolist()
          del space
          print('Third Feature Space building is completed',space.shape[1])
          print('Time taken to build the phi6 is',  round(time.time()-start,3) ,'seconds')
          
          if self.no_of_operators+1 == 8:
            return self.df_feature_values,self.Target_column,self.columns
          else:
              print('Currently TorchSisso supports Feature Space Expansion till complexity of 7, provided input argument > 7. Further Feature Expansion cannot be performed, returning the last expanded feature space')
              return self.df_feature_values,self.Target_column,self.columns
          

    else:
      return self.df_feature_values, self.Target_column,self.columns
