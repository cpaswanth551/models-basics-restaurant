# Generated by Django 5.1.3 on 2024-11-28 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_restaurant_capacity'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='nickname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]