from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.db import models


class User(AbstractUser):
    __name__ = 'User'
    staff_id = models.IntegerField('微信', blank=True, null=True)
    is_leader = models.NullBooleanField('是否是领导', default=False, null=True)
    # dep_id = models.CharField(Department.name, blank=True)
    status = models.NullBooleanField('是否可用', default=True, null=True)

    class Meta(AbstractUser.Meta):
        db_table = 'User'
