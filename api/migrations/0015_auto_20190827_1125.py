# Generated by Django 2.2.1 on 2019-08-27 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20190825_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='supplier',
            field=models.IntegerField(blank=True, choices=[(1, '戴尔'), (2, '苹果'), (3, '')], default=3, null=True, verbose_name='供应商'),
        ),
    ]
