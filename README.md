# Table/graph generator for Portugal's Covid-19 Wikipedia page
This project has the goal of automating the process of searching and editing tables and graphs for the Portugal Covid-19 pandemic wikipedia page.

## Requirements
- Python 3
- Beautiful Soup
- pdfminer

## How to use
- Clone this repository and `cd` into it.
- Download the required packages with `pip3 install -r requirements.txt`.
- Run the command `python3 setup.py`.
- Go to the folder `output/` and copy the content of the file `GraphsCasesByAgeAndGender.txt` to https://en.wikipedia.org/w/index.php?title=2020_coronavirus_pandemic_in_Portugal&action=edit&section=8.
- Go to the folder `output/` and copy the content of the file `SummaryTable.txt` to https://en.wikipedia.org/w/index.php?title=2020_coronavirus_pandemic_in_Portugal&action=edit&section=6.


## Contributions
Thanks to [hagnat](https://github.com/hagnat/) for the inspiration (he did something similar [here](https://github.com/hagnat/covid) but for the Brazilian wikipedia page).

## To do:
- Implement testing.
- Right now, the correctness of the information taken from the PDFs is based upon its formatting. If DGS changes it, some error will be thrown while parsing for the data. That needs to be fixed (it's working for DGS reports starting on April 1 - I tested :).