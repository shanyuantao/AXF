# AXF项目要点提示：

 Orders(goods)、Goods 、

外键正向取值:Goods.orders_set.all()

外键逆向取值：Order.goods



修改已有字段的值：s = OrderModel.objects.filter(pk=order.id).update(o_status=1)

s.delete()

s.save()

s.order_by('-price')



字符串分割： split('#')



request.method

request.GET.get

request.POST.get

request.FILES.get

```
request.user = user_ticket[0]
user = request.user

```

模型字段 user=user 等价于 user_id=user.id 外键关联

pk 相当于 id



```
return render(request, 'order/order_info.html', data)
return HttpResponseRedirect(reverse('mine:mine1'))
return render(request,'order/order_list_wait_pay.html', {'orders':orders})
return JsonResponse(data)
return HttpResponse('密码不正确')
```

```
response = HttpResponseRedirect('/mine/mine1/') 
response.set_cookie('ticket', ticket, expires=out_time)
ticket = request.COOKIES.get('ticket')
response = HttpResponseRedirect('/home/home1/')
response.delete_cookie('ticket')
```

