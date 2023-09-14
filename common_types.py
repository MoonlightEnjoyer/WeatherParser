class User:
    def __init__(self, id, city) -> None:
        self.id = id
        self.city = city

class Report:
    def __init__(self, message, city, type) -> None:
        self.message = message
        self.city = city
        self.type = type

class Config:
    def __init__(self) -> None:
        with open('../config.txt', 'r') as config_file:
            lines = config_file.readlines()
            self.token = lines[0].strip()