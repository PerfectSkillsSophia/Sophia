# Generated by Django 4.1.1 on 2023-03-13 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='allAssessment',
            fields=[
                ('assId', models.AutoField(primary_key=True, serialize=False)),
                ('assessmentName', models.CharField(max_length=255, null=True)),
                ('assessmentDes', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quostion', models.CharField(max_length=255, null=True)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.allassessment')),
            ],
        ),
    ]
