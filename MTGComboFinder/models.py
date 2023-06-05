from django.db import models


class CardSupertype(models.Model):
    name = models.CharField(max_length=64, db_index=True)

    def __str__(self):
        return self.name


class CardType(models.Model):
    name = models.CharField(max_length=64, db_index=True)

    def __str__(self):
        return self.name


class CardSubtype(models.Model):
    name = models.CharField(max_length=64, db_index=True)

    def __str__(self):
        return self.name


class Keyword(models.Model):
    name = models.CharField(max_length=64, db_index=True)

    def __str__(self):
        return self.name


class CardTag(models.Model):
    tag = models.CharField(max_length=32)

    def __str__(self):
        return self.tag


class Card(models.Model):
    is_red = models.BooleanField(db_index=True)
    is_green = models.BooleanField(db_index=True)
    is_blue = models.BooleanField(db_index=True)
    is_white = models.BooleanField(db_index=True)
    is_black = models.BooleanField(db_index=True)
    count_in_arena_collection = models.IntegerField(db_index=True)
    converted_mana_cost = models.IntegerField()
    keywords = models.ManyToManyField(Keyword, related_name="card_keyword")
    name = models.CharField(max_length=64, db_index=True, unique=True)
    power = models.CharField(max_length=3, db_index=True)
    toughness = models.CharField(max_length=3, db_index=True)
    full_type_name = models.CharField(max_length=64)
    supertypes = models.ManyToManyField(CardSupertype, related_name="card_supertype")
    types = models.ManyToManyField(CardType, related_name='card_type')
    subtypes = models.ManyToManyField(CardSubtype, related_name='card_subtype')
    rules_text = models.TextField(db_index=True)
    front_image_uri = models.URLField(null=True)
    back_image_uri = models.URLField(null=True)
    tags = models.ManyToManyField(CardTag, related_name='card_tag')

    def __str__(self):
        return self.name


class Combo(models.Model):
    combo_id = models.IntegerField(db_index=True, unique=True)
    card_a = models.ForeignKey(Card, related_name='card_a', on_delete=models.CASCADE)
    card_b = models.ForeignKey(Card, related_name='card_b', on_delete=models.CASCADE)
    card_c = models.ForeignKey(Card, related_name='card_c', on_delete=models.CASCADE, null=True)
    card_d = models.ForeignKey(Card, related_name='card_d', on_delete=models.CASCADE, null=True)
    combo_card_count = models.IntegerField(db_index=True)

    def __str__(self):
        return f"[{self.card_a}], [{self.card_b}], [{self.card_c}], [{self.card_d}]"


class Deck(models.Model):
    name = models.CharField(max_length=64, db_index=True)
    is_red = models.BooleanField(db_index=True)
    is_green = models.BooleanField(db_index=True)
    is_blue = models.BooleanField(db_index=True)
    is_white = models.BooleanField(db_index=True)
    is_black = models.BooleanField(db_index=True)

    def __str__(self):
        deck_list = list(map(lambda x: f"{x.quantity} {x.card.name}", DeckEntry.objects.filter(deck=self)))
        deck_list_str = "\n".join(deck_list)
        return f"{self.name}\n{deck_list_str}"


class DeckEntry(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, related_name='deck_card', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} {self.card.name}"


