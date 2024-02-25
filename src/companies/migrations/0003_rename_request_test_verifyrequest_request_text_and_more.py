# Generated by Django 4.2 on 2024-02-25 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_verifyrequest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='verifyrequest',
            old_name='request_test',
            new_name='request_text',
        ),
        migrations.AddField(
            model_name='verifyrequest',
            name='status',
            field=models.CharField(choices=[('send', 'send'), ('accept', 'accept'), ('cancel', 'cancel')], default='send', max_length=10),
        ),
    ]
