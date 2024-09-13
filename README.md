# Gene Sequence Web Scraper

## Overview
This project is a powerful web scraping tool designed to interact with an online biology tool that processes gene sequences and generates corresponding primer sets. The tool allows continuous interaction with the site, passing through gene sequences, setting preferences, and downloading the relevant primer sets for each sequence. The scraper was successfully used to process **50,000 gene sequences** and retrieve their corresponding primers. The primary goal of this project is to reverse-engineer the site's algorithm using machine learning.

## Features
- **Scraping Biology Tool**: Automatically submits gene sequences to the biology tool and retrieves primers.
- **Sequence Processing**: Manages large batches of sequences (50,000+) efficiently.
- **Error Handling**: Efficient error handling correctly handles errors with grace allowing the script to keep running without manual intervention.
- **Preferences Automation**: Interacts with the preferences page to customize the parameters for each query.
- **Machine Learning Ready**: Outputs data for machine learning algorithms to reverse-engineer the underlying algorithm of the online tool.
- **Modular Design**: The project is modular, with core functionality divided across multiple Python scripts for clarity and maintainability.
- **Memory Efficient**: Memory concious programming techniques have been used to minimise memory consumption throughout the script preventing memory related issues, or recursive stack overflows, allowing the script to run     continuosly for massive gene sequence sets.
- **Memory Usage Data**: using MatPlotLib a graph plotting the memory usage of the script over run time is plotted at the end of script/sigint.

## Installation

### Step 1: Clone the repository
```bash 
git clone https://github.com/Dsavvi180/sequenceGenWebScraper.git
cd <project-folder>
```

### Step 2: Install Dependencies
```bash 
pip install virtualenv
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```
### Step 3: Run
```bash 
python3 main.py
```
