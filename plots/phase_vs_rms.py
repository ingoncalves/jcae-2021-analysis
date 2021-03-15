"""
            MASTERS ANALYSIS

Bernardo S. Peralva    <bernardo@iprj.uerj.br>
Guilherme I. Gonçalves <ggoncalves@iprj.uerj.br>

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

import sys
import os
import json

from .commom import plot_summary, plot_job_histograms


def main():
    """ create plots """
    input_folder = sys.argv[1]

    params_filepath = os.path.join(input_folder, "params.json")
    with open(params_filepath) as params_file:
        params = json.load(params_file)

        __plot_histograms(input_folder, params)
        __plot_phase_vs_rms(input_folder)


def __plot_phase_vs_rms(folder):
    output_file = "phase_vs_rms.pdf"
    x_field = "phase_module"
    x_label = "Phase Module (ADC)"
    y_field = "std"
    y_label = "Estimation Error RMS (MeV)"
    plot_summary(folder, output_file, x_field, x_label, y_field, y_label)


def __plot_histograms(folder, params):
    def __title_builder(job):
        phase = job["pulse_generator"]["phase_params"]
        return f"Filters Efficiency With Phase [{phase[0]}, {phase[1]}] nanoseconds"
    plot_job_histograms(folder, params, __title_builder)


if __name__ == "__main__":
    main()
