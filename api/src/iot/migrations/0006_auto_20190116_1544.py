# Generated by Django 2.1.2 on 2019-01-16 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0005_auto_20190116_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='types',
            field=models.ManyToManyField(to='iot.Type'),
        ),
    ]