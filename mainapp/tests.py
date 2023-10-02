from unittest import TestCase

from .models import *
import pytest


@pytest.mark.django_db
def test_category_create():
    return Category.objects.create(name='Test Category', slug='test-category')


@pytest.fixture
def category():
    return Category.objects.create(name='Test Category', slug='test-category')


@pytest.mark.django_db
def test_type_create(category):
    return InsuranceType.objects.create(title='Test Title', description='Test', content='Test', rate=0.1,
                                        cat=category,
                                        slug='test-slug')


@pytest.mark.django_db
def test_user_create():
    return User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')


@pytest.mark.django_db
def test_letter_create():
    return Letters.objects.create(letter='T', slug='t')


@pytest.fixture
def letter():
    return Letters.objects.create(letter='T', slug='t')


@pytest.mark.django_db
def test_company_create(letter):
    return InsuranceCompany.objects.create(name='Test', address='Test', phone_number='Test', letter_id=letter,
                                           slug='test')


@pytest.mark.django_db
def test_object_create():
    return InsuranceObjects.objects.create(name='Test', slug='test')


@pytest.fixture
def address(letter):
    return InsuranceCompany.objects.create(name='Test', address='Test', phone_number='Test', letter_id=letter,
                                           slug='test')


@pytest.mark.django_db
def test_agent_create(address):
    return InsuranceAgent.objects.create(last_name='Test', name='Test', middle_name='Test', email='orannon@gmail.com',
                                         phone_number='+375333808848',
                                         address=address, slug='test')


@pytest.fixture
def ins_object():
    return InsuranceObjects.objects.create(name='Test', slug='test')


@pytest.fixture
def user():
    return User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')


@pytest.fixture
def ins_type(category):
    return InsuranceType.objects.create(title='Test Title', description='Test', content='Test', rate=0.1,
                                        cat=category,
                                        slug='test-slug')
