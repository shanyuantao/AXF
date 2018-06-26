from django.conf.urls import url
from axf_app import views

urlpatterns = [
    url(r'^regist1/', views.Regist, name='regist1'),
    url(r'^login1/', views.Login, name='login1'),
    url(r'^logout/', views.Logout, name='logout1'),

    # 我的页面
    url(r'^mine/', views.Mine, name='mine'),
    url(r'^order_wait_pay', views.order_wait_pay, name='order_wait_pay'),
    url(r'^order_wait_shouhuo', views.order_wait_shouhuo, name='order_wait_shouhuo'),

    # 首页
    url(r'home/', views.home, name='home'),

    # 闪购
    url(r'flash_buy/', views.flash_buy, name='flash_buy'),
    url(r'^market/(\d+)/(\d+)/(\d+)/', views.market, name='marketparams'),

    # 购物车
    url(r'cart/', views.cart, name='cart'),
    url(r'^changeCartSelect/', views.change_select_goods, name='change_select'),
    url(r'^user_generate_order/', views.generate_order, name='generate_order'),
    url(r'^user_pay_order/(\d+)/', views.user_pay_order, name='user_pay_order'),
    url(r'^order_pay/(\d+)/', views.order_pay, name='order_pay'),
    url(r'^order_wait_pay/', views.order_wait_pay, name='order_wait_pay'),
    url(r'^order_wait_shouhuo/', views.order_wait_shouhuo, name='order_wait_shouhuo'),

    # 增减商品
    url(r'^addgoods/', views.add_goods, name='addgoods'),
    url(r'^subgoods/', views.sub_goods, name='subgoods'),




]
