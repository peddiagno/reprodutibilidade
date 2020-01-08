import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
import statistics

data_path = '../medidas'
results_path = '../resultados'
extension = 'csv'
os.chdir(data_path)
measures = glob.glob('*.{}'.format(extension))

measures_table = pd.read_csv(measures[0], na_values = "?", comment='\t',
                              sep=",", skipinitialspace=True )

headers = measures_table.columns
sds = []
means = []
cvs = []

for j in headers:
    sd = statistics.stdev(measures_table[j])
    mean = statistics.mean(measures_table[j])
    variation_coefficient = 100 * sd / mean
    sds.append(sd)
    means.append(mean)
    cvs.append(variation_coefficient)
    
measures_table.loc[len(measures_table)] = sds
measures_table.loc[len(measures_table)] = means
measures_table.loc[len(measures_table)] = cvs

measures_table.T.to_csv(results_path + "/" + measures[0])
    