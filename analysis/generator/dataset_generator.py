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

import numpy as np
from progress.bar import Bar


class DatasetGenerator():
    """ Dataset generator """

    def __init__(self, pulse_generator):
        """ Default constructor """
        self.pulse_generator = pulse_generator
        self.pulse_shape = pulse_generator.pulse_shape

    def generate_samples(self, n_events, sampling_rate, occupancy=0):
        """
        generate samples
        """
        samples = self.__random_noise(n_events) + self.pulse_generator.pedestal
        amplitudes = np.zeros(n_events)
        bunch_interval = int(sampling_rate / self.pulse_shape.resolution)

        progress_bar = Bar('Generating dataset', max=int(n_events/bunch_interval), suffix='%(percent).1f%% - %(eta)ds')

        for i in range(0, n_events, bunch_interval):
            signal_occurency_probability = np.random.uniform()
            if signal_occurency_probability < occupancy:
                pulse = self.pulse_generator.generate_pulse(pedestal=0, noise_mean=0, noise_sigma=0)
                amplitudes[i] = pulse.amplitude

                for j, (_, pulse_sample) in enumerate(pulse):
                    offset = j - self.pulse_shape.time_origin_index

                    # skip out of bound index
                    if offset < 0 and i < (-1 * offset):
                        continue
                    if i >= (n_events - offset):
                        continue

                    samples[i + offset] += pulse_sample
            progress_bar.next()

        progress_bar.finish()
        return (samples, amplitudes)

    def generate_windowed_samples(self, window_size, sampling_rate, n_events, occupancy):
        """
        generate segmented samples
        """
        time_resolution = self.pulse_shape.resolution
        total_length = int((window_size * n_events * sampling_rate) / time_resolution)

        raw_samples, raw_amplitudes = self.generate_samples(total_length, sampling_rate, occupancy)
        sampled_samples = self.__sample_list(raw_samples, time_resolution, sampling_rate)
        sampled_amplitudes = self.__sample_list(raw_amplitudes, time_resolution, sampling_rate)

        windowed_samples = np.array(np.split(sampled_samples, n_events))
        windowed_amplitudes = np.array(np.split(sampled_amplitudes, n_events))

        return (windowed_samples, windowed_amplitudes)

    def __sample_list(self, raw_list, time_resolution, sampling_rate):
        interval = int(sampling_rate / time_resolution)
        return raw_list[0::interval]

    def __random_noise(self, n_events):
        """
        generate a random noise
        """
        mean = self.pulse_generator.noise_mean
        sigma = self.pulse_generator.noise_sigma
        return np.random.normal(mean, sigma, n_events)
