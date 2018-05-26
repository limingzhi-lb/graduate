from xadmin.views import BaseAdminPlugin,  ModelFormAdminView, CreateAdminView, UpdateAdminView
import xadmin
from copy import deepcopy
from InfoManage.models import *
from InfoManage.config import Config
from django.forms.models import ModelChoiceField
from django.contrib.auth.models import Group
from users.models import User
from script.SendMsg import SendMsg
config = Config()


class AssemblyLinePlugin(BaseAdminPlugin):
    assembly_line = False

    def init_request(self, *args, **kwargs):
        return bool(self.assembly_line)

    def formfield_for_dbfield(self, data, *args, **kwargs):
        if isinstance(data, ModelChoiceField):
            queryset = data._get_queryset()
            if isinstance(queryset[0], User):
                group = Group.objects.get(name=config['produce'])
                queryset = group.user_set.all()
                data._set_queryset(queryset)
        return data

    def get_read_only_fields(self, readonly_fields, *args, **kwargs):
        readonly_fields = ('ass_name', 'leader', 'created', 'updated')
        if self.user.groups.all()[0].name == config['produce'] and self.user.is_leader:
            readonly_fields = ()
        if self.user.groups.filter(name=config['manage']):
            readonly_fields = ()
            return readonly_fields
        return readonly_fields


class ProductPlugin(BaseAdminPlugin):
    product = False

    def init_request(self, *args, **kwargs):
        return bool(self.product)

    def get_read_only_fields(self, readonly_fields, *args, **kwargs):
        readonly_fields = ('ass_name', 'price', 'created', 'updated')
        if self.user.groups.all()[0].name == config['produce'] and self.user.is_leader:
            readonly_fields = ()
        if self.user.groups.filter(name=config['manage']):
            readonly_fields = ()
            return readonly_fields
        return readonly_fields


class HalfProductPlugin(BaseAdminPlugin):
    halfproduct = False

    def init_request(self, *args, **kwargs):
        return bool(self.halfproduct)

    def get_read_only_fields(self, readonly_fields, *args, **kwargs):
        readonly_fields = ('hp_name', 'created', 'updated')
        if self.user.groups.all()[0].name == config['produce'] and self.user.is_leader:
            readonly_fields = ()
        if self.user.groups.filter(name=config['manage']):
            readonly_fields = ()
            return readonly_fields
        return readonly_fields


class MeterialPlugin(BaseAdminPlugin):
    meterial = False

    def init_request(self, *args, **kwargs):
        return bool(self.meterial)

    def get_read_only_fields(self, readonly_fields, *args, **kwargs):
        readonly_fields = ('name', 'num', 'product', 'hp_name', 'created', 'updated')
        if self.user.groups.all()[0].name == config['produce'] and self.user.is_leader:
            readonly_fields = ('actual_num', 'is_instor', 'is_finish', 'qualified_rate')
        if self.user.groups.filter(name=config['manage']):
            readonly_fields = ()
            return readonly_fields
        return readonly_fields


class CreateProducePlugin(BaseAdminPlugin):
    create_produce = False

    def init_request(self, *args, **kwargs):
        return bool(self.create_produce)

    def get_read_only_fields(self, readonly_fields, *args, **kwargs):
        readonly_fields = ('pf_name', 'pro_name', 'pro_num', 'hpro_name', 'hpro_num', 'created',
                           'assembly_line', 'actual_num', 'is_instor', 'note', 'is_finish', 'qualified_rate')
        if self.user.groups.all()[0].name == config['produce'] and self.user.is_leader:
            readonly_fields = ('actual_num', 'is_instor', 'is_finish', 'qualified_rate')
        if self.user.groups.filter(name=config['manage']):
            readonly_fields = ()
            return readonly_fields
        return readonly_fields

    def get_form_datas(self, data):
        new_data = deepcopy(data)
        if 'data' in new_data.keys():
            if 'pro_name' in new_data['data'].keys():
                if not new_data['data']['pro_name']:
                    new_data['data']['pro_num'] = ''
                elif 'pro_num' not in new_data['data'].keys():
                    new_data['data']['pro_num'] = '0'
                elif not new_data['data']['pro_num']:
                    new_data['data']['pro_num'] = '0'
                if new_data['data']['pro_name']:
                    meterials = Meterial.objects.all()
                    stors = StorDetail.objects.all()
                    less = int(new_data['data']['pro_num'])
                    for meterial in meterials:
                        if meterial.product:
                            if str(meterial.product.id) == new_data['data']['pro_name']:
                                for stor in stors:
                                    if stor.good_name == meterial.name.good_name:
                                        if int(stor.num) < int(meterial.num) * int(new_data['data']['pro_num']):
                                            if less > int(stor.num) // int(meterial.num):
                                                less = int(stor.num) // int(meterial.num)
                    new_data['data']['pro_num'] = str(less)
            if 'hpro_name' in new_data['data'].keys():
                if not new_data['data']['hpro_name']:
                    new_data['data']['hpro_num'] = ''
                elif 'hpro_num' not in new_data['data'].keys():
                    new_data['data']['hpro_num'] = '0'
                elif not new_data['data']['hpro_num']:
                    new_data['data']['hpro_num'] = '0'
                if new_data['data']['hpro_num']:
                    meterials = Meterial.objects.all()
                    stors = StorDetail.objects.all()
                    less = int(new_data['data']['hpro_num'])
                    for meterial in meterials:
                        if meterial.hp_name:
                            if str(meterial.hp_name.id) == new_data['data']['hpro_name']:
                                for stor in stors:
                                    if stor.good_name == meterial.name.good_name:
                                        if int(stor.num) < int(meterial.num)*int(new_data['data']['hpro_num']):
                                            if less > int(stor.num) // int(meterial.num):
                                                less = int(stor.num) // int(meterial.num)
                    new_data['data']['hpro_num'] = str(less)

        return new_data


class UpdateProductPlugin(BaseAdminPlugin):
    update_produce = False
    product_id = None

    def init_request(self, *args, **kwargs):
        self.product_id = args[0]
        return bool(self.update_produce)

    def get_read_only_fields(self, readonly_fields, *args, **kwargs):
        if self.user.groups.filter(name=config['manage']):
            readonly_fields = ()
            return readonly_fields
        pf = ProduceForm.objects.get(id=self.product_id)
        readonly_fields = ('pf_name', 'pro_name', 'pro_num', 'hpro_name', 'hpro_num', 'created',
                           'assembly_line', 'actual_num', 'is_instor', 'note', 'is_finish', 'qualified_rate')
        if (not (pf.pro_num or pf.hpro_num) or (pf.pro_num == 0 and pf.hpro_num == 0)) and \
                ((not self.user.is_leader and self.user.groups.all()[0].name == config['produce'])
                 or self.user.groups.all()[0].name == config['stor']):
            readonly_fields = ('pf_name', 'pro_name', 'pro_num', 'hpro_name', 'hpro_num', 'created',
                               'assembly_line', 'actual_num', 'is_instor', 'note', 'is_finish', 'qualified_rate')
            return readonly_fields
        if pf.is_finish:
            readonly_fields = ('pf_name', 'pro_name', 'pro_num', 'hpro_name', 'hpro_num', 'created',
                               'assembly_line', 'actual_num', 'is_instor', 'note', 'is_finish', 'qualified_rate')
            return readonly_fields
        elif pf.is_instor:
            if self.user.groups.all()[0].name == config['stor']:
                readonly_fields = ('pf_name', 'pro_name', 'pro_num', 'hpro_name', 'hpro_num', 'created',
                                   'assembly_line', 'actual_num', 'is_instor', 'note', 'is_finish', 'qualified_rate')
                return readonly_fields
            if self.user.is_leader and self.user.groups.all()[0].name == config['produce']:
                readonly_fields = ('pf_name', 'pro_name', 'pro_num', 'hpro_name', 'hpro_num', 'created',
                               'assembly_line', 'actual_num', 'is_instor', 'note', 'qualified_rate')
                return readonly_fields
        elif pf.assembly_line.leader.id == self.user.id:
            print('*******')
            if self.user.is_leader:
                readonly_fields = ('created', 'is_instor', 'qualified_rate')
                return readonly_fields
            else:
                readonly_fields = ('pf_name', 'pro_name', 'pro_num', 'hpro_name', 'hpro_num', 'created',
                                   'assembly_line', 'is_instor', 'is_finish', 'qualified_rate')
                return readonly_fields
        elif self.user.groups.all()[0].name == config['stor']:
            if pf.actual_num:
                readonly_fields = ('pf_name', 'pro_name', 'pro_num', 'hpro_name', 'hpro_num', 'created',
                                   'assembly_line', 'actual_num', 'note', 'is_finish', 'qualified_rate')
                return readonly_fields
        if self.user.is_leader and self.user.groups.all()[0].name == config['produce']:
            readonly_fields = ('created', 'is_instor', 'actual_num', 'qualified_rate')
            return readonly_fields
        return readonly_fields

    # TODO 创建生产目标之后，给仓库组发微信创建出库表，不强制要求，如未创建为仓库组内部失误，不应在生产目标中加强制要求
    # TODO 生产目标完成不需要减去仓库中的货物数量，由出库表减去
    def get_form_datas(self, data):
        new_data = deepcopy(data)
        if 'data' in new_data.keys():
            pf = ProduceForm.objects.get(id=self.product_id)
            if 'assembly_line' in new_data['data'].keys():
                if str(pf.assembly_line) != new_data['data']['assembly_line']:
                    new_data['data']['actual_num'] = ''
                    new_data['data']['is_finish'] = ''
                    if 'is_finish' in new_data['data'].keys():
                        new_data['data']['is_finish'] = ''
            if 'pro_name' in new_data['data'].keys():
                if not new_data['data']['pro_name']:
                    new_data['data']['pro_num'] = ''
                elif 'pro_num' not in new_data['data'].keys():
                    new_data['data']['pro_num'] = '0'
                elif not new_data['data']['pro_num']:
                    new_data['data']['pro_num'] = '0'
                elif pf.pro_num and str(new_data['data']['pro_num']) != str(pf.pro_num):
                    new_data['data']['pro_num'] = '0'
                meterials = Meterial.objects.all()
                stors = StorDetail.objects.all()
                less = int(new_data['data']['pro_num'])
                for meterial in meterials:
                    if meterial.product:
                        if str(meterial.product.id) == new_data['data']['pro_name']:
                            for stor in stors:
                                if stor.good_name == meterial.name.good_name:
                                    if int(stor.num) < int(meterial.num) * int(new_data['data']['pro_num']):
                                        if less > int(stor.num) // int(meterial.num):
                                            less = int(stor.num) // int(meterial.num)
                                    rw = RawMaterial.objects.get(rm_name=stor.good_name)
                                    if stor.num < rw.minimum_inventory:
                                        send = SendMsg(config['purchase'], '有原材料需要补货，请尽快操作')
                                        send.send()
                new_data['data']['pro_num'] = str(less)
            if 'hpro_name' in new_data['data'].keys():
                if not new_data['data']['hpro_name']:
                    new_data['data']['hpro_num'] = ''
                elif 'hpro_num' not in new_data['data'].keys():
                    new_data['data']['hpro_num'] = '0'
                elif not new_data['data']['hpro_num']:
                    new_data['data']['hpro_num'] = '0'
                elif pf.pro_num and str(new_data['data']['hpro_num']) != str(pf.pro_num):
                    new_data['data']['hpro_num'] = '0'
                meterials = Meterial.objects.all()
                stors = StorDetail.objects.all()
                less = int(new_data['data']['hpro_num'])
                for meterial in meterials:
                    if meterial.hp_name:
                        if str(meterial.hp_name.id) == new_data['data']['hpro_name']:
                            for stor in stors:
                                if stor.good_name == meterial.name.good_name:
                                    if int(stor.num) < int(meterial.num)*int(new_data['data']['hpro_num']):
                                        if less > int(stor.num) // int(meterial.num):
                                            less = int(stor.num) // int(meterial.num)
                                    rw = RawMaterial.objects.get(rm_name=stor.good_name)
                                    if stor.num < rw.minimum_inventory:
                                        send = SendMsg(config['purchase'], '有原材料需要补货，请尽快操作')
                                        send.send()
                new_data['data']['hpro_num'] = str(less)
            if new_data['data'].get('is_finish'):
                pro_name = pf.pro_name
                pro_num = pf.pro_num
                hpro_name = pf.hpro_name
                hpro_num = pf.hpro_num
                if pro_num:
                    add_stor = StorDetail()
                    add_stor.good_name = pro_name
                    add_stor.num = pro_num
                    add_stor.save()
                if hpro_num:
                    add_stor = StorDetail()
                    add_stor.good_name = hpro_name
                    add_stor.num = hpro_num
                    add_stor.save()
            if new_data['data'].get('is_instor'):
                send = SendMsg(config['produce'], '产品入库需要确认，请尽快操作')
                send.send()
        return new_data


class WasteFormPlugin(BaseAdminPlugin):
    waste_form = False

    def init_request(self, *args, **kwargs):
        return bool(self.waste_form)

    def formfield_for_dbfield(self, data, *args, **kwargs):
        if isinstance(data, ModelChoiceField):
            queryset = data._get_queryset()
            if queryset:
                if isinstance(queryset[0], ProduceForm):
                    group = ProduceForm.objects.filter(is_finish=False, assembly_line=AssemblyLine.objects.get(leader=self.user))
                    queryset = group.all()
                    data._set_queryset(queryset)
        return data


class UpdateWasteFormPlugin(BaseAdminPlugin):
    waste_form = False
    wf_id = None

    def init_request(self, *args, **kwargs):
        self.wf_id = args[0]
        return bool(self.waste_form)

    def get_read_only_fields(self, readonly_fields, *args, **kwargs):
        wf = WasteForm.objects.get(id=self.wf_id)
        if wf.pf_name.is_finish:
            readonly_fields = ('name', 'num', 'pf_name')
        if self.user.groups.filter(name=config['manage']):
            readonly_fields = ()
            return readonly_fields
        return readonly_fields


xadmin.site.register_plugin(AssemblyLinePlugin, ModelFormAdminView)
xadmin.site.register_plugin(ProductPlugin, ModelFormAdminView)
xadmin.site.register_plugin(HalfProductPlugin, ModelFormAdminView)
xadmin.site.register_plugin(MeterialPlugin, ModelFormAdminView)
xadmin.site.register_plugin(CreateProducePlugin, CreateAdminView)
xadmin.site.register_plugin(UpdateProductPlugin, UpdateAdminView)
xadmin.site.register_plugin(WasteFormPlugin, ModelFormAdminView)
xadmin.site.register_plugin(UpdateWasteFormPlugin, UpdateAdminView)


