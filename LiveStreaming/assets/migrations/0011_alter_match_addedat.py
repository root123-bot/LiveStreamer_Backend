# Generated by Django 3.2 on 2023-02-20 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0010_match_addedat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='addedAt',
            field=models.PositiveBigIntegerField(default=1676920585767.5293),
        ),
    ]