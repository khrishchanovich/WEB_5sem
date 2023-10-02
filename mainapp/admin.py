from django.contrib import admin
from .models import *


class InsuranceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'time_create', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class InsuranceCompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'phone_number', 'letter_id')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'address')
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class LettersAdmin(admin.ModelAdmin):
    list_display = ('id', 'letter')
    list_display_links = ('id', 'letter')
    search_fields = ('letter',)
    prepopulated_fields = {'slug': ('letter',)}


class ContractAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'last_name', 'name', 'middle_name', 'email', 'phone_number', 'cat', 'ins_object', 'address',
        'accept_terms',
        'initial_payment'
    )
    list_display_links = ('id', 'last_name')
    search_fields = ('id', 'last_name')
    # prepopulated_fields = {'slug': ('last_name',)}


class InsuranceAgentAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'name', 'middle_name', 'email', 'phone_number', 'address')
    list_display_links = ('id', 'last_name')
    search_fields = ('id', 'last_name', 'address')
    prepopulated_fields = {'slug': ('last_name', 'name')}


class InsuranceObjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class FAQAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer')
    list_display_links = ('id', 'question', 'answer')
    search_fields = ('answer',)
    # prepopulated_fields = {'slug': ('id',)}


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')
    # prepopulated_fields = {'slug': ('title',)}


class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'last_name', 'rating', 'feedback', 'time_create')
    list_display_links = ('id', 'user')
    search_fields = ('id', 'user', 'rating')
    # prepopulated_fields = {'slug': ('id', 'last_name', 'name')}


class CouponsAdmin(admin.ModelAdmin):
    list_display = ('id', 'archived', 'title', 'description')
    list_display_links = ('id', 'archived')
    search_fields = ('id', 'archived', 'title')
    # prepopulated_fields = {'slug': ('title', )}


admin.site.register(InsuranceType, InsuranceTypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(InsuranceCompany, InsuranceCompanyAdmin)
admin.site.register(Letters, LettersAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(InsuranceAgent, InsuranceAgentAdmin)
admin.site.register(InsuranceObjects, InsuranceObjectsAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(FeedBack, FeedBackAdmin)
admin.site.register(Coupons, CouponsAdmin)
