# Analysis for the JCAE 2021 Paper

This repository contains the source code of all analysis performed for the paper to be published at Journal of Control, Automation and Electrical Systems – JCAE, ISSN: 2195-3880 (print version) e ISSN: 2195-3899 (electronic version).

## Setup Python Environment

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

## Execute Analysis

The analysis consists of two steps:
1. Dataset generation
2. Estimators performance comparison

Create a subfolder within the `cases` folder and name it according to your simulation characteristics. Create a `setup.yml` file that contains all the parameters of the simulations.
An `setup.yml` example could be such as:
    
    setup:
        pulse_shape:
            path: "shared/cern-atlas-tilecalorimeter-pulse-shape.dat"
            digital_samples_time: [-75.5, -50.0, -25.0, 0.0, 25.0, 50.0, 75.0]
        pulse_generator:
            deformation_level: 0.01
            noise_mean: 0
            noise_sigma: 1.5
            pedestal: 0
            phase_generator: "random_integers"
            phase_params: [-4, 4]
        dataset_generator:
            n_events: 1000000
            pileup_occupancy: 0.5
            pileup_luminosity: 30.0
            sampling_rate: 25.0
            signal_pileup_ratio: 1
            window_size: 7

Then, you can execute the simulation as:

    python3 -m analysis cases/moderate_occupancy/setup.yaml

## Execute Examples

There are some examples of other features in the `examples` folder.
For instance, you can run one of these files as:

    python3 -m examples.pulse_simulator

-------------------------

>**Author:** Guilherme Inácio Gonçalves <ggoncalves@iprj.uerj.br><br/>
>Master in Computational Modeling at the State University of Rio de Janeiro.
