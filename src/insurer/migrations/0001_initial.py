# Generated by Django 2.2.4 on 2020-01-21 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_user_id', models.CharField(max_length=50)),
                ('benefit', models.CharField(max_length=50)),
                ('currency', models.CharField(max_length=50)),
                ('amount', models.IntegerField()),
                ('authorization', models.CharField(choices=[('true', 'true'), ('false', 'false')], default='False', max_length=5)),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp')),
            ],
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_user_id', models.CharField(max_length=50)),
                ('benefit', models.CharField(max_length=50)),
                ('currency', models.CharField(max_length=50)),
                ('total_max_amount', models.IntegerField()),
            ],
        ),
    ]