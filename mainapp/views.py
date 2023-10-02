from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
import requests

import json

from .forms import *
from .models import *
from .utils import *

menu = [{'title': "Создать тип", 'url_name': 'read'}
        ]


class TypeHome(DataMixin, ListView):
    model = InsuranceType
    template_name = 'mainapp/html_lab/main_page.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Insurance Group')

        context['exclude_navigation'] = True

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return InsuranceType.objects.filter(is_published=True).order_by('-time_create')[:1]


class InsType(DataMixin, ListView):
    model = InsuranceType
    template_name = 'mainapp/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Виды страхования')

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return InsuranceType.objects.filter(is_published=True)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class CompanyAddress(DataMixin, ListView):
    model = InsuranceCompany
    template_name = 'mainapp/address.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Филиалы компании', let_selected=0)

        context['is_address_page'] = True

        return dict(list(context.items()) + list(c_def.items()))


class AddContract(LoginRequiredMixin, DataMixin, CreateView):
    form_class = ContractForm
    template_name = 'mainapp/contract.html'
    success_url = reverse_lazy('pay')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Заключение договора о страховании')

        context['exclude_navigation'] = True

        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class Pay(DataMixin, ListView):
    model = InsuranceType
    template_name = 'mainapp/pay.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Оплата')

        context['exclude_navigation'] = True

        return dict(list(context.items()) + list(c_def.items()))


class ShowInfo(DataMixin, DetailView):
    model = InsuranceType
    template_name = 'mainapp/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])

        return dict(list(context.items()) + list(c_def.items()))


class TypeCat(DataMixin, ListView):
    model = InsuranceType
    template_name = 'mainapp/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Рубрика - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self, *, object_list=None, **kwargs):
        return InsuranceType.objects.filter(cat__slug=self.kwargs['cat_slug'])


class LetCompany(DataMixin, ListView):
    model = InsuranceCompany
    template_name = 'mainapp/address.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Сортировка по алфавиту - ' + str(context['posts'][0].letter_id),
                                      let_selected=context['posts'][0].letter_id)
        context['is_address_page'] = True

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self, *, object_list=None, **kwargs):
        return InsuranceCompany.objects.filter(letter_id__slug=self.kwargs['let_slug'])


class ShowAgent(DataMixin, ListView):
    model = InsuranceAgent
    context_object_name = 'agents'
    template_name = 'mainapp/agent.html'

    def get_queryset(self):
        company = get_object_or_404(InsuranceCompany, slug=self.kwargs['agent_slug'])
        queryset = super().get_queryset()
        return queryset.filter(address=company)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = get_object_or_404(InsuranceCompany, slug=self.kwargs['agent_slug'])
        c_def = self.get_user_context(title=company.name)
        context['is_address_page'] = True

        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'mainapp/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')

        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'mainapp/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')

        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)

    return redirect('login')


class ContractList(LoginRequiredMixin, DataMixin, ListView):
    model = Contract
    template_name = 'mainapp/contract_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Cписок ваших контрактов')

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Contract.objects.filter(user=self.request.user)


class News(DataMixin, ListView):
    model = InsuranceType
    template_name = 'mainapp/news.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Мировые новости')

        return dict(list(context.items()) + list(c_def.items()))

#
# class Crypto(DataMixin, ListView):
#     model = InsuranceType
#     template_name = 'mainapp/crypto.html'
#     context_object_name = 'posts'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Курс биткоина')
#
#         return dict(list(context.items()) + list(c_def.items()))


def insurance_type_create(request):
    if not request.user.is_staff:
        raise PermissionDenied("Недостаточно прав.")

    if request.method == 'POST':
        form = InsuranceTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('read')
    else:
        form = InsuranceTypeForm()

        return render(request, 'mainapp/create.html', {'form': form, 'menu': menu})


def insurance_type_list(request):
    if not request.user.is_staff:
        raise PermissionDenied("Недостаточно прав.")

    ins_types = InsuranceType.objects.all()

    return render(request, 'mainapp/read.html', {'ins_types': ins_types, 'menu': menu})


def insurance_type_detail(request, id):
    if not request.user.is_staff:
        raise PermissionDenied("Недостаточно прав.")

    ins_types = get_object_or_404(InsuranceType, id=id)

    return render(request, 'mainapp/detail.html', {'ins_types': ins_types, 'menu': menu})


def insurance_type_update(request, id):
    if not request.user.is_staff:
        raise PermissionDenied("Недостаточно прав.")

    ins_type = get_object_or_404(InsuranceType, id=id)
    if request.method == 'POST':
        form = InsuranceTypeForm(request.POST, instance=ins_type)
        if form.is_valid():
            form.save()
            return redirect('detail', id=ins_type.id)
    else:
        form = InsuranceTypeForm(instance=ins_type)

        return render(request, 'mainapp/update.html', {'form': form, 'menu': menu})


def insurance_type_delete(request, id):
    if not request.user.is_staff:
        raise PermissionDenied("Недостаточно прав.")

    ins_type = get_object_or_404(InsuranceType, id=id)
    ins_type.delete()
    return redirect('read')


def search(request):
    query = request.GET.get('q')
    if query:
        types = InsuranceType.objects.filter(title__icontains=query)
    else:
        types = InsuranceType.objects.all()

    return render(request, 'mainapp/search.html', {'types': types})


class AboutCompany(DataMixin, ListView):
    model = InsuranceType
    template_name = 'mainapp/html_lab/about_company.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О компании')

        context['agents'] = InsuranceAgent.objects.annotate(
            has_income_over_250=Case(
                When(income__gt=250, then=1),
                default=0,
                output_field=DecimalField(),
            )
        ).values('has_income_over_250').annotate(count=Count('id'))

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return InsuranceType.objects.filter(is_published=True)


class Sertificate(DataMixin, TemplateView):
    template_name = 'mainapp/html_lab/sertificate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Сертификаты')

        return dict(list(context.items()) + list(c_def.items()))


class FAQEdit(DataMixin, CreateView):
    form_class = FAQForm
    template_name = 'mainapp/html_lab/FAQs.html'
    success_url = reverse_lazy('faqs')
    login_url = reverse_lazy('register')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Помощь')

        return dict(context, **c_def)

        # return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class Politics(DataMixin, TemplateView):
    template_name = 'mainapp/html_lab/politics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Политика конфиденциальности')

        return dict(list(context.items()) + list(c_def.items()))


class CouponsView(DataMixin, ListView):
    model = Coupons
    template_name = 'mainapp/html_lab/coupons.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Купоны и промокоды')

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Coupons.objects.all()


class VacancyView(DataMixin, ListView):
    model = Vacancy
    template_name = 'mainapp/html_lab/vacancy.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Доступные вакансии')

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Vacancy.objects.all()


class FeedBackForm(DataMixin, CreateView):
    form_class = FeedBackForm
    template_name = 'mainapp/html_lab/feedback_form.html'
    success_url = reverse_lazy('feedback_view')
    login_url = reverse_lazy('register')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Отзыв')

        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class FeedBackView(DataMixin, ListView):
    model = FeedBack
    template_name = 'mainapp/html_lab/feedback_view.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Отзывы')

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return FeedBack.objects.all()


class TableStatic(DataMixin, ListView):
    model = Contract
    template_name = 'mainapp/html_lab/static_table.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Статистика')

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Contract.objects.all()
