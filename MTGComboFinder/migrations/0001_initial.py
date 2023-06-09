# Generated by Django 2.0 on 2023-05-09 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_red', models.BooleanField(db_index=True)),
                ('is_green', models.BooleanField(db_index=True)),
                ('is_blue', models.BooleanField(db_index=True)),
                ('is_white', models.BooleanField(db_index=True)),
                ('is_black', models.BooleanField(db_index=True)),
                ('converted_mana_cost', models.IntegerField()),
                ('name', models.CharField(max_length=64)),
                ('power', models.IntegerField()),
                ('toughness', models.IntegerField()),
                ('full_type_name', models.CharField(max_length=64)),
                ('rules_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CardSubtype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='CardSupertype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='CardType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='keywords',
            field=models.ManyToManyField(to='MTGComboFinder.Keyword'),
        ),
        migrations.AddField(
            model_name='card',
            name='subtypes',
            field=models.ManyToManyField(to='MTGComboFinder.CardSubtype'),
        ),
        migrations.AddField(
            model_name='card',
            name='supertypes',
            field=models.ManyToManyField(to='MTGComboFinder.CardSupertype'),
        ),
        migrations.AddField(
            model_name='card',
            name='types',
            field=models.ManyToManyField(to='MTGComboFinder.CardType'),
        ),
    ]
