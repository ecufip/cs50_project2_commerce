# Generated by Django 3.1.2 on 2021-03-09 14:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210223_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='pic_url',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.CharField(default=django.utils.timezone.now, max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='listing',
            name='min_starting_bid',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
