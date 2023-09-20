#!/usr/bin/python3

SEPARATOR = '='


class PropertiesReader:
    def __init__(self, properties_file) -> None:
        self.keys = {}
        with open(properties_file, 'r') as config_file:
            for line in config_file:
                if SEPARATOR in line:
                    key, value = line.split(SEPARATOR, 1)
                    self.keys[key.strip()] = value.strip()

    def get(self, key):
        try:
           return self.keys[key]
        except:
            return None
