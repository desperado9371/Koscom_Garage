# Generated by Django 2.0.13 on 2020-03-04 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Furits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('descript', models.TextField()),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('cdate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]