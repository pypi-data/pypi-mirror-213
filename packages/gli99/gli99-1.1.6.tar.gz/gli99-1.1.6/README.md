***Do NOT use this repo for professional use, this was a personal project to practice version control, web scraping, and readme design. The correct way to access GifCities.org is through its (admittedly slow) [API](https://gifcities.archive.org/api/v1/gifsearch?q=hamster).***

---



## Installation

Run the following to install:

```python
pip install gli99
```

## Usage

```python
from gli99.tools import GifScraper

gs = GifScraper(browser="firefox")
gs.load(query="brazil",amount=5)
gs.download()
```

currently supported browsers:

* Edge
* Chrome
* Firefox