# Romania Parliament Scraper

Scrapes information about Romanian parliament members (deputies and senators) from official government websites.

## Setup

1. Create virtual environment and activate it:
```
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:
```
pip install -r requirements.txt
```

## Usage

Run the scraper:
```
python src/scraper.py
```

Output will be saved to data/parliament_members.json

## Features

- Scrapes deputy names, counties, and parties
- Extracts profile URLs
- Optional: Scrapes individual profiles for email and phone
- Optional: Downloads and parses CVs for contact information

## Todo

- [ ] Test and adjust HTML parsing selectors
- [ ] Add Senate scraping
- [ ] Implement CV download and parsing
- [ ] Add error recovery and resume capability
- [ ] Add data validation
