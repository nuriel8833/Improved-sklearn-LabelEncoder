##########################################################################
#                     Corrected LabelEncoder()
#         Created by Nuriel Reuven , All Rights Reserved © 2022
##########################################################################

import pandas as pd
import numpy as np

class LabelEncoder():

    def __init__(self , series = None , dict = None, labels = None , ignorenan = False):
        self.series = series
        self.dict = dict
        self.labels = labels
        self.ignorenan = ignorenan
        
    def mapping(self , series , encodeddictionary = None , ignorenan = False):
        self.series = series
        if isinstance(series, pd.core.series.Series) == False:
            raise Exception('"series" input is not a Pandas series')
        if encodeddictionary == None:
            encodedict = {}
        else:
            if isinstance(series, pd.core.series.Series) == False:
                raise Exception('"encodeddictionary" input is not a dictionary')
            encodedict = encodeddictionary
        code = len(encodedict)+1
        vseries = pd.unique(series)
        for i in vseries:
            if i not in encodedict.keys():
                if self.ignorenan == False:
                    if pd.isnull(i) == True:
                        encodedict[np.nan] = 0
                        continue
                    encodedict[i] = code
                    code += 1
            else:
                continue
        self.dict = encodedict
        self.labels = list(encodedict.keys())
        self.ignorenan = ignorenan
        return encodedict

    def encode(self, series, encodeddictionary):
        if isinstance(series, pd.core.series.Series) == False:
            raise Exception('Input is not a Pandas series')
        if isinstance(encodeddictionary, dict) == False:
            raise Exception('"encodeddictionary" input is not a dictionary')
        res = series.apply(lambda x: encodeddictionary[x] if x in encodeddictionary.keys() else x)
        return res

    def decode(self, series, encodeddictionary):
        if isinstance(series, pd.core.series.Series) == False:
            raise Exception('Input is not a Pandas series')
        if isinstance(encodeddictionary, dict) == False:
            raise Exception('"encodeddictionary" input is not a dictionary')
        res = series.apply(lambda x: list(encodeddictionary.keys())[list(encodeddictionary.values()).index(x)] if x in encodeddictionary.values() else x)
        return res

    def isnan(self):
        return True if 0 in self.dict.values() else False

    def set_value(self, label , value):
        if isinstance(value, (int, float)) == False:
            raise Exception('"value" is not an integer or a float')
        if self.dict == None:
            raise Exception('No encoding was created! Encode before setting a value.')
        else:
            if label not in self.labels:
                raise Exception('This label was not encoded and does not exist.')
            if pd.isnull(value):
                raise Exception('Can not encode NaNs. To encode NaNs use set_nan() function.')
            else:
                if value in self.dict.values():
                    prevlabel = list(self.dict.keys())[list(self.dict.values()).index(value)]
                    del self.dict[prevlabel]
                    print(f'{value} was already the encode of {prevlabel}, now {prevlabel} is encoded as {max(self.dict.values())+1}')
                    self.dict[prevlabel] = max(self.dict.values())+1
                del self.dict[label]
                self.dict[label] = value
                self.labels.append(label)
                return f'Label {label} and its encoded value {value} were successfully added!'

    def ignore_nans(self, value):
        if isinstance(value, bool) == False:
            raise Exception('"value" is not a boolean.')
        self.ignorenan = value
        if value == True:
            return f'Encoder settings was changed and is now succesfully not encoding NaNs'
        else:
            return f'Encoder settings was changed and is now succesfully encoding NaNs'

    def set_nan(self, value):
        return self.set_value(np.nan , value)

    def add_label(self, label , value):
        if isinstance(value, (int, float)) == False:
            raise Exception('"value" is not an integer or a float')
        if self.dict == None:
            raise Exception('No encoding was created! Encode before setting a value.')
        else:
            if label in self.labels:
                raise Exception('This label was already encoded , use set_value() to set a different encode or remove_value() to remove it')
            else:
                if value in self.dict.values():
                    prevlabel = list(self.dict.keys())[list(self.dict.values()).index(value)]
                    del self.dict[prevlabel]
                    print(f'{value} was already the encode of {prevlabel}, now {prevlabel} is encoded as {max(self.dict.values())+1}')
                    self.dict[prevlabel] = max(self.dict.values())+1
                self.dict[label] = value
                self.labels.append(label)
                return f'Label {label} and its encoded value {value} were successfully added!'

    def remove_label(self, label):
        if self.dict == None:
            raise Exception('No encoding was created! Encode before setting a value.')
        else:
            if label not in self.labels:
                raise Exception('This label was not encoded.')
            else:
                value = self.dict[label]
                del self.dict[label]
                self.labels.remove(label)
                return f'Label {label} and its encoded value {value} were successfully removed!'

    def summary(self):
        if self.dict == None or self.labels == None:
            raise Exception('No series was encoded. Use LabelEncoder().mapping to create the labels dictionary and LabelEncoder().encode to encode a series')
    
        else:
            print('===============[Encoder Summary]===============')
            print(f'Encoding Dictionary: \n{self.dict}') 
            print('-----------------------------------------------')
            print(f'Labels:\n {self.labels}')
            print('-----------------------------------------------')      
            print(f'Total number of unique labels: {len(self.labels)}\nNaNs found: {self.isnan()}')
            if self.ignorenan == True:
                print('The encoder does not encode NaNs')
            else:
                print('The encoder does encode NaNs')
            print('===============================================')
