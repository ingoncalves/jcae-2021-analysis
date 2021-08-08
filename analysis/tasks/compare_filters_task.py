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
import csv
import os
import numpy as np
from ..filters import Blue, OF2, MAE, Wiener
from ..generator import PulseShape, PulseGenerator


class CompareFiltersTask():
    """ Compare Job """

    def __init__(self, yml, output_path, logging):
        self.yml = yml
        self.output_path = output_path
        self.logging = logging
        self.pulse_shape = None
        self.pulse_generator = None
        self.train_dataset = None
        self.test_dataset = None
        self.filters = None
        self.results_buffer = None

    def perform(self):
        """ perform """

        self.__read_dataset()
        self.__setup_pulse_shape()
        self.__setup_pulse_simulator()
        self.__setup_filters()
        self.__start_performance_test()
        self.__build_results()

    def __read_dataset(self):
        dataset_file = self.output_path + "/dataset.csv"
        if not os.path.exists(dataset_file):
            raise "Dataset file does not exist"

        dataset = np.loadtxt(dataset_file)
        [self.train_dataset, self.test_dataset] = np.split(dataset, 2)

        self.logging.info(textwrap.dedent(f"""\
          Dataset loaded:
            {dataset_file}\
        """))

    def __setup_pulse_shape(self):
        self.pulse_shape = PulseShape.from_yml(self.yml["setup"]["pulse_shape"])
        self.logging.info(self.pulse_shape)

    def __setup_pulse_simulator(self):
        self.pulse_generator = PulseGenerator.from_yml(self.yml["setup"]["pulse_generator"], self.pulse_shape)
        self.logging.info(self.pulse_generator)

    def __setup_filters(self):
        self.logging.info("Initializing filters")

        # setup generator to design the Wiener filter
        wiener_pulse_generator = PulseGenerator.from_yml(self.yml["setup"]["filters"]["wiener"]["pulse_generator"], self.pulse_shape)
        self.logging.info("Wiener Pulse Generator")
        self.logging.info(wiener_pulse_generator)

        self.filters = {
            "BLUE": Blue(),
            "BLUECOV": Blue(self.train_dataset),
            "OF2": OF2(),
            "OF2COV": OF2(self.train_dataset),
            "MAE": MAE(threshold=self.yml["setup"]["filters"]["mae"]["threshold"]),
            "WHF": Wiener(self.train_dataset, wiener_pulse_generator)
        }

        for key in self.filters:
            self.logging.info(self.filters[key])

        self.logging.debug("Filters ready")


    def __start_performance_test(self):
        self.logging.info("Initializing performance test")

        dataset_params = self.yml["setup"]["dataset_generator"]
        signal_pileup_ratio = dataset_params["signal_pileup_ratio"]
        pileup_luminosity = dataset_params["pileup_luminosity"]
        signal_luminosity = pileup_luminosity * signal_pileup_ratio

        # setup generator to perform the comparison
        # using exponential distribution
        self.pulse_generator.set_amplitude_generator(np.random.exponential, (signal_luminosity,))

        buffer = {
            "amplitude_estimated": {},
            "signal": np.zeros((len(self.test_dataset), 7)),
            "amplitude_truth": np.zeros(len(self.test_dataset)),
            "phase_truth": np.zeros(len(self.test_dataset)),
        }
        for key in self.filters:
            buffer["amplitude_estimated"][key] = []

        for i in range(len(self.test_dataset)):
            analog_pulse = self.pulse_generator.generate_pulse()
            digital_samples = analog_pulse.get_digital_samples()

            amplitude = analog_pulse.amplitude
            phase = analog_pulse.phase

            buffer["amplitude_truth"][i] = amplitude
            buffer["phase_truth"][i] = phase

            signal = digital_samples + self.train_dataset[i, :]
            buffer["signal"][i] = signal

            for key in self.filters:
                amplitude_estimated = self.filters[key].apply(signal)
                buffer["amplitude_estimated"][key].append(amplitude_estimated)

        self.logging.info("Performance test finished")
        self.results_buffer = buffer


    def __build_results(self):
        self.__write_csv_file("results_filter_weights_blue.csv", self.filters["BLUE"].weights)
        self.__write_csv_file("results_filter_weights_bluecov.csv", self.filters["BLUECOV"].weights)
        self.__write_csv_file("results_filter_weights_of2.csv", self.filters["OF2"].weights)
        self.__write_csv_file("results_filter_weights_of2cov.csv", self.filters["OF2COV"].weights)
        self.__write_csv_file("results_filter_weights_wiener.csv", self.filters["WHF"].weights)
        self.__write_csv_file("results_amplitude_truth.csv", self.results_buffer["amplitude_truth"])
        self.__write_csv_file("results_phase_truth.csv", self.results_buffer["phase_truth"])
        self.__write_csv_file("results_signals.csv", self.results_buffer["signal"])
        for key in self.filters:
            self.__write_csv_file(f"results_amplitude_estimated_{key.lower()}.csv", self.results_buffer["amplitude_estimated"][key])


    def __write_csv_file(self, filename, data):
        output_file = f"{self.output_path}/{filename}"
        with open(output_file, mode='w') as outcsv:
            writer = csv.writer(outcsv)
            for value in data:
                row = np.asarray(value) if type(value) is np.ndarray else [value]
                writer.writerow(row)

        self.logging.info(textwrap.dedent(f"""\
          CompareFiltersTask:
            Output file ready!
            {output_file}\
        """))
