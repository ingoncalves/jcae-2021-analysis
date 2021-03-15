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
from .jobs import compare_filters

logging.basicConfig(
    format='%(asctime)s %(process)s %(levelname)s %(name)s %(message)s',
    level=logging.DEBUG,
)


def main():
    """
    main function
    """
    start_time = time.time()
    logging.info('Starting analysis')

    input_file = sys.argv[1]
    logging.info("Input: %s", input_file)

    output_file = None
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    if not os.path.exists(input_file):
        logging.error("Input file does not exist")
        sys.exit(1)

    result = compare_filters(input_file, output_file)

    elapsed_time = time.time() - start_time
    logging.info("Analysis finished after %d seconds", elapsed_time)
    logging.info("Output: %s", result)
    sys.exit(0)


if __name__ == '__main__':
    main()
