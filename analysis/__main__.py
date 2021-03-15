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
import sys
import os
import logging
import time
from .utils import read_yaml_file
from .tasks import generate_dataset_task


def main():
    """
    main function
    """

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print("Input file does not exist")
        sys.exit(1)

    output_path = os.path.dirname(os.path.abspath(input_file))

    logging.basicConfig(
        format='%(asctime)s %(process)s %(levelname)s %(name)s %(message)s',
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(output_path + '/debug.log'),
            logging.StreamHandler()
        ]
    )

    logging.info('Starting analysis')
    start_time = time.time()

    logging.info("Input: %s", input_file)
    logging.info("Output: %s", output_path)

    _, yml = read_yaml_file(input_file)
    generate_dataset_task(yml, output_path, logging)

    elapsed_time = time.time() - start_time
    logging.info("Task finished after %d seconds", elapsed_time)

    sys.exit(0)


if __name__ == '__main__':
    main()
