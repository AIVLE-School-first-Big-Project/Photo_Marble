# Generated by Django 3.2 on 2022-04-20 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20220419_2343'),
    ]

    operations = [
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('location_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Locations',
            },
        ),
    ]
