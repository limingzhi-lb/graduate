from xadmin.views import BaseAdminPlugin, ModelFormAdminView, CreateAdminView, UpdateAdminView
import xadmin
from copy import deepcopy
from InfoManage.models import *
from InfoManage.config import Config
from django.forms.models import ModelChoiceField
from django.contrib.auth.models import Group
from users.models import User
import datetime
from script.SendMsg import SendMsg
config = Config()


class CreateOutStorForm(BaseAdminPlugin):
    create_out_stor = False

    def init_request(self, *args, **kwargs):
        return bool(self.create_out_stor)

    def formfield_for_dbfield(self, data, *args, **kwargs):
        if isinstance(data, ModelChoiceField):
            queryset = data._get_queryset()
            if isinstance(queryset[0], User):
                group = Group.objects.get(name=config['stor'])
                queryset = group.user_set.all()
                data._set_queryset(queryset)
        return data

    def get_read_only_fields(self, readonly_fields, *args, **kwargs):
        readonly_fields = ('finished', 'check')
        return readonly_fields

    def get_form_datas(self, data):
        send = SendMsg(config['stor'], '有一个出库订单创建完成需要确认，请尽快操作')
        send.send()
        return data


class UpdateOutStorForm(BaseAdminPlugin):
    update_out_stor = False
    of_id = None

    def init_request(self, *args, **kwargs):
        self.of_id = args[0]
        return bool(self.update_out_stor)

    def formfield_for_dbfield(self, data, *args, **kwargs):
        if isinstance(data, ModelChoiceField):
            queryset = data._get_queryset()
            if isinstance(queryset[0], User):
                group = Group.objects.get(name=config['stor'])
                queryset = group.user_set.all()
                data._set_queryset(queryset)
        return data

    def get_read_only_fields(self, readonly_fields, *args, **kwargs):
        if self.user.groups.filter(name=config['manage']):
            readonly_fields = ()
            return readonly_fields
        os_form = OutStorForm.objects.get(id=self.of_id)
        if os_form.check:
            readonly_fields = ('osf_name', 'created', 'staff_id', 'note', 'finished', 'check')
            return readonly_fields
        if os_form.finished:
            if self.user.is_leader:
                readonly_fields = ('osf_name', 'created', 'staff_id', 'note', 'finished')
                return readonly_fields
            else:
                readonly_fields = ('osf_name', 'created', 'staff_id', 'note', 'finished', 'check')
                return readonly_fields
        elif os_form.staff_id.id == self.user.id:
            if self.user.is_leader:
                readonly_fields = ('created',)
            else:
                readonly_fields = ('created', 'check')
        elif self.user.is_leader:
            readonly_fields = ('created', 'finished', 'check')
        else:
            readonly_fields = ('osf_name', 'created', 'staff_id', 'note', 'finished', 'check')
        return readonly_fields

    def get_form_datas(self, data):
        os_form = OutStorForm.objects.get(id=self.of_id)
        new_data = deepcopy(data)
        today = datetime.datetime.now().strftime('%Y/%m/%d')
        now = datetime.datetime.now().strftime("%H:%M:%S")
        if 'data' in new_data.keys():
            if str(os_form.staff_id.id) != str(new_data['data'].get('staff_id') or os_form.staff_id.id):
                new_data['data']['finished_0'] = ''
                new_data['data']['finished_1'] = ''
                if 'check' in new_data['data'].keys():
                    new_data['data']['check'] = ''
                send = SendMsg(config['stor'], '有一个出库订单被修改需要确认，请尽快操作')
                send.send()
            elif 'check' in new_data['data'].keys():
                if new_data['data']['check'] == 'on':
                    if not new_data['data'].get('finished_0'):
                        new_data['data']['finished_0'] = today
                        new_data['data']['finished_1'] = now
                    elif not new_data['data']['finished_0']:
                        new_data['data']['finished_0'] = today
                        new_data['data']['finished_1'] = now
                os_infos = OutStorDetail.objects.filter(osf_name=self.of_id)
                for os_info in os_infos:
                    os_info.good_name.num -= os_info.num
                    os_info.good_name.save()
        return new_data


class OutStorDetailForm(BaseAdminPlugin):
    out_stor_detail = False

    def init_request(self, *args, **kwargs):
        return bool(self.out_stor_detail)

    def get_form_datas(self, data):
        new_data = deepcopy(data)

        if 'data' in new_data.keys():
            good_name = new_data['data']['good_name']
            print(good_name)
            stor_info = StorDetail.objects.get(id=good_name)
            if int(stor_info.num) < int(new_data['data']['num']):
                new_data['data']['num'] = stor_info.num
        return new_data

    def formfield_for_dbfield(self, data, *args, **kwargs):
        if isinstance(data, ModelChoiceField):
            queryset = data._get_queryset()
            if queryset:
                if isinstance(queryset[0], OutStorForm):
                    queryset = OutStorForm.objects.filter(check=False)
                    data._set_queryset(queryset)
        return data


class UpdateOutStorDetailForm(BaseAdminPlugin):
    out_stor_detail = False
    good_id = None

    def init_request(self, *args, **kwargs):
        self.good_id = args[0]
        return bool(self.out_stor_detail)

    def get_read_only_fields(self, readonly_fields, *args, **kwargs):
        if self.user.groups.filter(name=config['manage']):
            readonly_fields = ()
            return readonly_fields
        osf_good = OutStorDetail.objects.get(id=self.good_id)
        if osf_good.osf_name.check:
            readonly_fields = ('good_name', 'num', 'osf_name')
            return readonly_fields
        if self.user.is_leader:
            readonly_fields = ()
            return readonly_fields
        if osf_good.osf_name.staff_id.id != self.user.id:
            readonly_fields = ('good_name', 'num', 'osf_name')
        else:
            readonly_fields = ()
        return readonly_fields


xadmin.site.register_plugin(CreateOutStorForm, CreateAdminView)
xadmin.site.register_plugin(UpdateOutStorForm, UpdateAdminView)
xadmin.site.register_plugin(OutStorDetailForm, ModelFormAdminView)
xadmin.site.register_plugin(UpdateOutStorDetailForm, UpdateAdminView)
