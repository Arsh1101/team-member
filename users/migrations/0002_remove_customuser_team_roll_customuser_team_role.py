# Generated by Django 4.1.6 on 2023-02-04 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='team_roll',
        ),
        migrations.AddField(
            model_name='customuser',
            name='team_role',
            field=models.CharField(choices=[('Admin', 'Can delete members'), ('Regular', "Can't delete members")], default='Regular', max_length=7, verbose_name='Team Role'),
        ),
    ]
