# Generated by Django 3.2.19 on 2023-05-11 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MTGComboFinder', '0006_combo_combo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='combo',
            name='combo_id',
            field=models.IntegerField(db_index=True, unique=True),
        ),
    ]
