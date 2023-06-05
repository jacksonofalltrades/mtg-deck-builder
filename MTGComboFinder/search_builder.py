import logging
import operator
from functools import reduce
from operator import or_, and_

from django.db.models import Q, QuerySet, Count, F
from django.db.models.functions import Length

from MTGComboFinder.models import Card, CardTag

logger = logging.getLogger(__name__)


class CardSearchBuilder:
    TAG_DRAW = 'Draw'
    TAG_REMOVAL = 'Removal'
    TAG_RAMP = 'Ramp'

    def __init__(self):
        self.red = Q(is_red=True)
        self.green = Q(is_green=True)
        self.blue = Q(is_blue=True)
        self.black = Q(is_black=True)
        self.white = Q(is_white=True)

    def owned(self):
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

    def rm_chaff(self):
        """
        Remove weird card types that are not used in normal formats

        'Scheme', 'Plane', 'Conspiracy', 'Vanguard', 'Dungeon', 'Phenomenon',

        """
        return operator.and_(
            ~Q(types__name__in=['Scheme', 'Plane', 'Conspiracy', 'Vanguard', 'Dungeon', 'Phenomenon']),
            ~Q(supertypes__name__in=['Ongoing'])
        )

    def text_re(self, regex: str):
        return Q(rules_text__regex=regex)

    def removal(self):
        return operator.or_(
            Q(rules_text__contains="\nDestroy"),
            Q(rules_text__contains="\nExile"),
            Q(rules_text__contains="destroy target"),
            Q(rules_text__contains="exile target"),
            Q(rules_text__contains="destroy all"),
            Q(rules_text__contains="exile all")
        )

    def card_draw(self):
        return operator.and_(
            operator.or_(
                Q(rules_text__contains="\nDraw"),
                Q(rules_text__icontains="draws")
            ),
            ~Q(rules_text__icontains="controller draws"))

    def ramp(self):
        return operator.or_(
            Q(rules_text__contains="Add"),
            Q(rules_text__iregex=r"create\s.+treasure token"),
            Q(rules_text__iregex=r"search\s.+\sfor\s.+land"),
        )

    def apply_card_tags(self, base_query: QuerySet) -> None:
        """
        This method is idempotent and can be applie repeatedly.
        Doing so will clear old tag relationships and recreate based on latest queries
        :param base_query:
        :return:
        """
        # Clear tags first if we are updating this
        ramp_tag = CardTag.objects.get(tag=self.TAG_RAMP)
        ramp_tag.card_tag.clear()
        ramp_cards = base_query.filter(self.ramp())
        ramp_tag.card_tag.add(*ramp_cards)

        draw_tag = CardTag.objects.get(tag=self.TAG_DRAW)
        draw_tag.card_tag.clear()
        draw_cards = base_query.filter(self.card_draw())
        draw_tag.card_tag.add(*draw_cards)

        removal_tag = CardTag.objects.get(tag=self.TAG_REMOVAL)
        removal_tag.card_tag.clear()
        removal_cards = base_query.filter(self.removal())
        removal_tag.card_tag.add(*removal_cards)

    def calculate_card_quality_weight(self, base_query: QuerySet):
        """
        NOTE: Don't use values_list if you want to be able to see names of each annotation in query results
        1 point for card draw
            annotate(draw_points=Count('tags', filter=Q(tags__name='Draw')))

        1 point for removal
            annotate(removal_points=Count('tags', filter=Q(tags__name='Removal')))

        1 point ramp
            annotate(ramp_points=Count('tags', filter=Q(tags__name='Ramp')))

        -1 point for each CMC cost > 3
            annotate(cost_points=3-F('converted_mana_cost'))

        1 point for each keyword ability
            annotate(keyword_points=Count('keywords'))

        0.2 points for each multiple of 5 > 5 for rules text char count
            annotate(ability_points=(Length('rules_text') - 5)/5 *0.2)

        Total weight
        annotate(
            card_weight=Count('tags', filter=Q(tags__name='Draw'))
                + Count('tags', filter=Q(tags__name='Removal'))
                + Count('tags', filter=Q(tags__name='Ramp'))
                + 3-F('converted_mana_cost')
                + Count('keywords')
                + (Length('rules_text') - 5)/5 *0.2)
        )
        :return:
        """
        return base_query.annotate(
            card_weight=(
                    Count('tags', filter=Q(tags__name='Draw')) +
                    Count('tags', filter=Q(tags__name='Removal')) +
                    Count('tags', filter=Q(tags__name='Ramp')) +
                    3 - F('converted_mana_cost') +
                    Count('keywords') +
                    ((Length('rules_text') - 5) / 5 * 0.2)
            )
        )






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

    def color_filters(self, color_include_str: str, color_exclude_str: str):
        card_count_card_col_map = {
            '2': ['card_a', 'card_b'],
            '3': ['card_a', 'card_b', 'card_c'],
            '4': ['card_a', 'card_b', 'card_c', 'card_d']
        }

        str_to_filt_name = {
            'R': 'is_red',
            'G': 'is_green',
            'U': 'is_blue',
            'W': 'is_white',
            'B': 'is_black'
        }

        def filt_key(map_key: str) -> bool:
            return str_to_filt_name[map_key]

        def make_color_filter_map(card_count_key: str, filter_key_list_iter: iter, filt_val_bool: bool):
            def make_ored_color_filter_list():
                card_col_name_list = card_count_card_col_map[card_count_key]

                return map(lambda x: reduce(operator.or_,
                                            map(lambda y: Q(**{f"{x}__{y}": filt_val_bool}),
                                                filter_key_list_iter)),
                           card_col_name_list)
            return reduce(operator.and_, make_ored_color_filter_list())

        def make_included_color_filter_list(card_count_key, included_color_list):
            if included_color_list is not None and len(included_color_list) > 0:
                filter_key_list_iter = list(map(filt_key, included_color_list))
                return make_color_filter_map(card_count_key, filter_key_list_iter, True)
            else:
                return []

        def make_excluded_color_filter_list(card_count_key, excluded_color_list):
            if excluded_color_list is not None and len(excluded_color_list) > 0:
                filter_key_list_iter = list(map(filt_key, excluded_color_list))
                return make_color_filter_map(card_count_key, filter_key_list_iter, False)
            else:
                return []

        def make_full_color_filter_list(card_count, included_color_list, excluded_color_list):
            full_list = []
            inc = make_included_color_filter_list(card_count, included_color_list)
            exc = make_excluded_color_filter_list(card_count, excluded_color_list)
            if len(inc) > 0:
                full_list.append(inc)
            if len(exc) > 0:
                full_list.append(exc)
            return full_list

        z = make_full_color_filter_list('2', color_include_str, color_exclude_str)
        print(z)

        return dict(map(lambda x:
                        (x,
                         base_query_dict[x].filter(
                             *make_full_color_filter_list(
                                 x, color_include_str, color_exclude_str
                             )
                         )
                         ),
                         base_query_dict.keys()))
