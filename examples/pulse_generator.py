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
import matplotlib.pyplot as plt
from analysis.generator import PulseGenerator, PulseShape


def main():
    """
    main function
    """

    shape_path = "shared/unipolar-pulse-shape.dat"
    pulse_shape = PulseShape(shape_path)

    pulse_generator = PulseGenerator(pulse_shape)
    pulse_generator.set_amplitude_generator(np.random.random_integers, (0, 800))
    pulse_generator.set_deformation_level(0.01)
    pulse_generator.set_noise_params(0, 1.5)
    pulse_generator.set_pedestal(40)
    pulse_generator.set_phase_generator(np.random.random_integers, (-5, 5))

    analog_pulse = pulse_generator.generate_pulse(pedestal=20)
    print(analog_pulse)

    time_series = list()
    sample_series = list()
    for time, sample in analog_pulse:
        time_series.append(time)
        sample_series.append(sample)

    plt.grid(zorder=0, linestyle="--")
    plt.plot(time_series, sample_series, ".", label="pulse")
    plt.plot(pulse_shape.time, pulse_shape.shape *
             analog_pulse.amplitude, "-", label="shape")

    plt.annotate(analog_pulse, xy=(0.6, 0.5), xycoords="axes fraction")

    plt.legend()
    plt.xlabel("time", horizontalalignment="right", x=1.0, zorder=3)
    plt.ylabel("ADC", horizontalalignment="right", y=1.0)
    plt.show()


if __name__ == '__main__':
    main()
