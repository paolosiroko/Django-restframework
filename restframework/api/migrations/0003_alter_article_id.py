# Generated by Django 4.0.4 on 2022-05-27 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_article_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]