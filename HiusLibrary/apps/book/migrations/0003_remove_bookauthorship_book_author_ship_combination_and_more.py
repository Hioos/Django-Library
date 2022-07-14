# Generated by Django 4.0.5 on 2022-07-13 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='bookauthorship',
            name='book_author_ship_combination',
        ),
        migrations.RemoveField(
            model_name='bookauthorship',
            name='bookauthorship_authorRole',
        ),
        migrations.AddConstraint(
            model_name='bookauthorship',
            constraint=models.UniqueConstraint(fields=('bookauthorship_bookId', 'bookauthorship_authorId'), name='book_author_ship_combination'),
        ),
    ]
