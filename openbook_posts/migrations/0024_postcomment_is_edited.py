# Generated by Django 2.2rc1 on 2019-03-27 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openbook_posts', '0023_auto_20190317_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='is_edited',
            field=models.BooleanField(default=False),
        ),
    ]
