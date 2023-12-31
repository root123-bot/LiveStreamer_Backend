# Generated by Django 3.2 on 2023-01-26 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0008_alter_match_starting_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='position_name',
            field=models.CharField(choices=[('GK', 'GK'), ('CB', 'CB'), ('RB', 'RB'), ('LB', 'LB'), ('DM', 'DM'), ('LW', 'LW'), ('RW', 'RW'), ('AM', 'AM'), ('CM', 'CM'), ('DM', 'DM'), ('S', 'S'), ('FW', 'FW'), ('CF', 'CF')], max_length=5),
        ),
        migrations.CreateModel(
            name='TeamManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=400)),
                ('last_name', models.CharField(max_length=400)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('team', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.team')),
            ],
        ),
    ]
