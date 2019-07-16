# Generated by Django 2.2.1 on 2019-07-10 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=64)),
                ('code', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name_plural': '操作表',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=64)),
                ('url', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name_plural': 'url表',
            },
        ),
        migrations.CreateModel(
            name='Permission2Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Action')),
                ('p', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Permission')),
            ],
            options={
                'verbose_name_plural': '权限表',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='User2Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Role')),
                ('u', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User')),
            ],
            options={
                'verbose_name_plural': '用户分配角色',
            },
        ),
        migrations.CreateModel(
            name='Permission2Action2Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p2a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Permission2Action')),
                ('r', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Role')),
            ],
            options={
                'verbose_name_plural': '角色分配权限',
            },
        ),
    ]