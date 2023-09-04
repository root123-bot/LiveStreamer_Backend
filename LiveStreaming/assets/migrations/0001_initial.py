# Generated by Django 3.2 on 2022-11-23 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('address', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('short_name', models.CharField(max_length=4)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('stadium', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.venue')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=400)),
                ('last_name', models.CharField(max_length=400)),
                ('number', models.PositiveIntegerField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('starter', models.BooleanField(default=False)),
                ('position_type', models.CharField(choices=[('Goalkeeper', 'Goalkeeper'), ('Defender', 'Defender'), ('Midfielder', 'Midfielder'), ('Forward', 'Forward')], max_length=20)),
                ('position_name', models.CharField(choices=[('GK', 'GK'), ('CB', 'CB'), ('RB', 'RB'), ('DM', 'DM'), ('LW', 'LW'), ('RW', 'RW'), ('AM', 'AM'), ('CM', 'CM'), ('DM', 'DM'), ('S', 'S'), ('CF', 'CF')], max_length=5)),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.team')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_name', models.CharField(max_length=400)),
                ('starting_time', models.DateTimeField()),
                ('is_completed', models.BooleanField(default=False)),
                ('matchId', models.CharField(max_length=6)),
                ('extraTime', models.BooleanField(default=False)),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away', to='assets.team')),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.competition')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home', to='assets.team')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.venue')),
            ],
        ),
        migrations.AddField(
            model_name='competition',
            name='teams',
            field=models.ManyToManyField(blank=True, null=True, to='assets.Team'),
        ),
    ]
