# Generated by Django 4.0.5 on 2022-06-25 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_ID', models.PositiveIntegerField()),
                ('board_message', models.CharField(max_length=5000)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indivisual_ID', models.PositiveIntegerField()),
                ('dest_ID', models.PositiveIntegerField()),
                ('message', models.CharField(max_length=2000)),
                ('read_status', models.PositiveIntegerField()),
                ('send_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_ID', models.PositiveIntegerField()),
                ('opinion_message', models.CharField(max_length=2000)),
                ('send_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]