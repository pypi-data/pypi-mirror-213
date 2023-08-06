"""
 * Copyright (C) ArtD SAS - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Written by Jonathan Favian Urzola Maldonado <jonathan@artd.com.co>, 2023
"""
from django.core.management.base import BaseCommand

from colombian_cities.data.regions import REGIONS
from colombian_cities.models import Country, Region


class Command(BaseCommand):
    help = "Create colombian regions"

    def handle(self, *args, **kwargs):
        country = Country.objects.get(id=45)
        for region in REGIONS:
            if Region.objects.filter(id=region[0]).count() == 0:
                Region.objects.create(
                    id=region[0],
                    name=region[1],
                    country=country,
                )
                print(f"{region[1]} was created")
            else:
                region_obj = Region.objects.get(
                    id=region[0],
                )
                region_obj.name = region[1]
                region_obj.country = country
                region_obj.save()
                print(f"{region[1]} was updated")
