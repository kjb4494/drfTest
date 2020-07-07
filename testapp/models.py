import os
from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from hashlib import sha512, md5


# Create your models here.
class CmbUserManager(BaseUserManager):

    def create_user(self, username, country, point, password=None):
        if not username:
            raise ValueError(_('유저명을 입력해주세요.'))
        if not country:
            raise ValueError(_('국가를 입력해주세요.'))
        if not point:
            raise ValueError(_('할당 가능 점수를 입력해주세요.'))
        user = self.model(
            username=username,
            country=country,
            point=point
        )
        user.set_password(password)
        user.save()
        bulk_bucket = []
        modifier_list = Modifier.objects.all()
        for modifier in modifier_list:
            bulk_bucket.append(UserHasModifier(
                user=user,
                modifier=modifier,
            ))
        UserHasModifier.objects.bulk_create(bulk_bucket)
        return user

    def create_superuser(self, username, country, point, password):
        user = self.create_user(
            username=username,
            password=password,
            country=country,
            point=point
        )
        user.is_superuser = True
        user.save()
        return user


class CmbUser(AbstractBaseUser, PermissionsMixin):
    idx = models.AutoField(db_column='idx', primary_key=True)
    username = models.CharField(db_column='username', unique=True, null=False, max_length=63)
    password = models.CharField(db_column='password', null=False, max_length=255)
    password_salt = models.CharField(db_column='passwordSalt', max_length=15)
    country = models.CharField(db_column='country', null=False, max_length=63)
    point = models.IntegerField(db_column='point', null=False)
    reg_date = models.DateTimeField(db_column='regDate', auto_now=True)
    last_login = models.DateTimeField(db_column='lastLogin', null=True, blank=True)
    is_superuser = models.BooleanField(db_column='isSuperUser', null=False, default=False)

    objects = CmbUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['country', 'point']

    class Meta:
        db_table = 'cmbUser'

    def is_staff(self):
        return self.is_superuser

    def get_username(self):
        return self.username

    def set_password(self, raw_password):
        salt = md5(os.urandom(128)).hexdigest()[:15]
        hashed_password = sha512(str(raw_password + salt).encode('utf-8')).hexdigest()
        self.password_salt = salt
        self.password = hashed_password

    def check_password(self, raw_password):
        try:
            user = CmbUser.objects.get(idx=self.idx)
            hashed_password = sha512(str(raw_password + user.password_salt).encode('utf-8')).hexdigest()
            return user.password == hashed_password
        except CmbUser.DoesNotExist:
            return False

    def natural_key(self):
        return self.username

    def __str__(self):
        return self.username


class Modifier(models.Model):
    idx = models.AutoField(db_column='idx', primary_key=True)
    description = models.CharField(db_column='description', max_length=255)
    description_ko = models.CharField(db_column='descriptionKo', max_length=255, default='')
    effect_type = models.CharField(db_column='effectType', max_length=63)
    example = models.CharField(db_column='example', max_length=255)
    modifier = models.CharField(db_column='modifier', max_length=127, null=False, unique=True)
    m_type = models.CharField(db_column='mType', max_length=63, null=False)
    version_added = models.CharField(db_column='versionAdded', max_length=15)
    default_value = models.FloatField(db_column='defaultValue')

    class Meta:
        db_table = 'cmbModifier'

    def natural_key(self):
        return {
            'idx': self.idx,
            'name': self.modifier,
            'type': self.m_type,
            'effect_type': self.effect_type,
            'description': self.description,
            'description_ko': self.description_ko,
            'default_value': self.default_value
        }

    def __str__(self):
        return '{idx}: {modifier}({description})'.format(
            idx=self.idx, modifier=self.modifier, description=self.description
        )


class UserHasModifier(models.Model):
    idx = models.AutoField(db_column='idx', primary_key=True)
    user = models.ForeignKey(CmbUser, on_delete=models.CASCADE, db_column='uIdx')
    modifier = models.ForeignKey(Modifier, on_delete=models.CASCADE, db_column='mIdx')
    used_point = models.IntegerField(db_column='usedPoint', null=False, default=0)

    class Meta:
        db_table = 'cmbUserHasModifier'
        unique_together = (('user', 'modifier'),)

    def __str__(self):
        return '{user_name}: {modifier}: {um_value}'.format(
            user_name=self.user, modifier=self.modifier, um_value=self.used_point
        )


class Country(models.Model):
    idx = models.AutoField(db_column='idx', primary_key=True)
    country_name = models.CharField(db_column='countryName', unique=True, null=False, max_length=63)
    country_tag = models.CharField(db_column='countryTag', unique=True, null=False, max_length=3)
    img_name = models.CharField(db_column='imgName', max_length=63)

    class Meta:
        db_table = 'cmbCountry'

    def __str__(self):
        return '{country_tag}: {country_name}'.format(
            country_tag=self.country_tag, country_name=self.country_name
        )
