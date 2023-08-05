HOUR = 'hour'
MINUTES = 'min'

def get_minutes_from_str(datetime_str): #If datetime lenght is more than 4 characters then it has minutes in it
        index_to_trim = -1
        for i, e in enumerate(datetime_str):
            if e == MINUTES[0]:
                index_to_trim = i
                break
        return int(datetime_str[index_to_trim-3:index_to_trim-1])

def get_hours_from_str(datetime_):
    index_to_trim = -1
    for i, e in enumerate(datetime_):
        if e == HOUR[0]:
            index_to_trim = i
            break
    return int(datetime_[:index_to_trim-1])

def get_hours_and_minutes_from_datetime(datetime_):
    separator_index = -1
    for i, e in enumerate(datetime_):
        if e == ':':
            separator_index = i
            break
    return int(datetime_[:separator_index]), int(datetime_[separator_index+1:])

class Flight:
    def __init__(self, price, currency, duration, departure_datetime, arrival_datetime, scale=None, next_flight=None):
        self.price = price
        self.currency = currency
        self.duration = duration
        self.departure_datetime = departure_datetime
        self.arrival_datetime = arrival_datetime
        self.scale = scale
        self.next_flight = next_flight
        self.details = []

    def add_details(self, detail):
        self.details.append(detail)

    def print_details(self):
        for detail in self.details:
            print(detail)

    def __str__(self) -> str:
        return f"Price: {self.currency.upper()} {self.price}\n\
                Duration: {self.duration}\n\
                Departure Datetime: {self.departure_datetime}\n\
                Arrival Datetime: {self.arrival_datetime}\n\
                Scale: {self.scale}\n"
    
    def get_dict(self):
        flight_dict = {}
        flight_dict['price'] = self.price + ' ' + self.currency
        flight_dict['duration'] = self.duration
        flight_dict['departure_date'] = str(self.departure_datetime.year) + '-' + str(self.departure_datetime.month) + '-' + str(self.departure_datetime.day)
        flight_dict['departure_time'] = str(self.departure_datetime.hour) + ':' + str(self.departure_datetime.minute)
        flight_dict['arrival_date'] = str(self.arrival_datetime.year) + '-' + str(self.arrival_datetime.month) + '-' + str(self.arrival_datetime.day)
        flight_dict['arrival_time'] = str(self.arrival_datetime.hour) + ':' + str(self.arrival_datetime.minute)
        flight_dict['scales'] = self.scale
        details_list = []
        for detail in self.details:
            details_list.append(detail.get_dict())
        flight_dict['details'] = details_list
        return flight_dict
    

class FlightDetails:
    def __init__(self, origin, departure_time, departure_airport, duration, destination, arrival_time, arrival_airport, flight_code, airplane_code):
        self.origin = origin
        self.departure_time = departure_time
        self.departure_airport = departure_airport
        self.duration = duration
        self.destination = destination
        self.arrival_time = arrival_time
        self.arrival_airport = arrival_airport
        self.flight_code = flight_code
        self.airplane_code = airplane_code

    def __str__(self) -> str:
        out_str = f'\tFlight: {self.flight_code} ({self.airplane_code})\n'
        out_str += f'\t- Origin: {self.origin} {self.departure_time} ({self.departure_airport})\n'
        out_str += f'\t- Duration: {self.duration}\n'
        out_str += f'\t- Destination: {self.destination} {self.arrival_time} ({self.arrival_airport})'
        return out_str
    
    def get_dict(self):
        flightdetails_dict = {}
        flightdetails_dict['flight_code'] = self.flight_code
        flightdetails_dict['airplane_code'] = self.airplane_code
        flightdetails_dict['origin'] = self.origin + ' (' + self.departure_time + ')'
        flightdetails_dict['origin_airport'] = self.departure_airport
        flightdetails_dict['destination'] = self.destination + ' (' + self.arrival_time + ')'
        flightdetails_dict['destination_airport'] = self.arrival_airport
        flightdetails_dict['duration'] = self.duration
        return flightdetails_dict

class Scale:
    def __init__(self, scale_duration, details):
        self.scale_duration = scale_duration
        self.details = details
    
    def __str__(self) -> str:
        return f'\t\t{self.details}\n\t\t{self.scale_duration}'
    
    def get_dict(self):
        scale_dict = {}
        scale_dict['scale_details'] = self.details
        scale_dict['scale_duration'] = self.scale_duration
        return scale_dict

dict_of_acronyms = {
    'Arequipa':'AQP',
    'Cuzco':'CUZ',
    'Lima':'LIM',
    'Piura':'PIU',
    'Tumbes':'TBP'
}