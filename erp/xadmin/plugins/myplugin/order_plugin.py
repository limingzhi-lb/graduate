from xadmin.views import BaseAdminPlugin, ModelFormAdminView, CreateAdminView, UpdateAdminView
import xadmin
from copy import deepcopy
from InfoManage.models import *
from users.models import User
from InfoManage.config import Config
import datetime
from script.SendMsg import SendMsg
from django.forms.models import ModelChoiceField
from django.contrib.auth.models import Group
config = Config()


class CreateOrderFormPlugin(BaseAdminPlugin):
    create_order_form = False

    def init_request(self, *args, **kwargs):
        return bool(self.create_order_form)

    def get_form_datas(self, data):
        if 'data' in data.keys():
            new_data = deepcopy(data)
            new_data['data']['payment_status'] = ''
            new_data['data']['is_finish'] = ''
            return new_data
        return data

    def get_read_only_fields(self, readonly_fields, *args, **kwargs):
        if self.user.groups.filter(name=config['manage']):
            readonly_fields = ()
            return readonly_fields
        readonly_fields = ['delivery', 'receipt_status', 'payment_status', 'total_price', 'storage_time', 'is_finish']
        return readonly_fields


class UpdateOrderFormGoodsPlugin(BaseAdminPlugin):
    order_form_goods = False
    of_good_id = None

    def init_request(self, *args, **kwargs):
        self.of_good_id = args[0]
        return bool(self.order_form_goods)

    def get_read_only_fields(self, readonly_fields, *args, **kwargs):
        if self.user.groups.filter(name=config['manage']):
            readonly_fields = ()
            return readonly_fields
        of_good = OrderFormGoods.objects.get(id=self.of_good_id)
        if of_good.of_name.is_finish:
            readonly_fields = ('rm_name', 'num', 'of_name')
        return readonly_fields


class OrderFormGoodsPlugin(BaseAdminPlugin):
    order_form_goods = False
    of_good_id = None

    def init_request(self, *args, **kwargs):
        return bool(self.order_form_goods)

    def formfield_for_dbfield(self, data, *args, **kwargs):
        if isinstance(data, ModelChoiceField):
            queryset = data._get_queryset()
            if queryset:
                if isinstance(queryset[0], OrderForm):
                    queryset = OrderForm.objects.filter(is_finish=False)
                    data._set_queryset(queryset)
        return data

    def get_form_datas(self, data):
        new_data = deepcopy(data)
        print(new_data)
        if 'data' in new_data.keys():
            of_id = new_data['data']['of_name']
            rm_id = new_data['data']['rm_name']
            vender = OrderForm.objects.get(id=of_id).ven_name
            rm = RawMaterial.objects.get(id=rm_id)
            if rm not in vender.rm_name.all():
                new_data['data']['num'] = 0
            if not vender.rm_name:
                new_data['data']['num'] = 0
        return new_data


class OrderFormPlugin(BaseAdminPlugin):
    order_form = False
    of_good_id = None

    def init_request(self, *args, **kwargs):
        return bool(self.order_form)

    def formfield_for_dbfield(self, data, *args, **kwargs):
        if isinstance(data, ModelChoiceField):
            queryset = data._get_queryset()
            if queryset:
                if isinstance(queryset[0], User):
                    group = Group.objects.get(name=config['purchase'])
                    queryset = group.user_set.all()
                    data._set_queryset(queryset)
        return data


class UpdateOrderFormByPurchase(BaseAdminPlugin):
    update_order_form = False
    of_id = None

    def init_request(self, *args, **kwargs):
        is_purchase = ''
        if self.user.groups.all():
            is_purchase = self.user.groups.all()[0].name == config['purchase']
        self.of_id = args[0]
        return bool(self.update_order_form and is_purchase)

    def get_read_only_fields(self, readonly_fields, *args, **kwargs):
        if self.user.groups.filter(name=config['manage']):
            readonly_fields = ()
            return readonly_fields
        if OrderForm.objects.get(id=self.of_id).is_finish:
            readonly_fields = ['of_name', 'ven_name', 'created', 'delivery', 'typ', 'receipt_status',
                               'payment_status', 'total_price', 'executor', 'storage_time', 'is_finish']
        elif self.user.is_leader:
            readonly_fields = ('delivery', 'receipt_status', 'storage_time', 'total_price')
            if not OrderForm.objects.get(id=self.of_id).receipt_status:
                readonly_fields = ('delivery', 'receipt_status', 'storage_time', 'total_price', 'is_finish')
        else:
            readonly_fields = ('delivery', 'receipt_status', 'storage_time', 'created', 'payment_status',
                               'total_price', 'executor', 'is_finish')
        print(readonly_fields)
        return readonly_fields

    def get_form_datas(self, data):
        new_data = deepcopy(data)

        if 'data' in new_data.keys() and 'is_finish' in new_data['data'].keys():
            if self.user.is_leader:
                if new_data['data']['is_finish'] == 'on':
                    new_data['data']['payment_status'] = 'on'
                    of_goods = OrderFormGoods.objects.filter(of_name=new_data['instance'].id)
                    for of_good in of_goods:
                        stor_detail = ''
                        if of_good.num == 0:
                            of_good.delete()
                        else:
                            try:
                                stor_detail = StorDetail.objects.filter(good_name=of_good.rm_name)
                            except:
                                pass
                            if stor_detail:
                                stor_detail[0].num += of_good.num
                                stor_detail[0].save()
                            else:
                                stor_detail = StorDetail()
                                stor_detail.good_name = of_good.rm_name
                                stor_detail.num = of_good.num
                                stor_detail.save()
        return new_data


class UpdateOrderFormByStor(BaseAdminPlugin):
    update_order_form = False
    of_id = None

    def init_request(self, *args, **kwargs):
        is_stor = ''
        if self.user.groups.all():
            is_stor = self.user.groups.all()[0].name == config['stor']
        self.of_id = args[0]
        return bool(self.update_order_form and is_stor)

    def get_form_datas(self, data):
        new_data = deepcopy(data)
        if 'data' in new_data.keys():
            today = datetime.datetime.now().strftime('%Y/%m/%d')
            now = datetime.datetime.now().strftime("%H:%M:%S")
            if 'receipt_status' in new_data['data'].keys():
                if not new_data['data']['delivery_0'] and not new_data['data']['storage_time_0']:
                    new_data['data']['delivery_0'] = new_data['data']['storage_time_0'] = today
                    new_data['data']['delivery_1'] = new_data['data']['storage_time_1'] = now
                elif not new_data['data']['delivery_0']:
                    new_data['data']['delivery_0'] = new_data['data']['storage_time_0']
                    new_data['data']['delivery_1'] = new_data['data']['storage_time_1']
                elif not new_data['data']['storage_time_0']:
                    new_data['data']['storage_time_0'] = new_data['data']['delivery_0']
                    new_data['data']['storage_time_1'] = new_data['data']['delivery_1']
                send = SendMsg(config['purchase'], '有一个订单需要确认，请尽快操作')
                send.send()
            elif 'delivery_0' in new_data['data'].keys():
                if new_data['data']['delivery_0'] or new_data['data']['storage_time_0']:
                    new_data['data']['receipt_status'] = 'on'
                    if not new_data['data']['delivery_0']:
                        new_data['data']['delivery_0'] = new_data['data']['storage_time_0']
                        new_data['data']['delivery_1'] = new_data['data']['storage_time_1']
                    elif not new_data['data']['storage_time_0']:
                        new_data['data']['storage_time_0'] = new_data['data']['delivery_0']
                        new_data['data']['storage_time_1'] = new_data['data']['delivery_1']
                delivery = datetime.datetime.strptime(new_data['data']['delivery_0'], '%Y/%m/%d')
                storage = datetime.datetime.strptime(new_data['data']['storage_time_0'], '%Y/%m/%d')

                today_ = datetime.datetime.strptime(today, '%Y/%m/%d')
                now_ = datetime.datetime.strptime(now, "%H:%M:%S")
                if delivery >= today_:
                    new_data['data']['delivery_0'] = today
                    if datetime.datetime.strptime(new_data['data']['delivery_1'], "%H:%M") > now_:
                        new_data['data']['delivery_1'] = now
                if storage >= today_:
                    new_data['data']['storage_time_0'] = today
                    if datetime.datetime.strptime(new_data['data']['storage_time_1'], "%H:%M") > now_:
                        new_data['data']['dstorage_time_1'] = now
                send = SendMsg(config['purchase'], '有一个订单需要确认，请尽快操作')
                send.send()
        return new_data

    def get_read_only_fields(self, readonly_fields, *args, **kwargs):
        if self.user.groups.filter(name=config['manage']):
            readonly_fields = ()
            return readonly_fields
        if OrderForm.objects.get(id=self.of_id).receipt_status:
            readonly_fields = ['of_name', 'ven_name', 'created', 'delivery', 'typ', 'receipt_status',
                               'payment_status', 'total_price', 'executor', 'storage_time', 'is_finish']
            return readonly_fields
        if OrderForm.objects.get(id=self.of_id).is_finish:
            readonly_fields = ['of_name', 'ven_name', 'created', 'delivery', 'typ', 'receipt_status',
                               'payment_status', 'total_price', 'executor', 'storage_time', 'is_finish']
        else:
            readonly_fields = ('of_name', 'ven_name', 'created', 'typ', 'payment_status',
                               'total_price', 'executor', 'is_finish')
        return readonly_fields


class ViewOrderFormDetail(BaseAdminPlugin):
    view_order_form_detail = False

    def init_request(self, *args, **kwargs):
        return bool(self.view_order_form_detail)


class test(BaseAdminPlugin):
    view_order_form_detail = True

    def init_request(self, *args, **kwargs):
        return bool(self.view_order_form_detail)

    def get_readonly_fields(self, readonly_fields):
        if OrderForm.objects.get(id=self.of_id).is_finish:
            readonly_fields = ['of_name', 'ven_name', 'created', 's_name', 'delivery', 'typ', 'receipt_status',
                               'payment_status', 'total_price', 'executor', 'storage_time', 'is_finish']
        return readonly_fields


xadmin.site.register_plugin(CreateOrderFormPlugin, CreateAdminView)
xadmin.site.register_plugin(UpdateOrderFormByStor, UpdateAdminView)
xadmin.site.register_plugin(UpdateOrderFormByPurchase, UpdateAdminView)
xadmin.site.register_plugin(UpdateOrderFormGoodsPlugin, UpdateAdminView)
xadmin.site.register_plugin(OrderFormGoodsPlugin, ModelFormAdminView)
xadmin.site.register_plugin(OrderFormPlugin, ModelFormAdminView)
