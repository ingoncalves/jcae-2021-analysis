"""
            MASTERS ANALYSIS

Bernardo S. Peralva    <bernardo@iprj.uerj.br>
Guilherme I. Goncalves <ggoncalves@iprj.uerj.br>

Copyright (C) 2021 Bernardo & Guilherme

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from analysis.filters import MAE


def main():
    """
    main function
    """

    dataset_file = "./cases/plpocc0.0_plplumi30.0_snr3_phase1nsUni_tilecal/results_signals.csv"
    truth_amplitudes_file = "./cases/plpocc0.0_plplumi30.0_snr3_phase1nsUni_tilecal/results_amplitude_truth.csv"

    dataset          = np.loadtxt(dataset_file, delimiter=',')
    truth_amplitudes = np.loadtxt(truth_amplitudes_file)
    mae              = MAE(threshold=4.5)
    mae_error        = np.zeros(len(dataset))

    for i in range(len(dataset)):
        signal = dataset[i]
        truth_amplitude = truth_amplitudes[i]
        mae_amplitude = mae.apply(signal)[3]
        mae_error[i] = (mae_amplitude - truth_amplitude) / 12.0

    print(f"Mean = {np.mean(mae_error)}")
    print(f"RSM  = {np.std(mae_error)}")

    kwargs = dict(bins=50)
    plt.hist(mae_error, **kwargs)
    plt.title("First Sample of Dataset")
    plt.xlabel("Energy (ADC)")
    plt.ylabel("Events")
    plt.yscale('log')
    plt.show()


if __name__ == '__main__':
    main()
