# Generated by Django 3.2 on 2022-12-03 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0006_alter_match_matchid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='short_name',
            field=models.CharField(max_length=4, unique=True),
        ),
    ]
