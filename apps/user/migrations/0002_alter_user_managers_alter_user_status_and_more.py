# Generated by Django 5.1.1 on 2024-09-15 13:18

import apps.user.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', apps.user.managers.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('DELETED', 'DELETED'), ('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE'), ('DISABLED', 'DISABLED')], default='ACTIVE'),
        ),
        migrations.AlterField(
            model_name='user',
            name='subscription_type',
            field=models.CharField(blank=True, choices=[('MEMBER', 'Member'), ('PREMIUM', 'Premium')], null=True),
        ),
    ]
