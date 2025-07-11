# Generated by Django 5.1.7 on 2025-07-03 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Postac',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imie', models.CharField(max_length=100)),
                ('rasa', models.CharField(max_length=50)),
                ('klasa', models.CharField(max_length=50)),
                ('hp', models.IntegerField(default=0)),
                ('max_hp', models.IntegerField(default=0)),
                ('sila', models.IntegerField(default=0)),
                ('zrecznosc', models.IntegerField(default=0)),
                ('wytrzymalosc', models.IntegerField(default=0)),
                ('inteligencja', models.IntegerField(default=0)),
                ('charyzma', models.IntegerField(default=0)),
                ('doswiadczenie', models.IntegerField(default=0)),
                ('poziom', models.IntegerField(default=1)),
                ('exp_do_nastepnego_poziomu', models.IntegerField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='Przeciwnik',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=100)),
                ('hp', models.IntegerField()),
                ('max_hp', models.IntegerField()),
                ('sila', models.IntegerField()),
                ('zrecznosc', models.IntegerField()),
                ('exp_do_pokonania', models.IntegerField(default=0)),
            ],
        ),
    ]
