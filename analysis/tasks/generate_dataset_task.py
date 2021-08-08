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
import os
import numpy as np
from ..generator import PulseShape, DatasetGenerator, PulseGenerator


class GenerateDatasetTask():
    """ Dataset Generator Task """

    def __init__(self, yml, output_path, logging):
        self.yml = yml
        self.output_file = output_path + "/dataset.csv"
        self.logging = logging
        self.pulse_shape = None
        self.pulse_generator = None
        self.dataset = None

        dataset_params = yml["setup"]["dataset_generator"]
        self.n_events = dataset_params["n_events"]
        self.pileup_luminosity = dataset_params["pileup_luminosity"]
        self.pileup_occupancy = dataset_params["pileup_occupancy"]
        self.sampling_rate = dataset_params["sampling_rate"]
        self.signal_pileup_ratio = dataset_params["signal_pileup_ratio"]
        self.window_size = dataset_params["window_size"]

    def perform(self):
        """ Call dataset generator """

        self.logging.info(textwrap.dedent(f"""\
          GenerateDatasetTasks:
            n_events = {self.n_events}
            pileup_luminosity = {self.pileup_luminosity}
            pileup_occupancy = {self.pileup_occupancy}
            sampling_rate = {self.sampling_rate}
            signal_pileup_ratio = {self.signal_pileup_ratio}
            window_size = {self.window_size}\
        """))


        if os.path.exists(self.output_file):
            self.logging.info(textwrap.dedent(f"""\
              GenerateDatasetTasks:
                Dataset already exists. Skipping!
                {self.output_file}\
            """))
            return

        self.__setup_pulse_shape()
        self.__setup_pulse_generator()
        self.__generate_dataset()
        self.__write_dataset_to_file()

        self.logging.info(textwrap.dedent(f"""\
          GenerateDatasetTasks:
            Dataset ready!
            {self.output_file}\
        """))

    def __setup_pulse_shape(self):
        self.pulse_shape = PulseShape.from_yml(self.yml["setup"]["pulse_shape"])
        self.logging.info(self.pulse_shape)

    def __setup_pulse_generator(self):
        self.pulse_generator = PulseGenerator.from_yml(self.yml["setup"]["pulse_generator"], self.pulse_shape)
        self.pulse_generator.set_amplitude_generator(np.random.exponential, (self.pileup_luminosity,))
        self.logging.info(self.pulse_generator)

    def __generate_dataset(self):
        dataset_generator = DatasetGenerator(self.pulse_generator)
        self.dataset, _ = dataset_generator.generate_windowed_samples(self.window_size, self.sampling_rate, self.n_events, self.pileup_occupancy)

    def __write_dataset_to_file(self):
        np.savetxt(self.output_file, self.dataset, delimiter=" ", fmt="%.5f")
