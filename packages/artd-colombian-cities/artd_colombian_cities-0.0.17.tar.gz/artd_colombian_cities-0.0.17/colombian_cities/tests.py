"""
 * Copyright (C) ArtD SAS - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Written by Jonathan Favian Urzola Maldonado <jonathan@artd.com.co>, 2023
"""
from django.test import TestCase

from colombian_cities.data.cities import CITIES
from colombian_cities.data.countries import COUNTRIES
from colombian_cities.data.regions import REGIONS
from colombian_cities.models import City, Country, Region


class TestLocation(TestCase):
    def setUp(self) -> None:
        for country in COUNTRIES:
            Country.objects.create(
                id=country[0],
                spanish_name=country[1],
                english_name=country[2],
                nom=country[3],
                iso2=country[4],
                iso3=country[5],
                phone_code=country[6],
            )
        country = Country.objects.get(id=45)
        for region in REGIONS:
            Region.objects.create(
                id=region[0],
                name=region[1],
                country=country,
            )
        for city in CITIES:
            region = Region.objects.get(id=city[4])
            City.objects.create(
                id=city[0],
                name=city[3],
                name_in_capital_letters=city[2],
                code=city[1],
                region=region,
            )
        self.countries = Country.objects.all()
        self.regions = Region.objects.all()
        self.cities = City.objects.all()

    def test_country_creation(self):
        assert len(COUNTRIES) == self.countries.count()

    def test_colombian_region_creation(self):
        assert len(REGIONS) == self.regions.count()

    def test_colombian_cities_creation(self):
        assert len(CITIES) == self.cities.count()
