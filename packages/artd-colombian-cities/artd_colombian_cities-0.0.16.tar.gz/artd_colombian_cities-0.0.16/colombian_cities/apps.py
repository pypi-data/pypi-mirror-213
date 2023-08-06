from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ColombianCitiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _("Colombian Cities")
    name = "colombian_cities"
