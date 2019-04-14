# Generated by Django 2.2 on 2019-04-14 17:53

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('openbook_connections', '0012_auto_20190414_1909'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='connection',
            index_together={('target_user', 'id'), ('target_user', 'target_connection')},
        ),
    ]
