# Generated by Django 2.2.4 on 2020-01-21 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='authorization',
            field=models.CharField(choices=[('true', 'true'), ('false', 'false')], default='false', max_length=5),
        ),
    ]
