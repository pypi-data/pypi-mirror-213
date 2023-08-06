"""
 * Copyright (C) ArtD SAS - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Written by Jonathan Favian Urzola Maldonado <jonathan@artd.com.co>, 2023
"""
from django.contrib import admin

from colombian_cities.models import City, Country, Region


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = [
        "spanish_name",
        "english_name",
        "nom",
        "iso2",
        "iso3",
        "phone_code",
    ]
    list_display = [
        "id",
        "spanish_name",
        "english_name",
        "nom",
        "iso2",
        "iso3",
        "phone_code",
        "status",
    ]
    readonly_fields = [
        "spanish_name",
        "english_name",
        "nom",
        "iso2",
        "iso3",
        "phone_code",
        "status",
        "created_at",
        "updated_at",
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
        "country__spanish_name",
        "country__english_name",
    ]
    list_display = [
        "id",
        "name",
        "country",
        "status",
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
        "name_in_capital_letters",
        "code",
        "region__name",
    ]
    list_display = [
        "name",
        "name_in_capital_letters",
        "region",
        "code",
        "status",
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
