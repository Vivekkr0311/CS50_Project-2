# Generated by Django 3.0.8 on 2020-09-16 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20200916_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='watch_list',
            name='product_name',
            field=models.ManyToManyField(blank=True, related_name='Watch_List', to='auctions.Product'),
        ),
    ]