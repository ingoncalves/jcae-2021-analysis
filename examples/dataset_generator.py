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
import numpy as np
import matplotlib.pyplot as plt
from analysis.generator import PulseShape, PulseGenerator, DatasetGenerator


def main():
    """
    main function
    """
    n_events = 10000
    pileup_luminosity = 100.0
    pileup_occupancy = 0.05

    # generate pulse
    pulse_generator = __setup_pulse_generator(pileup_luminosity)

    # setup dataset
    dataset, amplitudes = __setup_dataset(pulse_generator, n_events, pileup_occupancy)

    plt.grid(zorder=0, linestyle='--')
    plt.plot(range(0, n_events), dataset, ".-", label="samples")

    y_amplitudes = amplitudes[amplitudes > 0] + pulse_generator.pedestal
    x_amplitudes = np.array(range(0, n_events))[amplitudes > 0]
    plt.plot(x_amplitudes, y_amplitudes, ".", label="amplitudes")

    plt.legend()
    plt.xlabel("time", horizontalalignment='right', x=1.0, zorder=3)
    plt.ylabel("ADC", horizontalalignment='right', y=1.0)
    plt.show()


def __setup_pulse_generator(pileup_luminosity):
    shape_path = "shared/cern-atlas-tilecalorimeter-pulse-shape.dat"
    pulse_shape = PulseShape(shape_path)
    pulse_generator = PulseGenerator(pulse_shape)
    pulse_generator.set_amplitude_generator(np.random.exponential, (pileup_luminosity,))
    pulse_generator.set_deformation_level(0.01)
    pulse_generator.set_noise_params(0, 1.5)
    pulse_generator.set_pedestal(50)
    pulse_generator.set_phase_generator(np.random.random_integers, (-5, 5))
    return pulse_generator


def __setup_dataset(pulse_generator, n_events, pileup_occupancy):
    sampling_rate = 25.0
    dataset_generator = DatasetGenerator(pulse_generator)
    dataset, amplitudes = dataset_generator.generate_samples(
        n_events, sampling_rate, pileup_occupancy)
    return (dataset, amplitudes)


if __name__ == '__main__':
    main()
