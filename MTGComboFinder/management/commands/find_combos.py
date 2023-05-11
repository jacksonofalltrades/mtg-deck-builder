import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from MTGComboFinder.models import Combo, Card


class Command(BaseCommand):
    combo_card_fields = ['card_a', 'card_b', 'card_c', 'card_d']

    def add_arguments(self, parser):
        parser.add_argument("--include-colors",
                            action="store",
                            help="Specify a string including any of letters RGUBW, "
                                 "or empty string to only include colorless cards")


    def handle(self, *args, **options):
        combos_2card_query = Combo.objects.filter(
            card_a__count_in_arena_collection__gte=1,
            card_b__count_in_arena_collection__gte=1,
            combo_card_count=2)
        combos_3card_query = Combo.objects.filter(
            card_a__count_in_arena_collection__gte=1,
            card_b__count_in_arena_collection__gte=1,
            card_c__count_in_arena_collection__gte=1,
            combo_card_count=3)
        combos_4card_query = Combo.objects.filter(
            card_a__count_in_arena_collection__gte=1,
            card_b__count_in_arena_collection__gte=1,
            card_c__count_in_arena_collection__gte=1,
            card_d__count_in_arena_collection__gte=1,
            combo_card_count=4)
        base_queries = [combos_2card_query, combos_3card_query, combos_4card_query]
