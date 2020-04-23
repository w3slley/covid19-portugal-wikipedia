# Covid-19 table/graph generator for wikipedia page
This project has the goal of automating the process of searching and editing tables and graphs for the Portugal Covid-19 pandemic wikipedia page.

## Requirements
- Python 3
- Beautiful Soup
- Pdfminer

## How to use
- Clone this repository and `cd` into it;
- Download the required packages with `pip install -r requirements.txt`;
- Run the command `python3 setup.py`.
- Go to the folder `output/` and copy the content of the file `GraphsCasesByAgeAndGender.txt` to https://en.wikipedia.org/w/index.php?title=2020_coronavirus_pandemic_in_Portugal&action=edit&section=8.
- Go to the folder `output/` and copy the content of the file `SummaryTable.txt` to https://en.wikipedia.org/w/index.php?title=2020_coronavirus_pandemic_in_Portugal&action=edit&section=6.


## Contributions
Thanks to [hagnat](https://github.com/hagnat/) for the inspiration (he did something similar [here](https://github.com/hagnat/covid) but for the Brazilian wikipedia page).

## To do:
- Implement parser for timeline graphs (confirmed cases, deaths, pacients hospitalized and in ICU, daily cases and daily deaths). The problem right now is that I can only get the data for each day (from the DGS report), and not the cumulative ones.
