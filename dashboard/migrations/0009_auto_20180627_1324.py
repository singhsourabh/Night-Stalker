# Generated by Django 2.0.6 on 2018-06-27 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20180626_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cc',
            name='userid',
        ),
        migrations.RemoveField(
            model_name='cf',
            name='userid',
        ),
        migrations.RemoveField(
            model_name='sj',
            name='userid',
        ),
    ]
