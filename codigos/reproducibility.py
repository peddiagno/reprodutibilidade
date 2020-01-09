import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
import statistics

data_path = 'medidas'
results_path = '../resultados'
extension="csv"
os.chdir(data_path)

measures   = glob.glob('*results.csv')
pulses_plt_files = glob.glob('*plt.csv')
pulses_wbc_files = glob.glob('*wbc.csv')
pulses_rbc_files = glob.glob('*rbc.csv')

measures_table = pd.read_csv(measures[0], na_values = "?", comment='\t',
                              sep=",", skipinitialspace=True )

results_order = ["wbc","lynp","monp","midp","neup","eosp","rbc","hgb",
                 "hct","mcv","mch","mchc","rdw_cv","rdw_sd","plt",
                 "mpv","pct","pdw","plcr"]

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

identifiers = range(len(measures_table))
identifiers = identifiers + ["DP", "Media", "CV"]

measures_table.loc[len(measures_table)] = sds
measures_table.loc[len(measures_table)] = means
measures_table.loc[len(measures_table)] = cvs

measures_table.insert(0,"Exame",identifiers)
measures_table = measures_table.round(2)

xy = ["x","y"]

for plt_file in pulses_plt_files:
    histo_plt = [0] * 256
    pulses_plt = pd.read_csv(plt_file,na_values = "?", comment='\t', names=['x','y'],
                              sep=",", skipinitialspace=True)
    for i in pulses_plt['x']:
        histo_plt[i] = histo_plt[i] + 1
    plt.plot(histo_plt)

plt.xlabel('Amplitude de pulsos')
plt.ylabel('Quantidade')
plt.title('Histograma de plaquetas')
plt.savefig(results_path + '/histoplt.png')

plt.figure()

for wbc_file in pulses_wbc_files:
    histo_wbc = [0] * 256
    pulses_wbc = pd.read_csv(wbc_file,na_values = "?", comment='\t', names=['x','y'],
                              sep=",", skipinitialspace=True)
    for i in pulses_wbc['x']:
        histo_wbc[i] = histo_wbc[i] + 1
    plt.plot(histo_wbc)

plt.xlabel('Amplitude de pulsos')
plt.ylabel('Quantidade')
plt.title('Histograma de leucocitos')
plt.savefig(results_path + '/histowbc.png')
plt.figure()
for rbc_file in pulses_rbc_files:
    histo_rbc = [0] * 256
    pulses_rbc = pd.read_csv(rbc_file,na_values = "?", comment='\t', names=['x','y'],
                              sep=",", skipinitialspace=True)
    for i in pulses_rbc['x']:
        histo_rbc[i] = histo_rbc[i] + 1
    plt.plot(histo_wbc)

plt.xlabel('Amplitude de pulsos')
plt.ylabel('Quantidade')
plt.title('Histograma de eritrocitos')
plt.savefig(results_path + '/historbc.png')

indexing_limit = len(measures_table.T)
    
measures_table.to_csv(results_path + "/" + measures[0], index=False)


    
