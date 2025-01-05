import datetime
import random
import string

from django.db import models
import hashlib
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


def create_key():
    key = []
    for i in range(4):
        key.append('')
        for _ in range(4):
            key[i] += random.choice(string.ascii_letters)

    return '-'.join(key)


def date():
    return datetime.date.today()


class Human(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.TextField(db_column='Name', null=False)
    surname = models.TextField(db_column='Surname', null=False)
    father_name = models.TextField(db_column='Father name', null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'Human'

    @property
    def __name_list(self):
        full_name = [self.surname, self.name]
        if self.father_name is not None:
            full_name.append(self.father_name)
        return full_name

    @property
    def full_name(self):
        return ' '.join(self.__name_list)

    @property
    def name_initials(self):
        full_name = self.__name_list
        for i in range(1, len(full_name)):
            full_name[i] = full_name[i][0].upper() + '.'
        return ' '.join(full_name)

    def __str__(self):
        return self.full_name


class UserManager(BaseUserManager):
    def create_user(
            self,
            login: str,
            name: str,
            surname: str,
            father_name: str,
            password=None,
            **extra_fields
    ):
        if not login:
            raise ValueError('The Login field must be set')

        human = Human.objects.filter(
            name=name,
            surname=surname,
            father_name=father_name
        ).first()

        if human is None:
            human = Human(
                name=name,
                surname=surname,
                father_name=father_name
            )
            human.save()

        user = self.model(login=login, human=human, human_id=human.id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, login, password=None, **extra_fields):
        name = input('name: ')
        surname = input('surname: ')
        father_name = input('father_name: ')
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(login, name, surname, father_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(db_column='ID', primary_key=True)
    human = models.ForeignKey(Human, models.DO_NOTHING)
    password = models.TextField(db_column='Password')
    login = models.TextField(db_column='Login', unique=True, verbose_name="Username")
    last_login = models.TextField(db_column='Last Login', default=None, null=True, blank=True)
    is_superuser = models.IntegerField(db_column='IsRoot', default=0)

    objects = UserManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payments = Payment.objects.filter(user_id=self.id)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = [login, password]

    @property
    def director_list(self):
        return Company.objects.filter(director=self)

    @property
    def can_set_payment(self):
        return len(self.director_list) or len(Connect.objects.filter(user=self))

    class Meta:
        managed = True
        db_table = 'User'
        verbose_name = "Пользователь"

    def set_password(self, password: str):
        self.password = hashlib.sha3_256(password.encode()).hexdigest()

    def __str__(self):
        return str(self.human)


class Payment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, null=False, blank=False)
    amount = models.IntegerField(db_column='Amount', null=False, blank=False, default=0)
    date = models.DateField(db_column='Date', null=False, blank=False, default=datetime.date.today)

    class Meta:
        managed = True
        db_table = "Payments"
        verbose_name = "Оплаты"


class Company(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.TextField(db_column='Name', null=False, blank=False)
    director = models.ForeignKey(User, models.DO_NOTHING, null=False, blank=False)
    key = models.TextField(db_column='Key', null=False, default=create_key)

    class Meta:
        managed = True
        db_table = "Company"
        verbose_name = "Компании"


class Connect(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, null=False, blank=False)
    company = models.ForeignKey(Company, models.DO_NOTHING, null=False, blank=False)

    class Meta:
        managed = True
        db_table = "Connect"
        verbose_name = "Соединение"
