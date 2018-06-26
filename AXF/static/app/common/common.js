// 添加商品
function addShop(goods_id){
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/axf/addgoods/',
        type:'POST',
        // 此处相当于表单的提交，在方法中可以利用request.POST.get('goods_id'),获得goods_id数据
        data:{'goods_id': goods_id},
        dataType:'json',
        headers:{'X-CSRFToken': csrf},
        // 访问url地址，所返回的东西都存在msg中
        success:function(msg){
            // goods_id 本来就是字符串类型
            $('#num_' + goods_id).html(msg.c_num)
        },
        error:function(msg){
            alert('请求错误')
        }
    });
}


//  减去商品
function subShop(goods_id){
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/axf/subgoods/',
        type:'POST',
        data:{'goods_id': goods_id},
        dataType:'json',
        headers:{'X-CSRFToken': csrf},
        success:function(msg){
            $('#num_' + goods_id).html(msg.c_num)
        },
        error:function(msg){
            alert('请求错误')
        }
    });
}


// 购物车选项
function cartchangeselect(cart_id){
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/axf/changeCartSelect/',
        type:'POST',
        data:{'cart_id':cart_id},
        dataType:'json',
        headers:{'X-CSRFToken':csrf},
        success:function(msg){
            if(msg.is_select){
                s = '<span onclick="cartchangeselect(' + cart_id +')">√</span>'
            }else{
                s = '<span onclick="cartchangeselect(' + cart_id +')">x</span>'
            }

            $('#changeselect_' + cart_id).html(s)
        },
        error:function(msg){
            alert('请求失败')
        }
    });
}