# Generated by Django 3.2.7 on 2021-09-26 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Programa',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('num_semesters', models.PositiveIntegerField()),
                ('state', models.CharField(default='A', max_length=1)),
            ],
            options={
                'db_table': 'Candy',
            },
        ),
        migrations.CreateModel(
            name='Pensum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('uploadedFile', models.FileField(upload_to='Uploaded Files/')),
                ('date_issue', models.DateField(auto_now_add=True)),
                ('expiration_date', models.DateField(auto_now_add=True)),
                ('state', models.CharField(default='A', max_length=1)),
                ('programa_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pensum.programa')),
            ],
            options={
                'db_table': 'pensum',
            },
        ),
    ]
