# Generated by Django 3.2.19 on 2023-06-05 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MTGComboFinder', '0009_auto_20230516_0256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='keywords',
            field=models.ManyToManyField(related_name='card_keyword', to='MTGComboFinder.Keyword'),
        ),
        migrations.AlterField(
            model_name='card',
            name='subtypes',
            field=models.ManyToManyField(related_name='card_subtype', to='MTGComboFinder.CardSubtype'),
        ),
        migrations.AlterField(
            model_name='card',
            name='supertypes',
            field=models.ManyToManyField(related_name='card_supertype', to='MTGComboFinder.CardSupertype'),
        ),
        migrations.AlterField(
            model_name='card',
            name='tags',
            field=models.ManyToManyField(related_name='card_tag', to='MTGComboFinder.CardTag'),
        ),
        migrations.AlterField(
            model_name='card',
            name='types',
            field=models.ManyToManyField(related_name='card_type', to='MTGComboFinder.CardType'),
        ),
    ]