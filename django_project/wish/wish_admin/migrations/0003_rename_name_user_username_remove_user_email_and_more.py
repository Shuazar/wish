# Generated by Django 4.0.5 on 2022-06-11 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wish_admin', '0002_alter_purchase_receiver'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.AddField(
            model_name='user',
            name='fullname',
            field=models.CharField(max_length=100, null=True, verbose_name='Full name'),
        ),
    ]
