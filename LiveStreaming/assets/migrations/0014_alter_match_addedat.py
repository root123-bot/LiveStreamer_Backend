# Generated by Django 3.2 on 2023-02-21 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0013_alter_match_addedat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='addedAt',
            field=models.PositiveBigIntegerField(default=1676995026111),
        ),
    ]
