# Generated by Django 3.2 on 2022-05-01 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_user_profile_s3_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='latitude',
            field=models.DecimalField(decimal_places=10, max_digits=18, null=True),
        ),
        migrations.AddField(
            model_name='gallery',
            name='longitude',
            field=models.DecimalField(decimal_places=10, max_digits=18, null=True),
        ),
    ]
