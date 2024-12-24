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


class Human(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.TextField(db_column='Name', null=False)
    surname = models.TextField(db_column='Surname', null=False)
    father_name = models.TextField(db_column='Father name', null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'Human'

    @property
    def full_name(self):
        full_name = [self.surname, self.name]
        if self.father_name is not None:
            full_name.append(self.father_name)
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

    @property
    def is_stand_alone(self):
        return Connect.objects.filter(user_id=self.id) > 0

    @property
    def is_ceo(self):
        return Organization.objects.filter(ceo__id__exact=self.id) > 0

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = [login, password]

    class Meta:
        managed = True
        db_table = 'User'
        verbose_name = "Пользователь"

    def set_password(self, password: str):
        self.password = hashlib.sha3_256(password.encode()).hexdigest()

    def __str__(self):
        return str(self.human)


class Organization(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.TextField(db_column='Name', null=False)
    key = models.TextField(db_column='Key', null=False, default=create_key)
    ceo = models.ForeignKey(User, models.DO_NOTHING, null=False, blank=False)

    class Meta:
        managed = True
        db_table = 'Organization'
        verbose_name = "Компании"

    def __str__(self):
        return self.name


class Connect(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, null=False, blank=False)
    organization = models.ForeignKey(Organization, models.DO_NOTHING, null=False, blank=False)

    class Meta:
        managed = True
        db_table = "Connections"
        verbose_name = "Соединение"


class Payment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, null=False, blank=False)
    amount = models.IntegerField(db_column='Amount', null=False, blank=False, default=0)

    class Meta:
        managed = True
        db_table = "Payments"
        verbose_name = "Оплаты"
