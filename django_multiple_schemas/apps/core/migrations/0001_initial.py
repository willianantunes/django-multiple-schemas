# Generated by Django 3.1.7 on 2021-03-11 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('language_tag', models.CharField(max_length=20, unique=True)),
                ('language', models.CharField(blank=True, max_length=50, null=True, verbose_name='Language')),
                ('accent_or_dialect', models.CharField(blank=True, max_length=50, null=True, verbose_name='Accent/Dialect')),
                ('family', models.CharField(blank=True, max_length=50, null=True, verbose_name='Family')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]