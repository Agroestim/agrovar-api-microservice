# Generated by Django 5.0.1 on 2024-05-19 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_varietyoptionsmodel_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationOptionsModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Identificador unico')),
                ('region_name', models.CharField(max_length=50, verbose_name='Nombre de la region')),
            ],
            options={
                'db_table': 'location_options',
                'db_table_comment': 'This model stores the campaing locations',
            },
        ),
        migrations.AlterModelTableComment(
            name='campaigndocumentsmodel',
            table_comment='This model stores the capaign documents',
        ),
        migrations.AlterModelTableComment(
            name='varietyoptionsmodel',
            table_comment='This model stores the crop varieties',
        ),
    ]