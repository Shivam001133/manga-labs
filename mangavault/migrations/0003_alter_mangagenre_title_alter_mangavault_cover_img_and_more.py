# Generated by Django 5.0.9 on 2024-09-27 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mangavault', '0002_mangagenre_mangavault_category_mangavault_is_new_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mangagenre',
            name='title',
            field=models.CharField(max_length=25, unique=True),
        ),
        migrations.AlterField(
            model_name='mangavault',
            name='cover_img',
            field=models.URLField(unique=True),
        ),
        migrations.AlterField(
            model_name='mangavault',
            name='vault_url',
            field=models.URLField(unique=True),
        ),
    ]
