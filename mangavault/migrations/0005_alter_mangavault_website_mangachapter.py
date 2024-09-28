# Generated by Django 5.0.9 on 2024-09-28 17:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('harvesters', '0002_alter_harvester_harvest_type'),
        ('mangavault', '0004_alter_mangagenre_related_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mangavault',
            name='website',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='manga_source', to='harvesters.harvester'),
        ),
        migrations.CreateModel(
            name='MangaChapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_title', models.CharField(max_length=100)),
                ('chapter_url', models.URLField(unique=True)),
                ('chapter_number', models.PositiveSmallIntegerField(max_length=5)),
                ('is_new', models.BooleanField(default=False)),
                ('is_latest', models.BooleanField(default=False)),
                ('is_trending', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('manga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manga_chapter', to='mangavault.mangavault')),
            ],
        ),
    ]
