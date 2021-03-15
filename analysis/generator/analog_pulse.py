"""
            MASTERS ANALYSIS

Bernardo S. Peralva    <bernardo@iprj.uerj.br>
Guilherme I. Goncalves <ggoncalves@iprj.uerj.br>

Copyright (C) 2019 Bernardo & Guilherme

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

import textwrap
import numpy as np


class AnalogPulse():
    """ Analog Pulse model """

    def __init__(self, pulse_shape, amplitude=1.0, phase=0, noise_mean=0.0, noise_sigma=0.0, pedestal=0.0, deformation_level=0.0):
        self.pulse_shape = pulse_shape
        self.amplitude = amplitude
        self.phase = phase
        self.noise_mean = noise_mean
        self.noise_sigma = noise_sigma
        self.pedestal = pedestal
        self.deformation_level = deformation_level
        self.__i = 0

    def get_sample(self, index):
        """
        get a sample by index
        """
        shape_sample = self.pulse_shape.shape[index]
        deformation = self.__random_deformation(shape_sample)
        noise = self.__random_noise()
        sample = self.amplitude * (shape_sample + deformation) + self.pedestal + noise
        return sample

    def with_phase(self, phase):
        """
        returns an iterator of samples with a phase deviation
        """
        self.phase = phase
        return iter(self)

    def __iter__(self):
        self.__i = 0
        return self

    def __next__(self):
        if self.__i < self.pulse_shape.size:
            time_index = self.__i
            sample_index = self.__index_with_phase_deviation(time_index)
            self.__i += 1

            if sample_index < 0 or sample_index >= self.pulse_shape.size:
                return self.__next__()

            # sample
            sample = self.get_sample(sample_index)

            # time
            time = self.pulse_shape.time[time_index]

            return (time, sample)

        raise StopIteration

    def __index_with_phase_deviation(self, time_index):
        phase_index_offset = int(self.phase / self.pulse_shape.resolution)
        index_with_phase_devitation = time_index - phase_index_offset
        return index_with_phase_devitation

    def __random_deformation(self, shape_sample):
        """
        generate a random deformation
        """
        if self.deformation_level == 0:
            return 0

        sigma = self.deformation_level * abs(shape_sample)
        return np.random.normal(0, sigma)

    def __random_noise(self):
        """
        generate a random gaussian noise
        """
        if self.noise_mean == 0 and self.noise_sigma == 0:
            return 0

        return np.random.normal(self.noise_mean, self.noise_sigma)

    def __str__(self):
        return textwrap.dedent(f"""\
          AnalogPulse:
            amplitude = {self.amplitude}
            deformation_level = {self.deformation_level}
            noise_mean = {self.noise_mean}
            noise_sigma = {self.noise_sigma}
            pedestal = {self.pedestal}
            phase = {self.phase}
            resolution = {self.pulse_shape.resolution}
            size = {self.pulse_shape.size}\
        """)
