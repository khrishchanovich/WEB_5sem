# Generated by Django 4.2.1 on 2023-09-10 17:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0008_alter_insuranceagent_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archived', models.BooleanField(default=True, verbose_name='Архив')),
                ('title', models.CharField(max_length=100, verbose_name='Название купона')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание вакансии')),
            ],
        ),
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0, message='Рейтинг должен быть не меньше 0.'), django.core.validators.MaxValueValidator(5, message='Рейтинг должен быть не больше 5.')], verbose_name='Рейтинг')),
                ('feedback', models.TextField(blank=True, null=True, verbose_name='Отзыв')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
            ],
        ),
    ]