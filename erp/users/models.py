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


'''
class Department(models.Model):
    __name__ = 'Department'
    name = models.CharField(max_length=12, primary_key=True)
    category = models.IntegerField()
    

class Role(models.Model):
    __name__ = 'Role'
    role_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=24, db_index=True)
    permission = JSONField()


class OrgRole(models.Model):
    __name__ = 'OrgRole'
    role_id = models.IntegerField(primary_key=True, db_index=True)
    dep_category = models.IntegerField(db_index=True)

    class Meta:
        unique_together = ('role_id', 'dep_category')


class UserPermission(models.Model):
    __name__ = 'UserPermission'
    staff_id = models.IntegerField(db_index=True)
    action = models.CharField(max_length=24)
    resource = models.CharField(max_length=24)

    class Meta:
        unique_together = ('staff_id', 'action', 'resource')


class RolePermission(models.Model):
    __name__ = 'RolePermission'
    role_id = models.IntegerField(primary_key=True,db_index=True)
    permission = JSONField()


class UserRole(models.Model):
    __name__ = 'UserRole'
    staff_id = models.IntegerField(db_index=True)
    org_id = models.IntegerField(db_index=True)
    role_id = models.IntegerField(db_index=True)

'''

