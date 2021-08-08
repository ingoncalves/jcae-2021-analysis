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
import matplotlib.pyplot as plt
from analysis.generator import AnalogPulse, PulseShape


def main():
    """
    main function
    """

    shape_path = "shared/unipolar-pulse-shape.dat"
    digital_samples_time = [-75.5, -50.0, -25.0, 0.0, 25.0, 50.0, 75.0]
    pulse_shape = PulseShape(shape_path, digital_samples_time)

    amplitude = 100.0

    default_pulse = AnalogPulse(
        pulse_shape=pulse_shape,
        amplitude=amplitude
    )
    print(default_pulse)
    plot_pulse(default_pulse, "default pulse")

    phased_pulse = AnalogPulse(
        pulse_shape=pulse_shape,
        amplitude=amplitude,
        phase=-25,
    )
    print(phased_pulse)
    plot_pulse(phased_pulse, "phased pulse")

    noisy_and_phased_pulse = AnalogPulse(
        pulse_shape=pulse_shape,
        amplitude=amplitude,
        phase=25,
        noise_mean=0,
        noise_sigma=1.5,
    )
    print(noisy_and_phased_pulse)
    plot_pulse(noisy_and_phased_pulse, "noisy and phased pulse")

    plt.grid(zorder=0, linestyle='--')
    plt.legend()
    plt.xlabel("time", horizontalalignment='right', x=1.0, zorder=3)
    plt.ylabel("ADC", horizontalalignment='right', y=1.0)
    plt.show()


def plot_pulse(pulse, label):
    """
    draw a pulse
    """
    time_series = list()
    sample_series = list()
    for time, sample in pulse:
        time_series.append(time)
        sample_series.append(sample)
    plot = plt.plot(time_series, sample_series, "-", label=label)
    plt.plot(pulse.pulse_shape.digital_samples_time, pulse.get_digital_samples(), ".",
             color=plot[0].get_color(),
             markersize=10,
             markeredgewidth=1.5,
             markeredgecolor="black")


if __name__ == '__main__':
    main()
