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
import os
import numpy as np
from ..generator import PulseShape, DatasetGenerator, PulseGenerator


def generate_dataset_task(yml, output_path, logging):
    output_file = output_path + "/dataset.csv"
    if os.path.exists(output_file):
        logging.info(textwrap.dedent(f"""\
          GenerateDatasetTasks:
            Dataset already exists. Skipping!
            {output_file}\
        """))
        return

    dataset_params = yml["setup"]["dataset_generator"]
    n_events = dataset_params["n_events"]
    pileup_luminosity = dataset_params["pileup_luminosity"]
    pileup_occupancy = dataset_params["pileup_occupancy"]
    sampling_rate = dataset_params["sampling_rate"]
    signal_pileup_ratio = dataset_params["signal_pileup_ratio"]
    window_size = dataset_params["window_size"]

    pulse_shape = PulseShape.from_yml(yml["setup"]["pulse_shape"])
    logging.info(pulse_shape)

    pulse_generator = PulseGenerator.from_yml(
        yml["setup"]["pulse_generator"], pulse_shape)
    pulse_generator.set_amplitude_generator(
        np.random.exponential, (pileup_luminosity,))
    logging.info(pulse_generator)

    dataset_generator = DatasetGenerator(pulse_generator)
    logging.info(textwrap.dedent(f"""\
      GenerateDatasetTasks:
        n_events = {n_events}
        pileup_luminosity = {pileup_luminosity}
        pileup_occupancy = {pileup_occupancy}
        sampling_rate = {sampling_rate}
        signal_pileup_ratio = {signal_pileup_ratio}
        window_size = {window_size}\
    """))

    dataset, _ = dataset_generator.generate_windowed_samples(
        window_size, sampling_rate, n_events, pileup_occupancy)

    np.savetxt(output_file, dataset, delimiter=" ", fmt="%.5f")
    logging.debug("Dataset ready")
