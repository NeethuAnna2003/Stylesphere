# Generated by Django 5.1.2 on 2024-11-15 11:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('styleapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clothes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField(default=100)),
                ('image', models.ImageField(upload_to='clothes_images/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='styleapp.category')),
            ],
        ),
    ]