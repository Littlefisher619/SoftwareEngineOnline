# Generated by Django 3.1.1 on 2020-09-10 17:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_auto_20200910_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judgement',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='judgement_user', to=settings.AUTH_USER_MODEL, verbose_name='对应学生'),
        ),
    ]
