from harvesters.models import Harvester
from django.db import models


def get_domain_info(domain_name: str) -> models:
    if not domain_name or domain_name == "":
        raise ValueError
    return Harvester.objects.filter(domain_name=domain_name, is_active=True)
