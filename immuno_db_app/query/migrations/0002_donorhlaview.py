# Generated by Django 4.0.6 on 2022-09-02 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonorHlaView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all_hla_alleles', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'donor_hla_view',
                'managed': False,
            },
        ),
    ]