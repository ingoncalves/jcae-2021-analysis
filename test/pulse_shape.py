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
import matplotlib.pyplot as plt
from analysis.generator import PulseShape


def main():
    """
    main function
    """

    # shape_path = "shared/cern-atlas-tilecalorimeter-pulse-shape.dat"
    shape_path = "/Users/guilherme/Downloads/TileCalorimeter_TileConditions_share_pulselo_physics.dat"
    digital_samples_time = [-75.5, -50.0, -25.0, 0.0, 25.0, 50.0, 75.0]
    pulse_shape = PulseShape(shape_path, digital_samples_time)


    # plot pulse shape
    plt.plot(pulse_shape.time, pulse_shape.shape, ".-", label="pulse shape")

    # plot digital samples
    digital_samples = [pulse_shape.shape[time] for time in pulse_shape.digital_samples_index]
    plt.plot(pulse_shape.digital_samples_time, digital_samples, ".", label="digital samples")

    plt.grid(zorder=0, linestyle='--')
    plt.xlabel("time", horizontalalignment='right', x=1.0, zorder=3)
    plt.ylabel("ADC", horizontalalignment='right', y=1.0)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
