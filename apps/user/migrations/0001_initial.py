# Generated by Django 4.2.3 on 2023-08-03 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.CharField(max_length=24, primary_key=True, serialize=False, verbose_name='유저 아이디')),
                ('username', models.CharField(max_length=24, verbose_name='유저 이름')),
                ('password', models.CharField(max_length=128, verbose_name='유저 비밀번호')),
                ('team', models.CharField(max_length=24, verbose_name='유저 소속 팀')),
            ],
            options={
                'verbose_name': '유저 테이블',
                'db_table': 'user',
            },
        ),
    ]
