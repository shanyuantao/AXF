from django.db import models

# 父类
class Main(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    trackid = models.CharField(max_length=16)

    class Meta:
        abstract = True


# 用户
class UserModel(models.Model):

    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=64, unique=True)
    sex = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='icon')
    is_delete = models.BooleanField(default=False)
    ticket = models.CharField(max_length=255, default=True)
    out_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'axf_users'


# 用户订单
class OrderModel(models.Model):
    user = models.ForeignKey(UserModel)
    # 订单的数量
    o_num = models.CharField(max_length=64)
    # 订单的状态
    o_status = models.IntegerField(default=0)
    # 订单创建的时间
    o_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'axf_order'


# 轮循
class MainWheel(Main):
    class Meta:
        db_table = 'axf_wheel'


# 首页导航栏
class MainNav(Main):

    class Meta:
        db_table = 'axf_nav'


# 首页必购栏
class MainMustBuy(Main):

    class Meta:
        db_table = 'axf_mustbuy'


# 首页商店
class MainShop(Main):

    class Meta:
        db_table = 'axf_shop'


# 首页展示的商品
class MainShow(Main):
    categoryid = models.CharField(max_length=16)
    brandname = models.CharField(max_length=100)

    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=16)
    productid1 = models.CharField(max_length=16)
    longname1 = models.CharField(max_length=100)
    price1 = models.FloatField(default=0)
    marketprice1 = models.FloatField(default=1)

    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=16)
    productid2 = models.CharField(max_length=16)
    longname2 = models.CharField(max_length=100)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=1)

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=16)
    productid3 = models.CharField(max_length=16)
    longname3 = models.CharField(max_length=100)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=1)

    class Meta:
        db_table = 'axf_mainshow'


# 闪购侧边栏商品分类
class FoodType(models.Model):
    typeid = models.CharField(max_length=16)
    typename = models.CharField(max_length=100)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_foodtype'


# 所有的商品
class Goods(models.Model):
    productid = models.CharField(max_length=16)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=100)
    productlongname = models.CharField(max_length=200)
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=100)
    specifics = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=1)
    categoryid = models.CharField(max_length=16)
    childcid = models.CharField(max_length=16)
    childcidname = models.CharField(max_length=100)
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=1)
    productnum = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_goods'


# 购物车
class CartModel(models.Model):
    user = models.ForeignKey(UserModel)
    goods = models.ForeignKey(Goods)

    c_num = models.IntegerField(default=1)
    is_select = models.BooleanField(default=True)

    class Meta:
        db_table = 'axf_cart'


# 一个订单
class OrderModel(models.Model):
    # 用户id
    user = models.ForeignKey(UserModel)
    # 没用
    o_num = models.CharField(max_length=64)
    # 订单的状态
    o_status = models.IntegerField(default=0)
    # 订单创建的时间
    o_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'axf_order'


# 总的订单， 因为可能下好几次单
class OrderGoodsModel(models.Model):
    # 商品号
    goods = models.ForeignKey(Goods)
    # 订单号
    order = models.ForeignKey(OrderModel)
    # 每一种商品的数量
    goods_num = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_order_goods'


