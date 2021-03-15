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

import os

def get_static_path(filename):
    """ build path of any static file within this project """
    return os.path.join(os.path.dirname(__file__), "../", filename)

def get_data_path(filename):
    """ build path of data file """
    return os.path.join(DATA_PATH, filename)

def get_filter_name(label):
    """ get filter name by label """
    return ({
        "OF2": "OF2",
        "COF": "COF",
        "SPR": "Sparse",
        "SCF": "Sparse COF",
        "WHF": "Wiener"
    })[label]

# number constants
PULSE_SIZE = 7

# path constants
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "../out")
SHAPER_PATH = get_static_path("shared/cern-atlas-tilecalorimeter-pulse-shape.dat")
