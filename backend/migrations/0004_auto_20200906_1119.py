# Generated by Django 3.1.1 on 2020-09-06 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_group_homework_judgement_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='stuid',
            field=models.CharField(max_length=10, verbose_name='学号'),
        ),
        migrations.AlterField(
            model_name='user',
            name='stuname',
            field=models.CharField(blank=True, max_length=255, verbose_name='姓名'),
        ),
    ]