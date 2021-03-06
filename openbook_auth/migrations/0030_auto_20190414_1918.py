# Generated by Django 2.2 on 2019-04-14 17:18

from django.db import migrations, models
import openbook_common.validators


class Migration(migrations.Migration):

    dependencies = [
        ('openbook_auth', '0029_auto_20190311_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(db_index=True, max_length=192, validators=[openbook_common.validators.name_characters_validator], verbose_name='name'),
        ),
    ]
