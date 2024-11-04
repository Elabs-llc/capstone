# Generated by Django 5.1.2 on 2024-11-04 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SkynexusData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=100)),
                ('temparture', models.FloatField()),
                ('description', models.CharField(max_length=150)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
