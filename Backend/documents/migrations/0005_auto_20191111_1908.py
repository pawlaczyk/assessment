# Generated by Django 2.2.6 on 2019-11-11 18:08

from django.db import migrations, models
import documents.models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_auto_20191111_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_file',
            field=models.FileField(blank=True, upload_to=documents.models.answer_upload_to),
        ),
        migrations.AlterField(
            model_name='document',
            name='document_file',
            field=models.FileField(blank=True, upload_to=documents.models.document_upload_to),
        ),
    ]
