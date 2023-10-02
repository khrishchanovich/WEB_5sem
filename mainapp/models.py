from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class InsuranceType(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Краткое описание')
    content = models.TextField(blank=True, null=True, verbose_name='Описание вида страхования')
    rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Тариф')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Вид страхования'
        verbose_name_plural = 'Виды страхования'
        ordering = ['cat_id', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class InsuranceCompany(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название филиала')
    address = models.CharField(max_length=100, verbose_name='Адресс')
    phone_number = models.CharField(max_length=13, verbose_name='Номер телефона')
    letter_id = models.ForeignKey('Letters', on_delete=models.PROTECT, verbose_name='Начальная буква')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('agent', kwargs={'agent_slug': self.slug})

    class Meta:
        verbose_name = 'Филлиал'
        verbose_name_plural = 'Филлиалы'
        ordering = ['letter_id']


class Letters(models.Model):
    letter = models.CharField(max_length=1, verbose_name='Буква')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.letter

    def get_absolute_url(self):
        return reverse('letter', kwargs={'let_slug': self.slug})

    class Meta:
        verbose_name = 'Буква'
        verbose_name_plural = 'Буквы'
        ordering = ['letter']


class Contract(models.Model):
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    name = models.CharField(max_length=100, verbose_name='Имя')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество')
    email = models.EmailField(verbose_name='Почта')
    phone_number = models.CharField(max_length=13, verbose_name='Номер телефона')
    cat = models.ForeignKey('InsuranceType', on_delete=models.PROTECT, verbose_name='Вид страхования')
    ins_object = models.ForeignKey('InsuranceObjects', on_delete=models.PROTECT, verbose_name='Объект страхования')
    address = models.ForeignKey('InsuranceCompany', on_delete=models.PROTECT, verbose_name='Филиал работника')
    accept_terms = models.BooleanField(default=True, verbose_name='Согласие с условиями договора')
    initial_payment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Первоначальный взнос')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания', null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Клиент')

    def __str__(self):
        return self.pk

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'
        ordering = ['id']


class InsuranceAgent(models.Model):
    photo = models.ImageField(upload_to="static/mainapp/images/agent", null=True, verbose_name="Фото")
    description = models.TextField(blank=True, null=True, verbose_name='Описание услуг')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    name = models.CharField(max_length=100, verbose_name='Имя')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество')
    email = models.EmailField(verbose_name='Почта')
    phone_number = models.CharField(max_length=13, verbose_name='Номер телефона')
    address = models.ForeignKey('InsuranceCompany', on_delete=models.PROTECT, verbose_name='Филиал работника')
    income = models.DecimalField(max_digits=10, null=True, decimal_places=2, verbose_name='Доход')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Агент'
        verbose_name_plural = 'Агенты'
        ordering = ['last_name']


class InsuranceObjects(models.Model):
    name = models.CharField(max_length=100, verbose_name='Объект')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'
        ordering = ['name']


class FAQ(models.Model):
    question = models.TextField(blank=True, null=True, verbose_name='Вопрос')
    answer = models.TextField(blank=True, null=True, verbose_name='Ответ')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'


class Vacancy(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание вакансии')


class FeedBack(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Клиент')
    name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    rating = models.IntegerField(validators=[
            MinValueValidator(0, message='Рейтинг должен быть не меньше 0.'),
            MaxValueValidator(5, message='Рейтинг должен быть не больше 5.'),
        ], verbose_name='Рейтинг')
    feedback = models.TextField(blank=True, null=True, verbose_name='Отзыв')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')


class Coupons(models.Model):
    archived = models.BooleanField(default=True, verbose_name='Архив')
    title = models.CharField(max_length=100, verbose_name='Название купона')
    description = models.TextField(blank=True, verbose_name='Описание')