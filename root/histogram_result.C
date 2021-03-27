/******************************************************************************
 *                         TILECAL SIMULATOR
 *
 * Bernardo S. Peralva    <bernardo@iprj.uerj.br>
 * Guilherme I. Gonçalves <ggoncalves@iprj.uerj.br>
 *
 * Copyright (C) 2018 Bernardo & Guilherme

 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at

 *   http://www.apache.org/licenses/LICENSE-2.0

 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************/

/* USAGE:
 *  root -l -x "root/histogram_result.C(\"cases/moderate_occupancy/results.csv\")"
 */

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TH1.h>
#include <TCanvas.h>
#include <TLegend.h>

#include <iostream>
#include <vector>
#include <fstream>

void read_results(const char *filepath, std::vector<std::string> &keys, TMatrixD &data) {
    std::vector<std::vector<Double_t>> tmpData;

    std::ifstream file;
    std::string   line, col;

    file.open(filepath);
    if (!file.is_open()) {
        throw std::invalid_argument("invalid path");
    }

    // read CSV header (first line)
    std::getline(file, line, '\n');
    std::stringstream header(line);
    while(std::getline(header, col, ',')){
        keys.push_back(col);
    }

    // read CSV data
    while (!std::getline(file, line, '\n').eof()) {
        std::stringstream row(line);
        std::vector<Double_t> rowData;

        while(std::getline(row, col, ',')){
            rowData.push_back(std::stod(col));
        }

        tmpData.push_back(rowData);
    }

    file.close();

    Int_t rows = tmpData.size();
    Int_t cols = tmpData[0].size();

    data.ResizeTo(rows, cols);
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < cols; j++) data[i][j] = tmpData[i][j];
}

void histogram_result(const Char_t* resultsFile)
{
    std::vector<std::string> keys;
    TMatrixD data;
    read_results(resultsFile, keys, data);

    UInt_t nHist = keys.size();
    Long64_t nData = data.GetNrows();

    TCanvas *canvas = new TCanvas("results", "Performance Results");

    TH1D * hists[nHist];
    for (UInt_t k = 0; k < nHist; k++) {
        hists[k] = new TH1D(keys[k].c_str(), "", 100, -200, 200);
    }

    for (Long64_t i = 0; i < nData; i++) {
        for (UInt_t k = 0; k < nHist; k++) {
            hists[k]->Fill(data[i][k]);
        }
    }

    Int_t color = 1;
    for (UInt_t k = 0; k < nHist; k++) {
        hists[k]->GetYaxis()->SetRangeUser(0, 70000);
        hists[k]->SetLineWidth(4);
        hists[k]->SetLineColor(color++);

        if (k == 0 ) {
            hists[k]->Draw();
            hists[k]->SetTitle("");
            hists[k]->GetXaxis()->SetTitle("Estimation Error");
            hists[k]->GetYaxis()->SetTitle("Events");
        } else {
            hists[k]->Draw("sames");
        }
    }

    TLegend *leg = new TLegend(0.7, 0.7, 0.9, 0.9);
    for (UInt_t k = 0; k < nHist; k++)  leg->AddEntry(hists[k], keys[k].c_str(), "l");
    leg->Draw();
}
