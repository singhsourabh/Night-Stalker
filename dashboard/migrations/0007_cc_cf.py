# Generated by Django 2.0.6 on 2018-06-26 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_sj_userid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=25, null=True)),
                ('date', models.DateField()),
                ('handle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.User')),
            ],
        ),
        migrations.CreateModel(
            name='Cf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=25, null=True)),
                ('date', models.DateField()),
                ('handle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.User')),
            ],
        ),
    ]