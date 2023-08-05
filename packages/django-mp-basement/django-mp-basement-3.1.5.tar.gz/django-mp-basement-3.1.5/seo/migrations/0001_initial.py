# Generated by Django 2.0.6 on 2018-06-20 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='URL')),
                ('title', models.CharField(max_length=68, verbose_name='Title')),
                ('keywords', models.CharField(blank=True, max_length=100, verbose_name='Keywords')),
                ('description', models.CharField(blank=True, max_length=155, verbose_name='Description')),
                ('breadcrumb', models.CharField(blank=True, max_length=100, verbose_name='Breadcrumb')),
                ('header', models.CharField(blank=True, max_length=100, verbose_name='Header')),
                ('robots', models.CharField(blank=True, choices=[('index, follow', 'Index, Follow'), ('noindex, nofollow', 'No Index, No Follow'), ('index, nofollow', 'Index, No Follow'), ('noindex, follow', 'No Index, Follow')], default='index, follow', max_length=30, verbose_name='Robots')),
            ],
            options={
                'verbose_name': 'Page meta',
                'verbose_name_plural': 'Pages meta',
            },
        ),
    ]
