"""
            MASTERS ANALYSIS

Bernardo S. Peralva    <bernardo@iprj.uerj.br>
Guilherme I. Gonçalves <ggoncalves@iprj.uerj.br>

Copyright (C) 2019 Bernardo & Guilherme

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
get filter name by labelf the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import glob
import csv
import matplotlib.pyplot as plt
import numpy as np
from analysis.constants import get_filter_name


def plot_summary(folder, output_file, x_field, x_label, y_field, y_label):
    """ 1D Plot pileup_occupancy x std """
    filepath = os.path.join(folder, "summary.dat")
    data = []
    with open(filepath, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)

    series = {}

    # x axis
    x_values = np.unique([float(d[x_field]) for d in data])
    x_axis = np.sort(x_values)
    series["x"] = x_axis

    # y axis
    filters = np.unique([d["filter"] for d in data])
    for key in filters:
        series[key] = []
    for entry in data:
        std_mev = adc_to_mev(entry[y_field])
        series[entry["filter"]].append(std_mev)

    # multiple line plot
    linestyles = ["--", "-.", "-"]
    colors = ["r", "k", "b"]
    markers = ["^", "s", "o"]

    plt.figure()
    for f, l, c, m in zip(filters, linestyles, colors, markers):
        plt.plot("x", f, data=series, label=get_filter_name(f), linestyle=l, color=c, marker=m, markersize=5)
    plt.legend()
    plt.xlabel(x_label, horizontalalignment='right', x=1.0)
    plt.ylabel(y_label, horizontalalignment='right', y=1.0)

    figure_filepath = os.path.join(folder, output_file)
    plt.savefig(figure_filepath)


def plot_job_histograms(folder, params, title_builder):
    """ 1D Histogram """
    glob_pattern = os.path.join(folder, "job_*_output.dat")
    for index, filepath in enumerate(glob.glob(glob_pattern)):

        data = []
        with open(filepath, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append(row)

        filters = list(data[0].keys())
        filters.remove("index")

        kwargs = dict(bins=100, linewidth=1.2)
        plt.figure(index)

        edge_colors = ["grey", "r", "b"]
        colors = ["lightgray", None, None]
        histtypes=['stepfilled', 'step', 'step']
        for f, ec, c, ht in zip(filters, edge_colors, colors, histtypes):
            serie = [adc_to_mev(d[f]) for d in data]
            plt.hist(serie, **kwargs, label=get_filter_name(f), ec=ec, color=c, histtype=ht)

        job = params["jobs"][index]
        # plt.title(title_builder(job))
        plt.xlabel("Erro de Estimação [MeV]", horizontalalignment='right', x=1.0)
        plt.ylabel("Número de Eventos", horizontalalignment='right', y=1.0)
        plt.xlim(-1000, 1000)
        plt.legend()

        figure_filepath = os.path.join(folder, f"job_{index}_histogram.pdf")
        plt.savefig(figure_filepath, format="pdf")

def __print_latex_table(folder, x_field):
    filepath = os.path.join(folder, "summary.dat")
    data = []
    with open(filepath, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)

    mean_series = {}
    std_series = {}

    # x axis
    x_values = np.unique([float(d[x_field]) for d in data])
    x_axis = np.sort(x_values)

    # y axis
    filters = np.unique([d["filter"] for d in data])
    for key in filters:
        mean_series[key] = []
        std_series[key] = []
    for entry in data:
        mean_mev = adc_to_mev(entry["mean"])
        mean_series[entry["filter"]].append(mean_mev)

        std_mev = adc_to_mev(entry["std"])
        std_series[entry["filter"]].append(std_mev)

    for index, _ in enumerate(x_axis):
        row = []
        row.append(x_axis[index])
        row.append(mean_series['WHF'][index])
        row.append(std_series['WHF'][index])
        row.append(mean_series['OF2'][index])
        row.append(std_series['OF2'][index])
        row.append(mean_series['COF'][index])
        row.append(std_series['COF'][index])
        row_str = "%f && %.4f & %.4f && %.4f & %.4f && %.4f & %.4f \\\\" % (
            row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        row_str = row_str.replace(".", ",")
        print(row_str)


def adc_to_mev(value):
    """ adv to MeV conversion """
    return 12 * float(value)
