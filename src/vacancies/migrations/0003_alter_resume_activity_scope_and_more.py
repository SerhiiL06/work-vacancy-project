# Generated by Django 4.2 on 2024-02-27 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_rename_request_test_verifyrequest_request_text_and_more'),
        ('vacancies', '0002_vacancy_calary_vacancy_format_work'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='activity_scope',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='companies.scoreofactivity'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='activity_scope',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.scoreofactivity'),
        ),
    ]
