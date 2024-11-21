# Generated by Django 4.0.6 on 2023-07-06 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0002_donorhlaview'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeptideModsView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peptide_modifications', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'peptide_mods_view',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProteinMatchesView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniprot_ids', models.TextField(blank=True, null=True)),
                ('protein_names', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'protein_matches_view',
                'managed': False,
            },
        ),
    ]