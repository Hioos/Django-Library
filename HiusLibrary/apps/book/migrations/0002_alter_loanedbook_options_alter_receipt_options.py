# Generated by Django 4.0.5 on 2022-07-26 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loanedbook',
            options={'get_latest_by': ['loanedBook_id']},
        ),
        migrations.AlterModelOptions(
            name='receipt',
            options={'get_latest_by': ['receipt_id']},
        ),
    ]
