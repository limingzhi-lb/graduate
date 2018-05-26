from django.db import models
from users.models import User


class RawMaterial(models.Model):
    rm_name = models.CharField('名称', max_length=24)
    price = models.FloatField('价格')
    classification = models.CharField('分类', max_length=8)
    minimum_inventory = models.IntegerField('最小库存')
    created = models.DateTimeField('创建时间')
    updated = models.DateTimeField('更新时间')

    class Meta:

        db_table = 'RawMaterial'
        verbose_name = '原材料'
        verbose_name_plural = '原材料'

    def __str__(self):
        return self.rm_name


class Vender(models.Model):
    ven_name = models.CharField('名称', max_length=24)
    addr = models.CharField('地址', max_length=24)
    tel = models.CharField('电话', max_length=12)
    created = models.DateTimeField('创建时间')
    updated = models.DateTimeField('更新时间')
    rm_name = models.ManyToManyField(RawMaterial, verbose_name='原材料')

    class Meta:
        db_table = 'Vender'
        verbose_name = '供货商'
        verbose_name_plural = '供货商'

    def __str__(self):
        return self.ven_name


class StorDetail(models.Model):
    good_name = models.CharField('货物名称', max_length=12)
    num = models.IntegerField('数量')

    class Meta:
        db_table = 'StorDetail'
        verbose_name = '仓库详情'
        verbose_name_plural = '仓库详情'

    def __str__(self):
        return self.good_name


class OrderForm(models.Model):
    of_name = models.CharField('订单名称', max_length=32, unique=True)
    ven_name = models.ForeignKey(Vender, related_name='order_form_ven_name', verbose_name='供货商')
    created = models.DateTimeField('创建时间')
    delivery = models.DateTimeField('交货时间', blank=True, null=True)
    typ = models.BooleanField('采购订单', default=True)
    receipt_status = models.BooleanField('已收货', default=False)
    payment_status = models.BooleanField('已支付', default=False)
    total_price = models.FloatField('总价', blank=True, null=True)
    executor = models.ForeignKey(User, related_name='order_form_username', verbose_name='执行人')
    storage_time = models.DateTimeField('入库时间', blank=True, null=True)
    is_finish = models.BooleanField('是否完成', default=False)

    class Meta:
        db_table = 'OrderForm'
        verbose_name = '订单'
        verbose_name_plural = '订单'

    def __str__(self):
        return self.of_name


class OrderFormGoods(models.Model):
    rm_name = models.ForeignKey(RawMaterial, related_name='order_form_goods_rm_name', verbose_name='材料')
    num = models.IntegerField('数量', null=True)
    of_name = models.ForeignKey(OrderForm, related_name='order_form_goods_of_name', verbose_name='订单')

    class Meta:
        db_table = 'OrderFormGoods'
        verbose_name = '订单中商品'
        verbose_name_plural = '订单中商品'

    def __str__(self):
        return self.rm_name.rm_name


class OutStorForm(models.Model):
    osf_name = models.CharField('表名', max_length=32, unique=True)
    created = models.DateTimeField('创建时间')
    staff_id = models.ForeignKey(User, related_name='out_store_form_username', verbose_name='执行人')
    check = models.BooleanField('是否确认', default=False, blank=True)
    note = models.CharField('备注', max_length=64, blank=True, null=True)
    finished = models.DateTimeField('完成时间', blank=True, null=True)

    class Meta:
        db_table = 'OutStorForm'
        verbose_name = '出库表'
        verbose_name_plural = '出库表'

    def __str__(self):
        return self.osf_name


class OutStorDetail(models.Model):
    good_name = models.ForeignKey(StorDetail, related_name='out_store_detail_good_name', verbose_name='货物名')
    num = models.IntegerField('数量')
    osf_name = models.ForeignKey(OutStorForm, related_name='out_store_detail_osf_name', verbose_name='出库表')

    class Meta:
        db_table = 'OutStorDetail'
        verbose_name = '出库货物'
        verbose_name_plural = '出库货物'

    def __str__(self):
        return self.good_name.good_name


class Product(models.Model):
    pro_name = models.CharField('产品名', max_length=8)
    price = models.FloatField('价格')
    created = models.DateTimeField('创建时间')
    updated = models.DateTimeField('更新时间')

    class Meta:
        db_table = 'Product'
        verbose_name = '产品'
        verbose_name_plural = '产品'

    def __str__(self):
        return self.pro_name


class HalfProduct(models.Model):
    hp_name = models.CharField('半成品名', max_length=8)
    created = models.DateTimeField('创建时间')
    updated = models.DateTimeField('更新时间')

    class Meta:
        db_table = 'HalfProduct'
        verbose_name = '半成品'
        verbose_name_plural = '半成品'

    def __str__(self):
        return self.hp_name


class Meterial(models.Model):
    name = models.ForeignKey(StorDetail, related_name='meterial_good_name', verbose_name='材料')
    num = models.IntegerField('数量')
    product = models.ForeignKey(Product, related_name='meterial_pro_name', null=True, verbose_name='成品',blank=True)
    hp_name = models.ForeignKey(HalfProduct, related_name='meterial_hp_name', null=True, verbose_name='半成品', blank=True)
    created = models.DateTimeField('创建时间')
    updated = models.DateTimeField('更新时间')

    class Meta:
        db_table = 'Meterial'
        verbose_name = '零部件'
        verbose_name_plural = '零部件'

    def __str__(self):
        return self.name.good_name


class AssemblyLine(models.Model):
    ass_name = models.CharField('名称', max_length=24)
    leader = models.ForeignKey(User, related_name='AsseblyLine', verbose_name='负责人')
    created = models.DateTimeField('创建时间')
    updated = models.DateTimeField('更新时间')

    class Meta:
        db_table = 'AssemblyLine'
        verbose_name = '生产线'
        verbose_name_plural = '生产线'

    def __str__(self):
        return self.ass_name


class ProduceForm(models.Model):
    pf_name = models.CharField('表名', max_length=32, unique=True)
    pro_name = models.ForeignKey(Product, related_name='produce_form_pro_name', verbose_name='成品', blank=True, null=True)
    pro_num = models.IntegerField('成品数量', blank=True, null=True)
    hpro_name = models.ForeignKey(HalfProduct, related_name='produce_form_hp_name', verbose_name='半成品', blank=True, null=True)
    hpro_num = models.IntegerField('半成品数量', blank=True, null=True)
    created = models.DateTimeField('创建时间')
    assembly_line = models.ForeignKey(AssemblyLine, related_name='produce_form_ass_name', verbose_name='生产线')
    actual_num = models.IntegerField('实际数量', blank=True, null=True)
    is_instor = models.BooleanField('是否入库', default=False, blank=True)
    is_finish = models.BooleanField('是否完成', default=False, blank=True)
    qualified_rate = models.FloatField('合格率', blank=True, null=True)
    note = models.TextField('备注', blank=True)

    class Meta:
        db_table = 'ProduceForm'
        verbose_name = '生产目标'
        verbose_name_plural = '生产目标'

    def __str__(self):
        return self.pf_name


class WasteForm(models.Model):
    name = models.ForeignKey(StorDetail, related_name='waste_form_good_name', verbose_name='材料')
    num = models.IntegerField('数量')
    pf_name = models.ForeignKey(ProduceForm, related_name='waste_product', verbose_name='生产目标表')

    class Meta:
        db_table = 'WasteForm'
        verbose_name = '废料表'
        verbose_name_plural = '废料表'

    def __str__(self):
        return self.name.good_name


class Customer(models.Model):
    c_name = models.CharField('客户名', max_length=24)
    tel = models.CharField('电话', max_length=12)
    addr = models.CharField('地址', max_length=32)

    class Meta:
        db_table = 'Customer'
        verbose_name = '客户'
        verbose_name_plural = '客户'

    def __str__(self):
        return self.c_name


class SaleForm(models.Model):
    sf_name = models.CharField('表名', max_length=32, unique=True)
    staff_name = models.ForeignKey(User, related_name='sale_form_username', verbose_name='执行人')
    c_name = models.ForeignKey(Customer, related_name='sale_form_c_name', verbose_name='客户')
    price = models.FloatField('价格', null=True, blank=True)
    created = models.DateTimeField('创建时间')
    deliver_date = models.DateField('交货时间', null=True, blank=True)
    state = models.BooleanField('是否发货', default=False, blank=True)
    check = models.BooleanField('是否确认', default=False, blank=True)
    out_stor_date = models.DateTimeField('出库时间', null=True, blank=True)

    class Meta:
        db_table = 'SaleForm'
        verbose_name = '销售订单'
        verbose_name_plural = '销售订单'

    def __str__(self):
        return self.sf_name


class SaleFormProduct(models.Model):
    sf_name = models.ForeignKey(SaleForm, related_name='sale_form_product_sf_name', verbose_name='销售订单')
    pro_name = models.ForeignKey(Product, related_name='sale_form_product_pro_name', verbose_name='产品')
    num = models.IntegerField('数量')

    class Meta:
        db_table = 'SaleFormProduct'
        verbose_name = '订单产品'
        verbose_name_plural = '订单产品'

    def __str__(self):
        return self.sf_name.sf_name


class PredictData(models.Model):
    pro_name = models.ForeignKey(Product, related_name='predict_pro_name', verbose_name='产品')
    date = models.DateField('日期')
    num = models.IntegerField('数量')

    class Meta:
        db_table = 'PredictData'
        verbose_name = '销量预测'
        verbose_name_plural = '销量预测'

    def __str__(self):
        return self.pro_name


