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

from textwrap import dedent
import numpy as np
from .base import FilterBase


class MAE(FilterBase):
    """ MAE filter """

    def __init__(self, threshold=3.0):
        super().__init__(7)

        # pileup pulse shape
        # pylint: disable=bad-whitespace
        self.mat_h = np.array([
            [1.0000, 0.5633, 0.1493, 0.0424, 0.,     0.,     0.    ], # nopep8
            [0.4524, 1.0000, 0.5633, 0.1493, 0.0424, 0.,     0.    ], # nopep8
            [0.0172, 0.4524, 1.0000, 0.5633, 0.1493, 0.0424, 0.    ], # nopep8
            [0.,     0.0172, 0.4524, 1.0000, 0.5633, 0.1493, 0.0424], # nopep8
            [0.,     0.,     0.0172, 0.4524, 1.0000, 0.5633, 0.1493], # nopep8
            [0.,     0.,     0.,     0.0172, 0.4524, 1.0000, 0.5633], # nopep8
            [0.,     0.,     0.,     0.,     0.0172, 0.4524, 1.0000]  # nopep8
        ])
        # pylint: enable=bad-whitespace

        self.mat_h_inv = np.linalg.inv(self.mat_h)
        self.centered_sample = 3
        self.threshold = threshold

    def apply(self, pulse, ped=0.):
        if pulse.size != self.filter_size:
            raise "Incompatible input size"

        # substracts the pedestal from the input signal
        no_ped_pulse = pulse - ped

        # projects the filter for each input
        weights, selected_samples = self.project_filter_weights(
            no_ped_pulse)

        # estimate amplitudes
        vec_amplitudes = np.dot(no_ped_pulse.T, weights.T)

        # build output vector
        j = 0
        vec_output = np.zeros(self.filter_size)
        for i in range(0, self.filter_size):
            if selected_samples[i] == 1:
                vec_output[i] = vec_amplitudes[j]
                j = j + 1

        return vec_output

    def project_filter_weights(self, pulse):
        """
        calculates the MAE weights
        """

        # selects samples of interest
        vec_selected_samples = np.zeros(self.filter_size)
        vec_selected_samples[self.centered_sample] = 1
        selected_samples_count = 1

        vec_dm = np.dot(pulse.T, self.mat_h_inv)
        for i in range(self.filter_size):
            if i == self.centered_sample:
                continue
            if vec_dm[i] > self.threshold:
                vec_selected_samples[i] = 1
                selected_samples_count = selected_samples_count + 1

        # projects the weights matrix
        count = 0
        target_amplitude_index = -1
        mat_d = np.zeros((selected_samples_count, self.filter_size))
        for i in range(self.filter_size):
            if vec_selected_samples[i] == 1:
                if i == self.centered_sample:
                    target_amplitude_index = count
                mat_d[count] = self.mat_h[i, :]
                count = count + 1

        mat_aux = np.dot(mat_d, mat_d.T)
        weights = np.linalg.solve(mat_aux, mat_d)

        return weights, vec_selected_samples

    def __str__(self):
        return dedent(f"""\
          MAE Filter:
            centered_sample = {self.centered_sample}
            threshold = {self.threshold}
            size = {self.filter_size}\
        """)
