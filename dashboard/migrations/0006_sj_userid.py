# Generated by Django 2.0.6 on 2018-06-26 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_remove_sj_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='sj',
            name='userid',
            field=models.CharField(max_length=25, null=True),
        ),
    ]