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

import textwrap
import numpy as np
from .analog_pulse import AnalogPulse


class PulseGenerator():
    """ Pulse generator """

    def __init__(self, pulse_shape):
        """ Default constructor """
        self.pulse_shape = pulse_shape

        self.deformation_level = 0.0
        self.noise_mean = 0.0
        self.noise_sigma = 0.0
        self.pedestal = 0

        # amplitude distribution
        self.amplitude_generator = np.random.random_integers
        self.amplitude_generator_args = (0, 1023)

        # phase distribution
        self.phase_generator = np.random.random_integers
        self.phase_generator_args = (0, 0)

    @classmethod
    def from_yml(cls, yml, pulse_shape):
        """ Constructor from YML """
        instance = cls(pulse_shape)

        if yml["deformation_level"]:
            instance.set_deformation_level(yml["deformation_level"])
        if yml["noise_mean"]:
            instance.set_noise_params(mean=yml["noise_mean"])
        if yml["noise_sigma"]:
            instance.set_noise_params(sigma=yml["noise_sigma"])
        if yml["pedestal"]:
            instance.set_pedestal(yml["pedestal"])
        if yml["phase_generator"]:
            instance.set_phase_generator(random_function=getattr(np.random, yml["phase_generator"]))
        if yml["phase_params"]:
            instance.set_phase_generator(random_function_args=tuple(yml["phase_params"]))

        return instance

    def generate_pulse(self, **kwargs):
        """
        generate a random pulse
        """
        default_pulse_params = {
            "amplitude": self.__random_amplitude(),
            "deformation_level": self.deformation_level,
            "noise_mean": self.noise_mean,
            "noise_sigma": self.noise_sigma,
            "pedestal": self.pedestal,
            "phase": self.__random_phase(),
        }
        merged_pulse_params = {**default_pulse_params, **kwargs}
        return AnalogPulse(self.pulse_shape, **merged_pulse_params)

    def __random_amplitude(self):
        """
        generate a random amplitude
        """
        return self.amplitude_generator(*self.amplitude_generator_args)

    def __random_phase(self):
        """
        generate a random phase
        """
        return self.phase_generator(*self.phase_generator_args)

    def set_amplitude_generator(self, random_function, random_function_args):
        """
        set the random amplitude generator
        """
        self.amplitude_generator = random_function
        self.amplitude_generator_args = random_function_args

    def set_deformation_level(self, level):
        """
        set sigma ratio of gaussian deformation generator
        """
        self.deformation_level = level

    def set_noise_params(self, mean=None, sigma=None):
        """
        set gaussian noise mean and sigma
        """
        if mean is not None:
            self.noise_mean = mean
        if sigma is not None:
            self.noise_sigma = sigma

    def set_pedestal(self, pedestal):
        """
        set the baseline value
        """
        self.pedestal = pedestal

    def set_phase_generator(self, random_function=None, random_function_args=None):
        """
        set the random phase generator
        """
        if random_function is not None:
            self.phase_generator = random_function
        if random_function_args is not None:
            self.phase_generator_args = random_function_args

    def __str__(self):
        return textwrap.dedent(f"""\
          PulseGenerator:
            amplitude_generator = {self.amplitude_generator}
            amplitude_generator_args = {self.amplitude_generator_args}
            deformation_level = {self.deformation_level}
            noise_mean = {self.noise_mean}
            noise_sigma = {self.noise_sigma}
            pedestal = {self.pedestal}
            phase_generator = {self.phase_generator}
            phase_generator_args = {self.phase_generator_args}\
        """)
