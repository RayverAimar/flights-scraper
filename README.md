<h1 align="center">Flights Scraper  </h1>

<div align="center">
    <a href="https://github.com/psf/black">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
    <a href="https://github.com/milaan9/90_Python_Examples/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-g.svg" alt="MIT License"/></a>

</div>


Automated scraper aimed to get data from different dynamic airline websites. This scraper utilizes selenium for scraping.

Currently, the scraper is aimed to [LATAM Airlines](https://www.latamairlines.com/).


<h3>Technologies</h3>
<p align="center">
  <a href="https://www.selenium.dev" target="_blank" rel="noreferrer"> <img src="https://selenium.dev/images/selenium_logo_square_green.png" alt="selenium" width="40" height="40"/> </a>
  <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
</p>

## Usage
Once cloned, make a LatamScraper instance with your own configuration (origin, destination, departure and return dates)


| Latam Scraper Class |      Type      |
|:-------------------:|:--------------:|
|        Origin       |       str      |
|     Destination     |       str      |
|    Departure Date   | date(yy/mm/dd) |
|     Return Date     | date(yy/mm/dd) |

## Export 
You can export the flights scraped by Latam Scraper in a JSON file with the .save method, which by default will create the JSON file in the [/data](https://github.com/RayverAimar/flights-scraper/tree/master/data) folder.

## Manipulate

The general layout of the JSON file exported is as follows:

```json
{
    "price":
        {
            "Basic":"________"
            "Light": "________"
            "Plus": "________"
            "Top":"________"
        }
    "currency":"________"
    "duration":"________"
    "departure_date":"________"
    "departure_time":"________"
    "arrival_date":"________"
    "arrival_time":"________"
    "scales":"________"
    "details":
        [
            {
            "flight_code":"________"
            "airplane_code":"________"
            "origin":"________"
            "origin_airport":"________"
            "departure_time":"________"
            "destination":"________"
            "destination_airport":"________"
            "arrival_time":"________"
            "duration":"________"
            },

            {
                "scale_details":"________",
                "scale_duration":"________"
            },

            {
                "flight_code":"________",
                "airplane_code":"________",
                "origin":"________",
                "origin_airport":"________",
                "departure_time":"________",
                "destination":"________",
                "destination_airport":"________",
                "arrival_time":"________",
                "duration":"________"
            },
            .
            .
            .
        ]
}
```

Prices per flight might not appear if they are not offered by the company in a given flight.

## Example
The following code uses a configuration for scraping flights from Arequipa to Lima in some random dates.

```python
myScraper = LatamScraper(origin='Arequipa',
                         destination='Lima',
                         departure_date=date(2024, 2, 3),
                         return_date=date(2024, 2, 5),
)
myScraper.scrape()
myScraper.save()
```
```bash
$ python .\src\latam_scraper.py
DevTools listening on ws://127.0.0.1:50368/devtools/browser/0bff5d16-1859-46b8-a936-97dfb68ca76f
There were found 22 flights for 2024-02-03
Initializing scraping...
Processing flight (1/22)
...
rocessing flight (22/22)
Data collected of Flights from 2024-02-03 saved successfully in './data/flights_latam_outbound_Arequipa_2024-02-03.json'
```
