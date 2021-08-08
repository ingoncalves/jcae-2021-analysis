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
from analysis.generator import PulseShape, PulseGenerator, DatasetGenerator


def main():
    """
    main function
    """

    window_size = 7
    n_samples = 1000
    sampling_rate = 25.0
    pileup_occupancy = 0.5
    pileup_luminosity = 100.0
    noise_mean = 1.5
    noise_std = 1.5
    deformation_level = 0

    # generate pulse
    shape_path = "shared/unipolar-pulse-shape.dat"
    pulse_shape = PulseShape(shape_path)
    pulse_generator = PulseGenerator(pulse_shape)
    pulse_generator.set_deformation_level(deformation_level)
    pulse_generator.set_noise_params(noise_mean, noise_std)

    # setup dataset
    pulse_generator.set_amplitude_generator(np.random.exponential, (pileup_luminosity,))
    dataset_generator = DatasetGenerator(pulse_generator)
    samples, _ = dataset_generator.generate_windowed_samples(window_size, sampling_rate, n_samples, pileup_occupancy)

    first_samples = [row[0] for row in samples]

    kwargs = dict(bins=50)
    plt.hist(first_samples, **kwargs)
    plt.title("First Sample of Dataset")
    plt.xlabel("Energy (ADC)")
    plt.ylabel("Frequency")
    plt.show()


if __name__ == '__main__':
    main()
