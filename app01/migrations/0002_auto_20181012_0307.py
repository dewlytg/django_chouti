# Generated by Django 2.1.1 on 2018-10-12 03:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app01.UserType'),
            preserve_default=False,
        ),
    ]
