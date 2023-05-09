import json
import os
from typing import Union

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from MTGComboFinder.models import *


class Command(BaseCommand):
    help = """
    Load canonical card data. Expects data located and named as follows:
    data/
        combos.json - all combo data
        AtomicCards.json - canonical card database
        collection_exports/
            <any file> - each line is <count> <card name> <other stuff>
    """

    def add_arguments(self, parser):
        parser.add_argument("--last-loaded-atomic-card")
#        parser.add_argument("poll_ids", nargs="+", type=int)

    @classmethod
    def skip_card(cls, found_last_card: bool, last_loaded_atomic: Union[str,None]) -> bool:
        if last_loaded_atomic is not None:
            if not found_last_card:
                return True
            else:
                return False
        else:
            return False

    def process_card(self, key: str, card_data: dict) -> bool:
        try:
            ci = card_data['colorIdentity']
            if not Card.objects.filter(name=card_data['name']).exists():
                c = Card.objects.create(
                    is_red='R' in ci,
                    is_green='G' in ci,
                    is_blue='U' in ci,
                    is_white='W' in ci,
                    is_black='B' in ci,
                    count_in_arena_collection=0,
                    converted_mana_cost=card_data['convertedManaCost'],
                    name=card_data['name'],
                    power='power' in card_data and card_data['power'] or 0,
                    toughness='toughness' in card_data and card_data['toughness'] or 0,
                    full_type_name=card_data['type'],
                    rules_text='text' in card_data and card_data['text'] or ''
                )
                # import pdb; pdb.set_trace()

                for super_type in card_data['supertypes']:
                    csupt, _ = CardSupertype.objects.get_or_create(name=super_type)
                    c.supertypes.add(csupt)

                for card_type in card_data['types']:
                    ct, _ = CardType.objects.get_or_create(name=card_type)
                    c.types.add(ct)

                for sub_type in card_data['subtypes']:
                    csubt, _ = CardSubtype.objects.get_or_create(name=sub_type)
                    c.subtypes.add(csubt)

                if 'keywords' in card_data:
                    for d in card_data['keywords']:
                        k, _ = Keyword.objects.get_or_create(name=d)
                        c.keywords.add(k)
                self.stdout.write(f"Completed processing card=[{key}]")
        except:
            self.stdout.write(f"Problem processing card {key}")
            import traceback
            traceback.print_exc()
            raise

    def handle(self, *args, **options):
        atomic_path = os.path.join(settings.BASE_DIR, "MTGComboFinder", "data", "AtomicCards.json")

        print(options)
        last_loaded_atomic = options['last_loaded_atomic_card']
        found_last_card = False

        with open(atomic_path, 'r') as f:
            atomic_data = json.load(f)
            sorted_keys = sorted(atomic_data['data'].keys())
            for key in sorted_keys:
                if not self.skip_card(found_last_card, last_loaded_atomic):
                    if last_loaded_atomic == key:
                        found_last_card = True
                    self.stdout.write(f"Processing card [{key}]")
                    self.process_card(key, atomic_data['data'][key][0])



