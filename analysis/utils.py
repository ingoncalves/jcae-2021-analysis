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
import logging
import json
import numpy as np
import yaml


def print_matrix(matrix, precision=2):
    """ prints a numpy matrix """
    np.set_printoptions(precision=precision)
    for row in matrix:
        for cell in row:
            print("{0:0.2f}".format(cell), end=" ")
        print("")


def read_yaml_file(filepath):
    """ reads and parse an yaml file """
    success = False
    data = None
    with open(filepath, "r") as stream:
        try:
            data = yaml.safe_load(stream)
            success = True
        except yaml.YAMLError as exc:
            logging.error(exc)
    return success, data


def get_file_name(filepath):
    """ get filename without path and extension """
    return os.path.splitext(os.path.basename(filepath))[0]

def write_json_file(filepath, data):
    """ parses and writes data to json file """
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)
