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

class PulseShape():
    """ Pulse generator """

    def __init__(self, shape_path):
        """ Default constructor """
        self.shape_path = shape_path
        self.read_pulse_shape()

    @classmethod
    def from_yml(cls, yml):
        """ Constructor from YML """
        instance = cls(yml["path"])
        return instance

    def read_pulse_shape(self):
        """
        read pulse shape file
        """
        input_data = np.loadtxt(self.shape_path)

        # shape values
        self.shape = input_data[:, 1]
        self.size = len(self.shape)

        # timing properties
        self.time = input_data[:, 0]
        self.time_origin_index = int(np.where(self.time == .0)[0][0])
        self.resolution = self.time[1] - self.time[0]
