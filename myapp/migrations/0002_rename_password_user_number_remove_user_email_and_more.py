# Generated by Django 4.2.4 on 2023-09-27 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='password',
            new_name='number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.AddField(
            model_name='user',
            name='message',
            field=models.TextField(default='-'),
        ),
    ]
