# Generated by Django 2.0.5 on 2018-05-07 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myHome', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='web_document',
            name='title',
            field=models.TextField(max_length=100),
        ),
    ]
