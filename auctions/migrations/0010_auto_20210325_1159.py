# Generated by Django 3.1.2 on 2021-03-25 11:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20210325_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]
