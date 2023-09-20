#!/usr/bin/python3

import unittest
from app.config.properties_reader import PropertiesReader


class TestPropertiesReader(unittest.TestCase):

    def setUp(self) -> None:
        self.properties_reader = PropertiesReader('test_data/test-config.properties')

    def test_get_properties(self):
        self.assertEqual("John", self.properties_reader.get("name"))
        self.assertEqual("Dublin", self.properties_reader.get("address"))

    def test_properties_not_found(self):
        self.assertIsNone(self.properties_reader.get("job"))
        self.assertIsNone(self.properties_reader.get("car"))