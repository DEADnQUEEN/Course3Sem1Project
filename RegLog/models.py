from django.db import models
import hashlib
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


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
            raise ValueError('The Phone field must be set')

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
    login = models.TextField(db_column='Login', unique=True, verbose_name="Phone")
    last_login = models.TextField(db_column='Last Login', default=None, null=True, blank=True)
    is_superuser = models.IntegerField(db_column='IsRoot', default=0)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    class Meta:
        managed = True
        db_table = 'User'
        verbose_name = "Пользователь"

    def set_password(self, password: str):
        self.password = hashlib.sha3_256(password.encode()).hexdigest()

    def __str__(self):
        return str(self.human)
