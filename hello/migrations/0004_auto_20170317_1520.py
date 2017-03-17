# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-17 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_answer_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_clean',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='txt_clean',
            field=models.TextField(blank=True, null=True),
        ),
    ]