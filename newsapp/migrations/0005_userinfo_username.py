# Generated by Django 4.0.3 on 2023-09-25 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0004_alter_userinfo_user_quota'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='username',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
