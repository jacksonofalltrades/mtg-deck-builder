import os

from django.conf import settings
from pprint import pformat
from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from MTGComboFinder.models import Combo, Card


class Command(BaseCommand):
    combo_card_fields = ['card_a', 'card_b', 'card_c', 'card_d']

    def add_arguments(self, parser):
        parser.add_argument("--include-colors", "-c",
                            action="store",
                            help="Specify a string including any of letters RGUBW, "
                                 "to only include the specified colors")
        parser.add_argument("--exclude-colors", "-e",
                            action="store",
                            help="Specify a string with letters RGUBW, "
                                 "to exclude specified colors. "
                                 "Specify all colors to only allow colorless cards.")
        parser.add_argument("--percent-in-collection", "-p",
                            action="store",
                            help="25% in collection means 1 out of 4 cards of a 4-card combo "
                                 "are in your collection")
        parser.add_argument("card_name", action="store",
                            help="Find combos that include the specified card name")

    @classmethod
    def collection_permutation_filter(cls, base_query_dict: dict, percent: str):
        a = Q(card_a__count_in_arena_collection__gte=1)
        b = Q(card_b__count_in_arena_collection__gte=1)
        c = Q(card_c__count_in_arena_collection__gte=1)
        d = Q(card_d__count_in_arena_collection__gte=1)

        percent_map = {
            'cards:25:2': a | b,
            'cards:25:3': a | b | c,
            'cards:25:4': a | b | c | d,
            'cards:50:2': a | b,
            'cards:50:3': (a & b) | (a & c) | (b & c),
            'cards:50:4': (a & b) | (a & c) | (a & d) | (b & c) | (b & d) | (c & d),
            'cards:75:2': a & b,
            'cards:75:3': (a & b) | (a & c) | (b & c),
            'cards:75:4': (a & b & c) | (a & b & d) | (a & c & d) | (b & c & d),
            'cards:100:2': a & b,
            'cards:100:3': a & b & c,
            'cards:100:4': a & b & c & d
        }

        percent_num = percent[0:-1]

        return dict(map(lambda x:
                   (x, base_query_dict[x].filter(percent_map[f'cards:{percent_num}:{x}'])),
                   base_query_dict.keys()))

    @classmethod
    def card_name_filter(cls, base_query_dict: dict, card_name: str):
        a = Q(card_a__name__startswith=card_name)
        b = Q(card_b__name__startswith=card_name)
        c = Q(card_c__name__startswith=card_name)
        d = Q(card_d__name__startswith=card_name)

        card_name_map = {
            '2': a | b,
            '3': a | b | c,
            '4': a | b | c | d
        }

        return dict(map(lambda x:
                        (x, base_query_dict[x].filter(card_name_map[x])),
                        base_query_dict.keys()))

    @classmethod
    def color_filters(cls, base_query_dict: dict, color_include_str: str, color_exclude_str: str):
        # str_to_filt_name = {
        #     'R': 'is_red',
        #     'G': 'is_green',
        #     'U': 'is_blue',
        #     'W': 'is_white',
        #     'B': 'is_black'
        # }
        #
        # def filt_key(map_key: str) -> bool:
        #     return str_to_filt_name[map_key]
        #
        # def make_color_filter_map(card_count_key: str, color_filt_name: str, filt_val_bool: bool):
        #     def make_filt_arg_dict(color_filt_name, filt_val_bool):
        #         return {
        #             '2': {
        #                 f"card_a__{color_filt_name}": filt_val_bool,
        #                 f"card_b__{color_filt_name}": filt_val_bool
        #             },
        #             '3': {
        #                 f"card_a__{color_filt_name}": filt_val_bool,
        #                 f"card_b__{color_filt_name}": filt_val_bool,
        #                 f"card_c__{color_filt_name}": filt_val_bool
        #             },
        #             '4': {
        #                 f"card_a__{color_filt_name}": filt_val_bool,
        #                 f"card_b__{color_filt_name}": filt_val_bool,
        #                 f"card_c__{color_filt_name}": filt_val_bool,
        #                 f"card_d__{color_filt_name}": filt_val_bool
        #             }
        #         }
        #     return make_filt_arg_dict(color_filt_name, filt_val_bool)[card_count_key]
        #
        #
        # def make_included_color_filter_list(card_count_key, included_color_list):
        #     filter_map = {}
        #     for color_letter in included_color_list:
        #         filter_map.update(make_color_filter_map(card_count_key,
        #                                                 filt_key(color_letter),
        #                                                 True))
        #     return filter_map
        #
        # def make_excluded_color_filter_list(card_count, excluded_color_list):
        #     pass
        #
        # def make_full_color_filter_list(card_count, included_color_list, excluded_color_list):
        #     full_list = []
        #     full_list.extend(make_included_color_filter_list(card_count, included_color_list))
        #     full_list.extend(make_excluded_color_filter_list(card_count, excluded_color_list))
        #     return full_list
        #
        # return dict(map(lambda x:
        #                     (x, base_query_dict[x].filter(*make_full_color_filter_list(
        #                         x, color_include_str, color_exclude_str
        #                     )),
        #                     base_query_dict.keys())))



        """
        make_included_color_filter_list(card_count, included_color_list):
            pass

        make_excluded_color_filter_list(card_count, excluded_color_list):
            pass

        make_full_color_filter_list(card_count, included_color_list, excluded_color_list)
            pass

        return dict(map(lambda x:
                            (x, base_query_dict[x].filter(*make_full_color_filter_list()),
                            base_query_dict.keys()))

        Final filter looks like this, e.g. for 4 card combo and RG included and UW excluded:
        filter(
            Q(card_a__is_red=True)|Q(card_a__is_green=True),
            Q(card_b__is_red=True)|Q(card_b__is_green=True),
            Q(card_c__is_red=True)|Q(card_c__is_green=True),
            Q(card_d__is_red=True)|Q(card_d__is_green=True),
            Q(card_a__is_blue=False)|Q(card_a__is_white=False),
            Q(card_b__is_blue=False)|Q(card_b__is_white=False),
            Q(card_c__is_blue=False)|Q(card_c__is_white=False),
            Q(card_d__is_blue=False)|Q(card_d__is_white=False),
        """

        #     color_filter_map = dict(
        #         map(lambda x: (x, Q(**make_filt_arg_dict(filt_key(x), filt_val(x)))), [
        #             'R:i', 'G:i', 'U:i', 'B:i', 'W:i',
        #             'R:e', 'G:e', 'U:e', 'B:e', 'W:e',
        #         ])
        #     )
        #
        # def make_color_map_keys(user_color_str: str, inc_ex_key: str):
        #     return list(map(lambda x: f"{x}:{inc_ex_key}", user_color_str))
        #
        # if color_include_str:
        #     color_incl_map_keys = make_color_map_keys(color_include_str, 'i')
        # else:
        #     color_incl_map_keys = []
        #
        # if color_exclude_str:
        #     color_ex_map_keys = make_color_map_keys(color_exclude_str, 'e')
        # else:
        #     color_ex_map_keys = []
        #
        # all_keys = color_incl_map_keys + color_ex_map_keys
        # final_filter_list = []
        # for color_key in all_keys:
        #     final_filter_list.append(color_filter_map[color_key])
        #
        # if len(final_filter_list) > 0:
        #     return dict(map(lambda x:
        #                     (x, base_query_dict[x].filter(*final_filter_list)),
        #                     base_query_dict.keys()))
        # else:
        #     print(f"No color filters included")
        #     return base_query_dict
        print(f"Color filters not yet implemented, ignoring")
        return base_query_dict

    @classmethod
    def sum_query_result_counts(cls, query_dict: dict) -> int:
        return sum(map(lambda x: query_dict[x].count(), query_dict.keys()))

    def handle(self, *args, **options):
        combos_2card_query = Combo.objects.filter(
            combo_card_count=2)
        combos_3card_query = Combo.objects.filter(
            combo_card_count=3)
        combos_4card_query = Combo.objects.filter(
            combo_card_count=4)

        base_query_dict = {
            '2': combos_2card_query,
            '3': combos_3card_query,
            '4': combos_4card_query
        }

        # Apply card name first, since no point doing other filters if no results
        card_name = options['card_name']
        base_query_dict = self.card_name_filter(base_query_dict, card_name)
        if self.sum_query_result_counts(base_query_dict) <= 0:
            print(f"No combos found with card [{card_name}]")
            exit(1)

        collect_filtered = {}

        # Apply collection overlap filters
        percent_in_coll = options['percent_in_collection']
        if percent_in_coll is not None:
            print(f"Finding combos having {percent_in_coll} of cards in your collection.")
            collect_filtered = self.collection_permutation_filter(base_query_dict, percent_in_coll)
            if self.sum_query_result_counts(collect_filtered) <= 0:
                print(f"No combos found with card [{card_name}] having "
                      f"{percent_in_coll} of cards in your collection.")
                exit(1)
        else:
            collect_filtered = base_query_dict
            print("No collection filters included")

        include_colors_str = options['include_colors']
        exclude_colors_str = options['exclude_colors']

        # Validate no overlap
        if include_colors_str is not None and exclude_colors_str is not None:
            valid_letters = set(['R', 'G', 'B', 'U', 'W'])

            a = set(include_colors_str)
            if not a.issubset(valid_letters):
                print("Your include color arg contains invalid letters")
                exit(1)

            b = set(exclude_colors_str)
            if not b.issubset(valid_letters):
                print("Your exclude color arg contains invalid letters")
                exit(1)

            if len(a.intersection(b)) > 0:
                print(f"Your include and exclude color lists cannot overlap.")
                exit(1)

        # Apply filters
        color_filtered_dict = self.color_filters(collect_filtered,
                                                 include_colors_str, exclude_colors_str)
        if self.sum_query_result_counts(color_filtered_dict) <= 0:
            print(f"Your query did not return any results.")
        else:
            for card_count, query in color_filtered_dict.items():
                query_result_list = list(query)
                print(f"{card_count}-card combos found: {pformat(query_result_list)}")







