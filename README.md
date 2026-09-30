# Electronic Word-of-Mouth Cognitive Complexity and Consumer Churn

This repository contains the data extraction scripts, analytical notebooks, and primary datasets for the paper: **"Estimating the Impact of Electronic Word-of-Mouth Cognitive Complexity on Digital Consumer Churn using Double Machine Learning."**

## Overview
This project investigates how the cognitive complexity of digital product reviews (eWOM) impacts a reviewer's subsequent digital consumption. Using a two-stage Double Machine Learning (DML) approach on Steam API telemetry data, the pipeline extracts structural complexity from text using `spaCy` and emotional valence using a RoBERTa sequence classifier, isolating the causal treatment effects on user churn.

## Repository Contents
| File/Directory | Description |
| :--- | :--- |
| `src/data_collection.py` | Python script utilizing the Steamworks Web API to fetch unstructured review text and longitudinal playtime telemetry (App ID: 1091500). |
| `data/primary_steam_data_1091500.csv` | Curated dataset containing 2,485 English-language reviews, engagement telemetry, and extracted latent variables. |
| `notebooks/Data_analysisR10.ipynb` | Jupyter Notebook containing the full NLP feature extraction, nuisance function training, and two-stage DML estimation pipeline. |

## Installation & Requirements
The analysis requires Python 3.8+ and the following core dependencies:
* `pandas`, `numpy`, `scikit-learn`, `statsmodels`
* `econml` (Causal estimation)
* `transformers`, `torch` (RoBERTa sentiment classification)
* `spacy`, `textstat` (Syntactic dependency parsing)

```bash
pip install pandas numpy scikit-learn statsmodels econml transformers torch spacy textstat
python -m spacy download en_core_web_sm
