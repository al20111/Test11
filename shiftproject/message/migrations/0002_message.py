# Generated by Django 4.0.5 on 2022-07-03 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indivisual_ID', models.PositiveIntegerField()),
                ('dest_ID', models.PositiveIntegerField()),
                ('message', models.CharField(max_length=1000)),
                ('read_status', models.PositiveIntegerField()),
                ('send_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
