# Generated by Django 2.0.6 on 2018-07-22 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_auto_20180719_0618'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='UserDetail',
        ),
    ]
