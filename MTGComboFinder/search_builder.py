import os
import urllib.parse
import hashlib
import logging
import requests
from django.conf import settings
from django.db.models import QuerySet
from MTGComboFinder.models import *

logger = logging.getLogger(__name__)


class SearchBuilder:
    def __init__(self):
        self.scryfall_card_search_api_url = "https://api.scryfall.com/cards/named?exact="
        self.results_cache = set([]) # Cache based on sorted db ids of cards
        self.result_page_root = "/tmp/mtg_search_results"
        if not os.path.exists(self.result_page_root):
            os.makedirs(self.result_page_root)

    def build_html_result_item(self, card: Card) -> str:
        safe_string = urllib.parse.quote_plus(card.name)
        r = requests.get(f"{self.scryfall_card_search_api_url}{safe_string}")
        if r.status_code == 200:
            data = r.json()
            if 'object' in data:
                if 'card_faces' in data and len(data['card_faces']) > 1:
                    image_uri1 = data['card_faces'][0]['image_uris']['normal']
                    image_uri2 = data['card_faces'][1]['image_uris']['normal']
                    return f"    <div class=\"grid-item\"><img src=\"{image_uri1}\" /><img src=\"{image_uri2}\" /></div>"
                else:
                    image_uri = data['image_uris']['normal']
                return f"    <div class=\"grid-item\"><img src=\"{image_uri}\" /></div>"
        return None

    def make_cache_key(self, cards: QuerySet) -> str:
        hash_key = ":".join(map(lambda x: str(x.pk), cards.order_by('pk')))
        m = hashlib.md5()
        m.update(hash_key.encode('utf-8'))
        cache_key = m.hexdigest()

        return cache_key

    def get_result_page(self, cache_key: str) -> str:
        cached_page = f"{cache_key}.html"
        return os.path.join(self.result_page_root, cached_page)

    def build_results_page(self, cards: QuerySet) -> str:
        """
        :param cards: cards to build result page for
        :return: path to results page
        """
        cache_key = self.make_cache_key(cards)
        results_page = self.get_result_page(cache_key)
        if cache_key in self.results_cache:
            return results_page

        all_items = []
        for card in cards:
            item = self.build_html_result_item(card)
            if item is not None:
                all_items.append(item)
            else:
                logger.warning(f"Problem fetching image uri for card named={card.name}")

        page_temp = os.path.join(settings.BASE_DIR, "templates", "results_page_template.html")
        page_contents = ""
        with open(page_temp, 'r') as f:
            page_contents = f.read()

        page_filled = page_contents % "\n".join(all_items)
        with open(results_page, 'w') as f:
            f.write(page_filled)

        self.results_cache.add(cache_key)

        return results_page



