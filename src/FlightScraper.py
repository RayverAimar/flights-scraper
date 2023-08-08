import json
from utils import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date, timedelta, datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import *

class LatamScraper:
    def __init__(self, origin, destination, departure_date, return_date):
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.return_date = return_date
        self.flights = []

    def __get_flight_query_latam(self):
        if not dict_of_acronyms[self.origin]:
            raise NameError(f'\'{self.origin}\' is not a valid place.')
        if not dict_of_acronyms[self.destination]:
            raise NameError(f'\'{self.destination}\' is not a valid place.')
        if self.departure_date <= datetime.now().date():
            raise ValueError(f'{self.departure_date} is not a valid date to query flights.')
        if self.departure_date > self.return_date:
            raise ValueError(f'{self.return_date} should be equal or higher than the date of departure.')

        origin = f'origin={dict_of_acronyms[self.origin]}'
        destination = f'destination={dict_of_acronyms[self.destination]}'
        departure_date = f'outbound={self.departure_date}T12%3A00%3A00.000Z'
        return_date = f'inbound={self.return_date}T12%3A00%3A00.000Z'
        adt = 'adt=1'
        chd = 'chd=0'
        inf = 'inf=0'
        trip = 'trip=RT'
        cabin = 'cabin=Economy'
        redemption = 'redemption=false'
        sort = 'sort=PRICE%2Casc'
        query_tuple=(origin,
                     departure_date,
                     destination,
                     return_date,
                     adt,
                     chd,
                     inf,
                     trip,
                     cabin,
                     redemption,
                     sort,
        )
        url = 'https://www.latamairlines.com/pe/es/ofertas-vuelos?'
        query = url + "&".join(query_tuple)
        return query
    
    def __get_data(self):
        latam_scraper_dict_list = []
        for flight in self.flights:
            latam_scraper_dict_list.append(flight.get_dict())
        return latam_scraper_dict_list
    
    def save(self, title="flights_latam_"):
        title='./data/'+title+self.departure_date.__str__()+'.json'
        with open(title, "w") as outfile:
            json.dump(self.__get_data(), outfile)
            print(f'Data collected of Flights from {self.departure_date} saved successfully in \'{title}\'')

    def scrape(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get(self.__get_flight_query_latam()) # See if dates are correct -> Should be later than today 
        try:
            #Wait for page to load
            WebDriverWait(driver, timeout=TIMEOUT_PER_PAGE).until(EC.presence_of_element_located((By.XPATH, '//li[contains(@class, "body-flightsstyle__ListItemAvailableFlights-sc__sc-1p74not-5")]')))
            flights = driver.find_elements(By.XPATH, '//li[contains(@class, "body-flightsstyle__ListItemAvailableFlights-sc__sc-1p74not-5")]')
            print(f'There were found {len(flights)} flights for {self.departure_date}')
            print(f'Initializing scraping...')
            for index, flight in enumerate(flights):
                print(f"Processing flight ({index+1}/{len(flights)})")
                # Get the currency
                currency = flight.find_element(By.XPATH, './/span[contains(@class, "display-currencystyle__CurrencyAmount-sc__sc-19mlo29-2 fMjBKP currency")]').get_attribute('textContent')
                # Currency and price have the same tags and classes, they only differ in one word
                price = flight.find_element(By.XPATH, './/span[contains(@class, "display-currencystyle__CurrencyAmount-sc__sc-19mlo29-2 fMjBKP")][2]').get_attribute('textContent')
                
                box_info = flight.find_element(By.XPATH, './/div[contains(@class, "card-flightstyle__WrapperFlightInfo-sc__sc-16r5pdw-17 ktzsYJ")]')
                
                duration_str = box_info.find_element(By.XPATH, './/div[2]/span[2]').get_attribute('textContent')
                duration_hours = get_hours_from_str(duration_str)
                duration_minutes = get_minutes_from_str(duration_str) if len(duration_str) > 4 else 0
                duration = timedelta(
                    hours=duration_hours,
                    minutes=duration_minutes,
                )

                departure_time_str = box_info.find_element(By.XPATH, './/div[1]/span').get_attribute('textContent')
                departure_datetime_hour, departure_datetime_minutes = get_hours_and_minutes_from_time(departure_time_str)
                departure_datetime = datetime(self.departure_date.year,
                                              self.departure_date.month,
                                              self.departure_date.day,
                                              departure_datetime_hour,
                                              departure_datetime_minutes,
                )
                
                arrival_datetime = departure_datetime + duration

                scale = flight.find_element(By.XPATH, './/a[contains(@class, "sc-hAZoDl fkClzL")]/span').get_attribute('textContent')
                # Scale is either just one number (digit) or a complete ('Directo') word
                scale = int(scale[0]) if scale[0].isnumeric() else scale
                fees_button = flight.find_element(By.XPATH, './/div[contains(@class, "card-flightstyle__CardExpander-sc__sc-16r5pdw-2 eHxiMm")]')
                fees_button.click()
                # Once the button is clicked
                WebDriverWait(driver, timeout=TIMEOUT_PER_BUTTON).until(EC.presence_of_element_located((By.XPATH, './/li[contains(@class, "columnBrandstyle__BrandWrapperDesktop-sc__sc-1e0tr9m-3 lewOyF")]')))
                fees_box = flight.find_elements(By.XPATH, './/li[contains(@class, "columnBrandstyle__BrandWrapperDesktop-sc__sc-1e0tr9m-3 lewOyF")]')
                fees = []
                for i, fee in enumerate(fees_box):
                    if i != len(fees_box) - 1:
                        fee_name = fee.find_element(By.XPATH, './/span[contains(@class, "brandCabinstyle__BrandName-sc__sc-5zp04j-1")]').get_attribute('textContent')
                    else:
                        fee_name = fee.find_element(By.XPATH, './/span[contains(@class, "jFntBH")]').get_attribute('textContent')
                    if fee_name != 'Basic':
                        fee_price = float(fee.find_element(By.XPATH, './/div[contains(@class, "display-currencystyle__DisplayCurrencyWrapper-sc__sc-19mlo29-0 brikxf differentialPricestyle__ExtendedDisplayCurrency-sc__sc-1wmoeew-2 taREJ")]/div/span/span[2]').get_attribute('textContent'))
                    else:    
                        fee_price = float(fee.find_element(By.XPATH, './/span[contains(@class, "display-currencystyle__CurrencyAmount-sc__sc-19mlo29-2 fMjBKP")][2]').get_attribute('textContent'))
                    fee_price = fee_price + float(price) if fee_price != float(price) else fee_price
                    fees.append(Fee(name=fee_name,
                                    price=fee_price,
                                )
                    )
                close_fees_box_button = flight.find_element(By.XPATH, './/button[contains(@class, "MuiButtonBase-root MuiButton-root MuiButton-text sc-jqUVSM jkrDKT MuiButton-disableElevation")]')
                close_fees_box_button.click()
                current_flight = Flight(fees=fees,
                                        currency=currency,
                                        duration=duration_str,
                                        departure_datetime=departure_datetime,
                                        arrival_datetime=arrival_datetime,
                                        scale=scale,
                )
                
                scale_button = flight.find_element(By.XPATH, './/a[contains(@class, "sc-hAZoDl fkClzL")]')
                scale_button.click()
                
                WebDriverWait(driver, timeout=TIMEOUT_PER_BUTTON).until(EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "path-infostyle__Top-sc__sc-xj1cll-2 eZnnpl")]/div[contains(@class, "iataCode")]/span[2]')))

                flight_segments = flight.find_elements(By.XPATH, '//section[contains(@class, "itinerarystyle__Section-sc__sc-1n97ky6-1 ddwMQK")]')
                scale_segments = flight.find_elements(By.XPATH, '//section[contains(@class, "itinerarystyle__Section-sc__sc-1n97ky6-1 ddwMLI")]') if len(flight_segments) > 1 else None
                
                current_flight.add_details(get_details_from_flight_segment(flight_segments[0]))
                if scale_segments:
                    for i, scale_segment in enumerate(scale_segments):
                        current_flight.add_details(get_details_from_scale_segment(scale_segment))
                        current_flight.add_details(get_details_from_flight_segment(flight_segments[i+1]))
                
                self.flights.append(current_flight)

                close_button = flight.find_element(By.XPATH, '//button[contains(@class, "MuiButtonBase-root MuiButton-root MuiButton-text sc-jqUVSM sc-kDDrLX jkrDKT fWvxrE sc-iqcoie sc-evZas ehOBsB drzyQS MuiButton-disableElevation")]')
                close_button.click()
                WebDriverWait(driver, timeout=TIMEOUT_PER_BUTTON).until(EC.presence_of_element_located((By.XPATH, '//li[contains(@class, "body-flightsstyle__ListItemAvailableFlights-sc__sc-1p74not-5")]')))
        except TimeoutException:
            print('The site can\'t be reached or specific tag wasn\'t found. ERR_CONNECTION_TIMED_OUT.')
        driver.quit()
    
    def print(self):
        for flight in self.flights:
            print(flight)
            flight.print_details()

def get_details_from_scale_segment(scale_segment):
    details = scale_segment.find_element(By.XPATH, './/div[contains(@class, "connection-infostyle__ConnectionInformation-sc__sc-1qity98-2 bOpeBi")]/div').get_attribute('textContent')
    duration = scale_segment.find_element(By.XPATH, './/div[contains(@class, "connection-infostyle__ConnectionInformation-sc__sc-1qity98-2 bOpeBi")]/span').get_attribute('textContent')
    return Scale(duration, details)

def get_details_from_flight_segment(flight_segment):
    
    def get_origin_hour_airportname_from_subsegment(subsegment):
        origin = subsegment.find_element(By.XPATH, './/div[contains(@class, "iataCode")]/span[1]').get_attribute('textContent')
        hour = subsegment.find_element(By.XPATH, './/div[contains(@class, "iataCode")]/span[2]').get_attribute('textContent')
        airport_name = subsegment.find_element(By.XPATH, './/span[contains(@class, "airport-name")]').get_attribute('textContent')
        return origin, hour, airport_name
    
    subsegment_top = flight_segment.find_element(By.XPATH, './/div[contains(@class, "path-infostyle__Top-sc__sc-xj1cll-2 eZnnpl")]')
    origin, departure_hour, departure_airport_name = get_origin_hour_airportname_from_subsegment(subsegment_top)
    duration = flight_segment.find_element(By.XPATH, './/div[contains(@class, "path-infostyle__Middle-sc__sc-xj1cll-3 ksaVIu")]/span[2]').get_attribute('textContent')
    subsegment_bot = flight_segment.find_element(By.XPATH, './/div[contains(@class, "path-infostyle__Bottom-sc__sc-xj1cll-4 jMpZeH")]')
    destination, arrival_hour, arrival_airport_name = get_origin_hour_airportname_from_subsegment(subsegment_bot)
    flight_code = flight_segment.find_element(By.XPATH, './/div[contains(@class, "plane-infostyle__AirlineWrapper-sc__sc-7wc798-0 cHGYdi airline-wrapper")]').get_attribute('textContent')
    airplane_name = flight_segment.find_element(By.XPATH, './/span[contains(@class, "airplane-code")]').get_attribute('textContent')

    return FlightDetails(origin,
                         departure_hour,
                         departure_airport_name,
                         duration,
                         destination,
                         arrival_hour,
                         arrival_airport_name,
                         flight_code,
                         airplane_name,
    )

myScraper = LatamScraper(origin='Arequipa',
                         destination='Piura',
                         departure_date=date(2024, 2, 2),
                         return_date=date(2024, 2, 5),
)
myScraper.scrape()
myScraper.save()
