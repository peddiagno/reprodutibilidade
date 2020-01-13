import matplotlib.pyplot as plt
import pandas as pd

def create_histogram(pulse_files, exam_type, basename, save_directory):
    plt.figure(figsize=(16, 12))
    for pulse_file in pulse_files:
        histo = [0] * 256
        pulses = pd.read_csv(pulse_file,na_values = "?", comment='\t', names=['y','x'],
                              sep=",", skipinitialspace=True)
        for i in pulses['x']:
            histo[i] = histo[i] + 1
        plt.plot(histo,linewidth=2)

    plt.xlabel('Amplitude de pulsos')
    plt.ylabel('Quantidade')
    plt.title('Histograma {}'.format(exam_type))
    plt.savefig(save_directory + basename +'histo{}.png'.format(exam_type))
