# Generated by Django 2.2.12 on 2020-05-06 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpm', '0008_advisory_pkg_sumtype_as_int'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rpmrepository',
            name='last_sync_revision_number',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
