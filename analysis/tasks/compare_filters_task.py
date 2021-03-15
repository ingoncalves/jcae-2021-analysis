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
from ..filters import OF2, COF, Wiener, Sparse, SparseCOF
from ..generator import DatasetGenerator, PulseGenerator


class CompareJob():
    """ Compare Job """

    def __init__(self, params, log):
        self.params = params
        self.log = log

    def perform(self):
        """
        perform
        """
        log = self.log
        params = self.params

        pileup_occupancy = params["pileup_occupancy"]
        signal_pileup_ratio = params["signal_pileup_ratio"]

        # pileup_luminosity = params["pileup_luminosity"]
        # signal_luminosity = pileup_luminosity * signal_pileup_ratio

        signal_luminosity = params["pileup_luminosity"]
        pileup_luminosity = signal_luminosity / signal_pileup_ratio

        n_events = params["n_events"]

        init_message = f"Processing"
        init_message += f" pileup_luminosity={pileup_luminosity}"
        init_message += f" pileup_occupancy={pileup_occupancy}"
        init_message += f" signal_pileup_ratio={signal_pileup_ratio}"
        init_message += f" n_events={n_events}"
        log.info(init_message)

        # generate pulse
        pulse_generator = self.setup_pulse_generator(log, params["pulse_generator"])

        # setup dataset
        train_dataset, test_dataset = self.setup_dataset(
            log, params["dataset_generator"], pulse_generator, pileup_luminosity, pileup_occupancy, n_events)

        # setup filters
        filters = self.setup_filters(log, pulse_generator,
                                  train_dataset, signal_luminosity)

        # perform estimations
        buffer = self.perform_estimations(
            log, pulse_generator, test_dataset, filters, signal_luminosity)

        return self.build_result(buffer, params)


    def setup_pulse_generator(self, log, params):
        pulse_size = params["pulse_size"]
        shaper_path = params["shaper_path"]
        deformation_level = params["deformation_level"]
        phase_params = params["phase_params"]

        debug_message = "Setup PulseGenerator with"
        debug_message += f" pulse_size={pulse_size}"
        debug_message += f" shaper_path={shaper_path}"
        debug_message += f" deformation_level={deformation_level}"
        debug_message += f" phase_params={phase_params}"
        log.debug(debug_message)

        pulse_generator = PulseGenerator(pulse_size, shaper_path)
        pulse_generator.set_deformation_level(deformation_level)
        pulse_generator.set_phase_generator(
            np.random.random_integers, tuple(phase_params))

        return pulse_generator


    def setup_dataset(self, log, params, pulse_generator, pileup_luminosity, pileup_occupancy, n_events):
        noise_params = params["noise_params"]

        debug_message = "Setup DatasetGenerator with"
        debug_message += f" noise_params={noise_params}"
        log.debug(debug_message)

        # use exponential distribution
        pulse_generator.set_amplitude_generator(
            np.random.exponential, (pileup_luminosity,))

        dataset_generator = DatasetGenerator(pulse_generator)
        dataset_generator.set_noise_params(noise_params[0], noise_params[1])

        dataset, _ = dataset_generator.generate_windowed_samples(
            pulse_generator.pulse_size, n_events, pileup_occupancy)
        [train_dataset, test_dataset] = np.split(dataset, 2)

        np.savetxt("train_dataset.csv", train_dataset, delimiter=" ", fmt="%.5f")

        log.debug("Dataset ready")
        return (train_dataset, test_dataset)


    def setup_filters(self, log, pulse_generator, train_dataset, signal_luminosity):
        log.debug("Initializing filters")

        # setup generator to design filters using uniform distribution
        pulse_generator.set_amplitude_generator(
            np.random.random_integers, (0, 1023))

        filters = {
            "OF2": OF2(),
            "COF": COF(threshold=4.5),
            # "SPR": Sparse(),
            # "SCF": SparseCOF(),
            "WHF": Wiener(train_dataset, pulse_generator)
        }

        log.debug("Filters ready")
        return filters


    def perform_estimations(self, log, pulse_generator, test_dataset, filters, signal_luminosity):
        log.debug("Initializing performance test")

        # setup generator to perform the comparison
        # using exponential distribution
        pulse_generator.set_amplitude_generator(
            np.random.exponential, (signal_luminosity,))

        buffer = {}
        for key in filters:
            buffer[key] = np.zeros(len(test_dataset))

        for i in range(len(test_dataset)):
            signal, amplitude = self.generate_signal(
                pulse_generator, test_dataset[i, :])
            for key in filters:
                estimation = filters[key].apply(signal)
                error = estimation - amplitude
                buffer[key][i] = error

        log.debug("Performance test done")
        return buffer


    def generate_signal(self, pulse_generator, noise):
        pulse, amplitude, _ = pulse_generator.generate_pulse()
        signal = pulse + noise
        return (signal, amplitude)


    def build_result(self, buffer, params):
        # get mean and std for each filter
        pileup_luminosity = params["pileup_luminosity"]
        pileup_occupancy = params["pileup_occupancy"]
        signal_pileup_ratio = params["signal_pileup_ratio"]
        phase_params = params["pulse_generator"]["phase_params"]
        phase_module = phase_params[1]

        result = []
        for key in buffer:
            data = buffer[key]
            mean = np.mean(data)
            std = np.std(data)
            result.append({
                "filter": key,
                "pileup_luminosity": pileup_luminosity,
                "pileup_occupancy": pileup_occupancy,
                "signal_pileup_ratio": signal_pileup_ratio,
                "phase_module": phase_module,
                "mean": mean,
                "std": std,
                "data": data,
            })

        return result
