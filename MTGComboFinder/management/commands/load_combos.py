import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from MTGComboFinder.models import Combo, Card


class Command(BaseCommand):
    combo_card_fields = ['card_a', 'card_b', 'card_c', 'card_d']
    help = """
    Load canonical card data. Expects data located and named as follows:
    data/
        combos.json - all combo data
        AtomicCards.json - canonical card database
        collection_exports/
            <any file> - each line is <count> <card name> <other stuff>
    """

    def handle(self, *args, **options):
        combo_path = os.path.join(settings.BASE_DIR, "MTGComboFinder", "data", "combos.json")
        with open(combo_path, 'r') as f:
            combo_dict = json.load(f)
            for combo_id, combo_cards in combo_dict['combos'].items():
                combo_query = Combo.objects.filter(combo_id=int(combo_id))
                if not combo_query.exists():
                    card_name_list = combo_cards['cardnames']
                    card_list = []
                    for card_name in card_name_list:
                        card = Card.objects.filter(name__startswith=card_name)
                        if card.exists():
                            card_list.append(card.first())
                        else:
                            print(f"Couldn't find card named {card_name}")
                    card_count = len(card_list)
                    if card_count >= 2:
                        combo_kwargs = {
                            "combo_card_count": card_count,
                            "combo_id": combo_id
                        }
                        for i, card_field in enumerate(self.combo_card_fields):
                            if i < card_count:
                                combo_kwargs[card_field] = card_list[i]
                        new_combo = Combo.objects.create(
                            **combo_kwargs
                        )
                        print(f"Added combo id={combo_id}")
