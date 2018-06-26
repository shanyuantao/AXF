import random
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse

from axf_app.models import UserModel, OrderModel, MainWheel, MainNav, MainShop, MainShow, MainMustBuy, FoodType, Goods, \
    CartModel, OrderGoodsModel


def Regist(request):

    if request.method == 'GET':
        return render(request, 'user/user_register.html')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        icon = request.FILES.get('icon')

        UserModel.objects.create(username=username, password=make_password(password),
                                 email=email, icon=icon)

        return HttpResponseRedirect(reverse('login:login1'))


def Login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = UserModel.objects.filter(username=username).first()
        if user:
            # 参数位置不可换， 第二个参数必须是数据库中的密码， 因为要进行解密
            if check_password(password, user.password):
                ticket = ''
                str = 'abcdefghijklmnopqrstuvwxyz'
                for x in range(15):
                    ticket += random.choice(str)
                out_time = datetime.now() + timedelta(days=1)
                response = HttpResponseRedirect('/axf/mine/')
                response.set_cookie('ticket', ticket, expires=out_time)

                user.ticket = ticket
                user.out_time = out_time
                user.save()

                return response
            else:
                return HttpResponse('密码不正确')
        else:
            return HttpResponse('用户不存在')


# 我的页面
def Mine(request):
    if request.method == 'GET':
        user = request.user
        data = {}
        if user.username:
            # 一个用户可以下多个订单，利用外键关系， 正向取出，用户下的所有订单
            orders = user.ordermodel_set.all()
            wait_pay, payed = 0, 0
            for order in orders:
                if order.o_status == 0:
                    wait_pay += 1
                elif order.o_status == 1:
                    payed += 1
            data = {
                'wait_pay': wait_pay,
                'payed': payed
            }
            return render(request, 'mine/mine.html', data)
        return render(request, 'mine/mine.html')


# 待付款
def order_wait_pay(request):
    if request.method == 'GET':
        # request中放的键值对，只要不删除什么时候都可以使用
        user = request.user
        if user and user.id:
            orders = OrderModel.objects.filter(user=user, o_status=0)
            return render(request, 'order/order_list_wait_pay.html', {'orders': orders})


# 带收货
def order_wait_shouhuo(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            orders = OrderModel.objects.filter(user=user, o_status=1)
            return render(request, 'order/order_list_payed.html', {'order': orders})


# 退出登录
def Logout(request):
    if request.method == 'GET':
        response = HttpResponseRedirect('/login/login1/')
        response.delete_cookie('ticekt')
        ticket = request.COOKIES.get('ticket')
        # UserModel.objects.filter(ticket=ticket).delete()
        return response


# 首页
def home(request):
    if request.method == 'GET':
        data = {
            'mainwheels': MainWheel.objects.all(),
            'mainnavs': MainNav.objects.all(),
            'mainmustbuys': MainMustBuy.objects.all(),
            'mainshops1': MainShop.objects.filter(id=1),
            'mainshops2': MainShop.objects.filter(id__gte=2, id__lte=3),
            'mainshops3': MainShop.objects.filter(id__gte=4, id__lte=7),
            'mainshops4': MainShop.objects.filter(id__gte=8, id__lte=11),
            'mainshows': MainShow.objects.all()
        }
        return render(request, 'home/home.html', data)


# 闪购超市跳转链接， 为了给url传参
def flash_buy(request):

    return HttpResponseRedirect(reverse('axf:marketparams', args=('104749', '0', '0')))


# 提示： 标签和商品是分开的， 由于参数过多， 所以参数子页面中a链接传来， 也从这里传入页面，
# 因为参数可能有不动，保留 全部分类，只改变子分类，前两个不动， 只动第三个
# 闪购超市  url访问该方法时， 接收url中的参数
def market(request, typeid, cid, sort_id):
    if request.method == 'GET':
        # 根据传入的参数，取出商品
        if cid == '0':
            # 取出全部分类的商品
            goods_types = Goods.objects.filter(categoryid=typeid)
        else:
            # 取出子分类下的商品
            goods_types = Goods.objects.filter(categoryid=typeid, childcid=cid)

        if sort_id == '0':
            pass
        elif sort_id == '1':
            # 得到排序之后对应的子分类下的排序之后的商品(按销量排序)
            goods_types = goods_types.order_by('productnum')
        elif sort_id == '2':
            # 价格从高到底排序
            goods_types = goods_types.order_by('-price')
        elif sort_id == '3':
            goods_types = goods_types.order_by('price')

        # 根据传入的参数，取出对应的分类名称
        foodtypes_childnames = FoodType.objects.filter(typeid=typeid).first()
        # 取出子分类的名字，一个全部分类对应多个子分类
        childtypenames = foodtypes_childnames.childtypenames
        childtypenames_list = childtypenames.split('#')
        child_types_list = []
        for childtypename in childtypenames_list:
            child_types_list.append(childtypename.split(':'))

        # 取出所有分类的名字， 用来填充分类标签
        foodtypes = FoodType.objects.all()

        data = {}
        data['foodtypes'] = foodtypes
        data['typeid'] = typeid
        data['cid'] = cid
        # 取出的商品
        data['goods_types'] = goods_types
        # 取出的分类标签
        data['child_types_list'] = child_types_list

        return render(request, 'market/market.html', data)


# 添加商品
def add_goods(request):
    if request.method == 'POST':
        data = {
            'msg': '请求成功',
            'code': '200'
        }
        user = request.user
        if user and user.id:
            goods_id = request.POST.get('goods_id')
            # 购物车外键关联user, 一个用户对应多个外键， 故user_id= user.id这里等价于user=user
            user_carts = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            # 如果购物车中该用户已经添加了商品， 进行 数量加 1
            if user_carts:
                user_carts.c_num += 1
                # 往已有记录中添加内容要保存，该记录要进行保存
                user_carts.save()
                data['c_num'] = user_carts.c_num
            # 如果该用户第一次添加该商品，则在购物车中新建一条商品记录
            else:
                CartModel.objects.create(user=user, goods_id=goods_id, c_num=1)
                # 第一次商品的数量为 1，再添加就执行上面的if条件了
                data['c_num'] = 1
        return JsonResponse(data)


# 减去商品
def sub_goods(request):
    if request.method == 'POST':
        data = {
            'code': '200',
            'msg': '请求成功'
        }
        user = request.user
        goods_id = request.POST.get('goods_id')
        if user and user.id:
            user_carts  = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            if user_carts:
                if user_carts.c_num == '1':
                    user_carts.delete()
                    data['c_num'] = 0
                else:
                    user_carts.c_num -= 1
                    user_carts.save()
                    data['c_num'] = user_carts.c_num
        return JsonResponse(data)


# 购物车
def cart(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            carts = CartModel.objects.filter(user=user)
            return render(request, 'cart/cart.html', {'carts': carts})
        else:
            return HttpResponseRedirect(reverse('login:login1'))


# 购物车中的商品勾选框
def change_select_goods(request):

    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        user = request.user
        data = {
            'code': '200',
            'msg': '请求成功'
        }
        if user and user.id:
            cart = CartModel.objects.filter(pk=cart_id).first()
            if cart.is_select:
                cart.is_select = False
            else:
                cart.is_select = True
            # 修改已有字段的内容也要保存
            cart.save()
            data['is_select'] = cart.is_select
        return JsonResponse(data)


# order是购物车中选中的商品，该订单包含了订单的编号、订单的状态； ordergoodsmodel用来盛放购物车中的商品
# 和该商品所对应得订单号、还有商品的对应的数量
def generate_order(request):

    if request.method == 'GET':
        user = request.user
        if user and user.id:
            # 购物车中点击下单时， 下单全部勾选的商品，下单过的购物车中的商品要进行删除
            carts_goods = CartModel.objects.filter(is_select=True)
            # 先创建一个订单
            order = OrderModel.objects.create(user=user, o_status=0)
            for carts in carts_goods:
                # 把勾选的所有的商品依次填进订单表格中 order_id = order.id
                OrderGoodsModel.objects.create(goods=carts.goods, order=order, goods_num=carts.c_num)
                carts.delete()
            return HttpResponseRedirect(reverse('axf:user_pay_order', args=(str(order.id),)))


# 订单详情页面
def user_pay_order(request, order_id):
    if request.method == 'GET':
        # 根据订单id找到该订单 order, 该订单刚下单直接跳转到订单详情页面
        orders = OrderModel.objects.filter(pk=order_id).first()
        data = {
            'order_id': order_id,
            'orders': orders
        }
        return render(request, 'order/order_info.html', data)


# 订单支付，由于没有微信接口， 把订单状态改成已支付状态，后跳转到我的页面
def order_pay(request, order_id):
    if request.method == 'GET':
        OrderModel.objects.filter(pk=order_id).update(o_status=1)
        return HttpResponseRedirect(reverse('axf:mine'))


# 我的页面中点击待支付时，跳转到待支付页面
def order_wait_pay(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            orders = OrderModel.objects.filter(user=user, o_status=0)
            return render(request, 'order/order_list_wait_pay.html', {'orders': orders})


# 我的页面中点击待收货的方法
def order_wait_shouhuo(request):

    if request.method == 'GET':
        user = request.user
        if user and user.id:
            orders = OrderModel.objects.filter(user=user, o_status=1)
            return render(request, 'order/order_list_payed.html', {'orders': orders})







