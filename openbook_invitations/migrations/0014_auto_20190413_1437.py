# Generated by Django 2.2 on 2019-04-13 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('openbook_invitations', '0013_auto_20190410_1534'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinvite',
            old_name='invited_date',
            new_name='created',
        ),
    ]
