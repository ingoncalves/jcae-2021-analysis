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
# pylint: disable=unbalanced-tuple-unpacking

import os
import time
import csv
import logging
import numpy as np

from ..constants import OUTPUT_PATH
from ..utils import read_yaml_file, write_json_file, get_file_name
from .compare_job import CompareJob


def perform(yaml_filepath, output_file=None):
    """
    perform filters comparison in parallel
    """
    success, params = __parse_yaml_params(yaml_filepath)

    if not success:
        logging.error("Params parsing failed")
        return None

    n_jobs = len(params["jobs"])
    results = []
    for i in range(n_jobs):
        result = __compare_filters(params["jobs"][i], i, n_jobs)
        results.append(result) 
    return __write_output_files(yaml_filepath, params, results, output_file)


def __compare_filters(params, index, n_jobs):
    """
    compare filters
    """
    log = __get_logger(index, n_jobs)
    job = CompareJob(params, log)
    return job.perform()


def __write_output_files(input_file, params, result, output_folder=None):
    folder = output_folder
    if folder is None:
        case_name = get_file_name(input_file)
        timestr = time.strftime("%Y%m%d_%H%M%S")
        foldername = f"compare_filters_{case_name}_{timestr}"
        folder = os.path.realpath(os.path.join(OUTPUT_PATH, foldername))

    # create output folder
    os.makedirs(folder, exist_ok=True)

    __write_json_params(folder, params)
    __write_job_output(folder, result)
    __write_summary_output(folder, result)

    return folder


def __write_job_output(folder, result):
    for job_index, job in enumerate(result):
        job_filename = f"job_{job_index}_output.dat"
        job_filepath = os.path.join(folder, job_filename)

        data_length = len(job[0]["data"])
        result_table = []
        for i in range(data_length):
            row = {}
            row["index"] = i
            for j in job:
                filter_name = j["filter"]
                row[filter_name] = j["data"][i]
            result_table.append(row)

        fieldnames = result_table[0].keys()

        with open(job_filepath, mode='w') as job_file:
            writer = csv.DictWriter(job_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(result_table)


def __write_summary_output(folder, result):
    summary_filename = "summary.dat"
    summary_filepath = os.path.join(folder, summary_filename)

    flat_result_list = [item for sublist in result for item in sublist]
    fieldnames = [
        "filter",
        "pileup_luminosity",
        "pileup_occupancy",
        "signal_pileup_ratio",
        "phase_module",
        "mean",
        "std",
    ]

    result_table = []
    for entry in flat_result_list:
        row = {}
        for field in fieldnames:
            row[field] = entry[field]
        result_table.append(row)

    with open(summary_filepath, mode='w') as summary_file:
        writer = csv.DictWriter(summary_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(result_table)


def __parse_yaml_params(yaml_filepath):
    success, parsed_params = read_yaml_file(yaml_filepath)
    return success, parsed_params["compare_filters"]


def __write_json_params(folder, params):
    filepath = os.path.join(folder, "params.json")
    write_json_file(filepath, params)


def __get_logger(index, n_jobs):
    return logging.getLogger(f"CompareFilters [JOB {index + 1} - {n_jobs}]")
