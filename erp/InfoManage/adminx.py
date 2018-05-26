import xadmin
from xadmin import views
from .models import *


class BaseSetting(object):

    enable_themes = True
    use_bootswatch = True


class VenderAdmin(object):
    say_hello = True
    list_display = ['ven_name', 'addr', 'tel', 'created', 'updated', 'rm_name']
    search_fields = ['ven_name', 'addr', 'tel', 'created', 'updated', 'rm_name']
    list_filter = ['ven_name', 'addr', 'tel', 'created', 'updated', 'rm_name']
    read_only_fields = ('ven_name', 'addr')
    list_per_page = 5
    filter_horizontal = ('rm_name',)


class RawMaterialAdmin(object):
    say_hello = False
    used = False
    list_display = ['rm_name', 'price', 'classification', 'minimum_inventory', 'created', 'updated']
    search_fields = ['rm_name', 'price', 'classification', 'minimum_inventory', 'created', 'updated']
    list_filter = ['rm_name', 'price', 'classification', 'minimum_inventory', 'created', 'updated']
    list_per_page = 5


class StorDetailInline(object):
    model = StorDetail
    extra = 0


class StorAdmin(object):
    list_display = ['s_name', 'valid']
    search_fields = ['s_name', 'valid']
    list_filter = ['s_name', 'valid']
    list_per_page = 5


class StorDetailAdmin(object):
    list_display = ['good_name', 'num']
    search_fields = ['good_name', 'num']
    list_filter = ['good_name', 'num']
    list_per_page = 5


class OrderFormAdmin(object):
    create_order_form = True
    update_order_form = True
    view_order_form_detail = True
    order_form = True
    list_display = ['of_name', 'ven_name', 'created', 'delivery', 'typ', 'receipt_status', 'payment_status',
                    'total_price', 'executor', 'storage_time', 'is_finish']
    search_fields = ['of_name', 'ven_name', 'created', 'delivery', 'typ', 'receipt_status', 'payment_status',
                     'total_price', 'executor', 'storage_time', 'is_finish']
    list_filter = ['of_name', 'ven_name', 'created', 'delivery', 'typ', 'receipt_status', 'payment_status',
                   'total_price', 'executor', 'storage_time', 'is_finish']
    list_per_page = 5


class OrderFormGoodsAdmin(object):
    order_form_goods = True
    list_display = ['rm_name', 'num', 'of_name']
    search_fields = ['rm_name', 'num', 'of_name']
    list_filter = ['rm_name', 'num', 'of_name']
    list_per_page = 5


class SwapFormAdmin(object):
    swap_form = True
    list_display = ['sf_name', 'staff_name', 'before_s_id', 'after_s_id', 'created', 'finished', 'check']
    search_fields = ['sf_name', 'staff_name', 'before_s_id', 'after_s_id', 'created', 'finished', 'check']
    list_filter = ['sf_name', 'staff_name', 'before_s_id', 'after_s_id', 'created', 'finished', 'check']
    list_per_page = 5


class SwapFormDetailAdmin(object):
    swap_form_detail = True
    swap_form = True
    list_display = ['good_name', 'num', 'sf_name']
    search_fields = ['good_name', 'num', 'sf_name']
    list_filter = ['good_name', 'num', 'sf_name']
    list_per_page = 5


class OutStorDetailAdmin(object):
    out_stor_detail = True
    list_display = ['good_name', 'num', 'osf_name']
    search_fields = ['good_name', 'num', 'osf_name']
    list_filter = ['good_name', 'num', 'osf_name']
    list_per_page = 5


class OutStoreFormAdmin(object):
    create_out_stor = True
    update_out_stor = True
    list_display = ['osf_name', 'created', 'staff_id', 'check', 'note', 'finished']
    search_fields = ['osf_name', 'created', 'staff_id', 'check', 'note', 'finished']
    list_filter = ['osf_name', 'created', 'staff_id', 'check', 'note', 'finished']
    list_per_page = 5


class AssemblyLineAdmin(object):
    list_display = ['ass_name']
    search_fields = ['ass_name']
    list_filter = ['ass_name']
    list_per_page = 5


class ProductAdmin(object):
    product = True

    list_display = ['pro_name', 'price', 'created', 'updated']
    search_fields = ['pro_name', 'price', 'created', 'updated']
    list_filter = ['pro_name', 'price', 'created', 'updated']
    list_per_page = 5


class HalfproductAdmin(object):
    half_product = True
    list_display = ['hp_name', 'created', 'updated']
    search_fields = ['hp_name', 'created', 'updated']
    list_filter = ['hp_name', 'created', 'updated']
    list_per_page = 5


class MeterialAdmin(object):
    list_display = ['name', 'num', 'product', 'hp_name', 'created', 'updated']
    search_fields = ['name', 'num', 'product', 'hp_name', 'created', 'updated']
    list_filter = ['name', 'num', 'product', 'hp_name', 'created', 'updated']
    list_per_page = 5


class AssembliLineAdmin(object):
    assembly_line = True
    list_display = ['ass_name', 'leader']
    search_fields = ['ass_name', 'leader']
    list_filter = ['ass_name', 'leader']
    list_per_page = 5


class ProduceFormAdmin(object):
    create_produce = True
    update_produce = True
    list_display = ['pf_name', 'pro_name', 'pro_num', 'hpro_name', 'hpro_num', 'created',
                    'assembly_line', 'actual_num', 'is_instor', 'note', 'is_finish', 'qualified_rate']
    search_fields = ['pf_name', 'pro_name', 'pro_num', 'hpro_name', 'hpro_num', 'created',
                     'assembly_line', 'actual_num', 'is_instor', 'note', 'is_finish', 'qualified_rate']
    list_filter = ['pf_name', 'pro_name', 'pro_num', 'hpro_name', 'hpro_num', 'created',
                   'assembly_line', 'actual_num', 'is_instor', 'note', 'is_finish', 'qualified_rate']
    list_per_page = 5


class WasteFormAdmin(object):
    waste_form = True
    list_display = ['name', 'num', 'pf_name']
    search_fields = ['name', 'num', 'pf_name']
    list_filter = ['name', 'num', 'pf_name']
    list_per_page = 5


class CustomerAdmin(object):
    list_display = ['c_name', 'tel', 'addr']
    search_fields = ['c_name', 'tel', 'addr']
    list_filter = ['c_name', 'tel', 'addr']
    list_per_page = 5


class SaleFormAdmin(object):
    sale_form = True
    list_display = ['sf_name', 'staff_name', 'c_name', 'price', 'created', 'deliver_date',
                     'state', 'check', 'out_stor_date']
    search_fields = ['sf_name', 'staff_name', 'c_name', 'price', 'created', 'deliver_date',
                      'state', 'check', 'out_stor_date']
    list_filter = ['sf_name', 'staff_name', 'c_name', 'price', 'created', 'deliver_date',
                   'state', 'check', 'out_stor_date']
    list_per_page = 5
    data_charts = {
        "user_count": {'title': u"销售业绩", "x-field": "deliver_date", "y-field": ("price",),
                       "order": ('price',)},
    }


class SaleFormProductAdmin(object):
    sale_form_product = True
    list_display = ['sf_name', 'pro_name', 'num']
    search_fields = ['sf_name', 'pro_name', 'num']
    list_filter = ['sf_name', 'pro_name', 'num']
    list_per_page = 5


class PredictAdmin(object):
    list_display = ['pro_name', 'date', 'num']


class GlobalSetting(object):
    site_title = 'ERP'
    site_footer = '我的公司'
    menu_style = "accordion"
    global_models_icon = {
        Vender: "glyphicon glyphicon-user", RawMaterial: "glyphicon glyphicon-align-justify",
        Customer: "glyphicon glyphicon-user", AssemblyLine: 'glyphicon glyphicon-align-justify',
        Product: 'glyphicon glyphicon-align-justify', HalfProduct: 'glyphicon glyphicon-align-justify',
        Meterial: 'glyphicon glyphicon-align-justify', PredictData: 'glyphicon glyphicon-cloud',
        OrderForm: 'glyphicon glyphicon-book', SaleForm: 'glyphicon glyphicon-book',
        OrderFormGoods: 'glyphicon glyphicon-book', SaleFormProduct: 'glyphicon glyphicon-book',
        StorDetail: 'glyphicon glyphicon-book', OutStorDetail: 'glyphicon glyphicon-book',
        OutStorForm: 'glyphicon glyphicon-book', ProduceForm: 'glyphicon glyphicon-book',
        WasteForm: 'glyphicon glyphicon-book',
    }


xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(Vender, VenderAdmin)
xadmin.site.register(RawMaterial, RawMaterialAdmin)
xadmin.site.register(OrderForm, OrderFormAdmin)
xadmin.site.register(OrderFormGoods, OrderFormGoodsAdmin)
xadmin.site.register(StorDetail, StorDetailAdmin)
xadmin.site.register(OutStorForm, OutStoreFormAdmin)
xadmin.site.register(OutStorDetail, OutStorDetailAdmin)
xadmin.site.register(AssemblyLine, AssembliLineAdmin)
xadmin.site.register(Product, ProductAdmin)
xadmin.site.register(HalfProduct, HalfproductAdmin)
xadmin.site.register(Meterial, MeterialAdmin)
xadmin.site.register(ProduceForm, ProduceFormAdmin)
xadmin.site.register(WasteForm, WasteFormAdmin)
xadmin.site.register(Customer, CustomerAdmin)
xadmin.site.register(SaleForm, SaleFormAdmin)
xadmin.site.register(SaleFormProduct, SaleFormProductAdmin)
xadmin.site.register(PredictData, PredictAdmin)
