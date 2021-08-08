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
import matplotlib.ticker as tck
import numpy as np
from analysis.generator import AnalogPulse, PulseShape


def main():
    """
    main function
    """
    _, axis = plt.subplots()

    shape_path = "shared/unipolar-pulse-shape.dat"
    digital_samples_time = [-75.5, -50.0, -25.0, 0.0, 25.0, 50.0, 75.0]
    pulse_shape = PulseShape(shape_path, digital_samples_time)
    amplitude = 1

    default_pulse = AnalogPulse(
        pulse_shape=pulse_shape,
        amplitude=amplitude
    )
    print(default_pulse)
    plot_pulse(default_pulse, "signal of interest", "black")

    phased_pulse = AnalogPulse(
        pulse_shape=pulse_shape,
        amplitude=amplitude,
        phase=50,
    )
    print(phased_pulse)
    plot_pulse(phased_pulse, "signal pile-up", "red")

    plot_sum_of_pulses(default_pulse, phased_pulse, "readout signal", "blue")

    axis.xaxis.set_minor_locator(tck.AutoMinorLocator())
    axis.yaxis.set_minor_locator(tck.AutoMinorLocator())
    axis.xaxis.set_tick_params(which='both', direction='in', top=True, bottom=True)
    axis.yaxis.set_tick_params(which='both', direction='in', left=True, right=True)

    plt.grid(zorder=0, linestyle='dotted', color="grey")
    plt.xlabel("Time (ns)", horizontalalignment='right', x=1.0, zorder=3)
    plt.ylabel("ADC Units", horizontalalignment='right', y=1.0)
    plt.legend()
    plt.show()


def plot_pulse(pulse, label, color):
    """
    draw a pulse
    """
    time_series = list()
    sample_series = list()
    for time, sample in pulse:
        time_series.append(time)
        sample_series.append(sample)
    plot = plt.plot(time_series, sample_series, "-", label=label, color=color)
    plt.plot(pulse.pulse_shape.digital_samples_time, pulse.get_digital_samples(), ".",
             color=plot[0].get_color(),
             markersize=10)

def plot_sum_of_pulses(pulse_a, pulse_b, label, color):
    """
    draw a pulse
    """
    time_series = [time for time,_ in pulse_a]
    samples_a = np.array([sample for _, sample in pulse_a])
    samples_b = np.array([sample for _, sample in pulse_b])
    pulses_sum = samples_a + samples_b 
    plt.plot(time_series, pulses_sum, "-", label=label, color=color)

    digital_samples = [pulses_sum[time_index] for time_index in pulse_a.pulse_shape.digital_samples_index]
    plt.plot(pulse_a.pulse_shape.digital_samples_time, digital_samples, ".",
             color=color,
             markersize=10)

if __name__ == '__main__':
    main()
