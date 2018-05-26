import xadmin
from xadmin import views
from .models import *


class UserAdmin(object):
    list_display = ['user_name', 'staff_id', 'is_leader', 'status']
    search_fields = ['user_name', 'staff_id', 'is_leader', 'status']
    list_filter = ['user_name', 'staff_id', 'is_leader', 'status']


# xadmin.site.register(User, UserAdmin)
