# Generated by Django 4.0.6 on 2022-07-23 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0008_alter_reaction_reaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='space',
            name='tag_line',
            field=models.CharField(blank=True, default='', max_length=75, null=True),
        ),
    ]