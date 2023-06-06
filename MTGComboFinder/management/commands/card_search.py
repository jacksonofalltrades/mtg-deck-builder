import json
import os
from typing import Union

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from MTGComboFinder.models import *
from MTGComboFinder.search_parser import CardSearchParser


class Command(BaseCommand):
    help = """
    Filters out chaff, filters by collected cards, then applies arguments to further provide search results
    Filters:
    * Color identity
    * Perform complex search using mini-language:
    * (a&b)|~c - and, or, not
    * condition keys:
    * t: type
    * s: subtype
    * z: supertype
    * r: rules text contains
    * e.g., z:legendary&s:rat|r:"+1/+1 counter"
    *    Find legendary rats or cards that give a +1/+1 counter
    """

    def add_arguments(self, parser):
        parser.add_argument("--color-identity", "-c", action="store", help="List of colors as string of letters, RGUWB")
        parser.add_argument("--search-expression", "-s", action="store", help="Search mini-language")

    def handle(self, *args, **options):

        pass


