import logging
from functools import reduce
from operator import or_, and_

from django.db.models import Q

logger = logging.getLogger(__name__)


class CardSearchBuilder:
    def __init__(self):
        self.red = Q(is_red=True)
        self.red_df = {"is_red": True}

        self.green = Q(is_green=True)
        self.green_df = {"is_green": True}

        self.blue = Q(is_blue=True)
        self.blue_df = {"is_blue": True}

        self.black = Q(is_black=True)
        self.black_df = {"is_black": True}

        self.white = Q(is_white=True)
        self.white_df = {"is_white": True}

    def owned(self, as_dict=False):
        if as_dict:
            return {"count_in_arena_collection__gte": 1}
        return Q(count_in_arena_collection__gte=1)

    def xr(self):
        return self.red & ~(self.green & self.blue & self.black & self.white)

    def xg(self):
        return self.green & ~(self.red & self.blue & self.black & self.white)

    def xu(self):
        return self.blue & ~(self.red & self.green & self.black & self.white)

    def xw(self):
        return self.white & ~(self.red & self.green & self.black & self.blue)

    def xb(self):
        return self.black & ~(self.red & self.green & self.white & self.blue)

    def text_re(self, regex: str):
        return Q(rules_text__regex=regex)


class ComboSearchBuilder(CardSearchBuilder):
    def __init__(self):
        super().__init__()
        self.card_refs = ['card_a__', 'card_b__', 'card_c__', 'card_d__']

    def any_card(self, filter_dict: dict):
        return reduce(or_, map(lambda x: Q(**dict(map(lambda y, z: (f"{x}{y}", z), filter_dict.items()))),
                               self.card_refs))

    def all_cards(self, filter_dict: dict):
        return reduce(and_, map(lambda x: Q(**dict(map(lambda y, z: (f"{x}{y}", z), filter_dict.items()))),
                                self.card_refs))

    def one_filt(self, filt_key: str, filt_val: any):
        return {filt_key: filt_val}

    def uses(self, card_name: str):
        return self.any_card(self.one_filt("name", card_name))
