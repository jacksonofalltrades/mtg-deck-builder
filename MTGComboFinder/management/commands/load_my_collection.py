import glob
import os
import re

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from MTGComboFinder.models import *


class Command(BaseCommand):
    help = "Load collected cards"

    def handle(self, *args, **options):
        line_pat = r'^(\d+)\s([^(]+)\s.+'
        cpat = re.compile(line_pat)
        collection_paths = glob.glob(os.path.join(settings.BASE_DIR,
                                                  "MTGComboFinder",
                                                  "data",
                                                  "collection_exports",
                                                  "*"))
        for path in collection_paths:
            with open(path, 'r') as f:
                for line in f:
                    m = cpat.match(line.strip())
                    if m:
                        qty, card_name = m.groups()
                        query = Card.objects.filter(name=card_name)
                        if query.exists():
                            card = query.first()
                            card.count_in_arena_collection = qty
                            card.save()
                        else:
                            # Try starts with
                            query = Card.objects.filter(name__startswith=card_name)
                            if query.exists():
                                card = query.first()
                                card.count_in_arena_collection = qty
                                card.save()
                            else:
                                self.stdout.write(f"Cannot find card named=[{card_name}], skipping.")
                    else:
                        self.stdout.write(f"Could not find a match for line={line}")




