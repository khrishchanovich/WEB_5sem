# Generated by Django 4.2.1 on 2023-09-10 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_alter_faq_options_insuranceagent_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insuranceagent',
            name='photo',
            field=models.ImageField(null=True, upload_to='static/mainapp/images/agent', verbose_name='Фото'),
        ),
    ]
