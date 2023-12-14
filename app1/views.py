import json
from datetime import datetime

from _decimal import Decimal


from django.contrib.auth.hashers import make_password
from django.utils.timezone import localtime

from .models import *
from .tools import *
# Create your views here.
SALT = '123'
DATE_TIME_FORMAT = '%Y-%m-%d %H:%M'
class Identity:
    BUYER = 'buyer'
    STAFF = 'staff'
    CANTEEN = 'canteen'

def buyer_register(request):
    print(request.body)
    data = json.loads(request.body)
    account = data['account']
    tele = data['tele']
    password = data['password']
    again = data['again']
    nick = data['nick']

    if password != again:
        return JsonResponse({'status' : 3})
    if Buyer.objects.filter(account = account).count() != 0:
        return JsonResponse({'status' : 2})
    if Buyer.objects.filter(tele = tele).count() != 0:
        return JsonResponse({'status' : 1})

    password = make_password(password,SALT)
    #   要上传img id怎么来？
    pic = Image(img=data['img'])
    pic.save()
    new_buyer = Buyer(account=account,password=password,tele=tele,img=pic,nick_name=nick)
    new_buyer.save()
    return JsonResponse({'status' : 0})


def canteen_register(request):
    data = json.loads(request.body)
    account = data['account']
    tele = data['tele']
    password = data['password']
    again = data['again']
    if password != again:
        return JsonResponse({'status' : 3})
    if Canteen.objects.filter(account = account).count() != 0:
        return JsonResponse({'status' : 2})
    if Canteen.objects.filter(tele = tele).count() != 0:
        return JsonResponse({'status' : 1})
    password = make_password(password, SALT)
    #   要上传img id怎么来？
    pic = Image(img=data['img'])
    pic.save()
    #   description = models.CharField(max_length=200)
    #     location = models.CharField(max_length=20)
    new_canteen = Canteen(account=account, password=password, tele=tele, img=pic,
                        description = data['description'], location = data['location'])
    new_canteen.save()
    return JsonResponse({'status': 0})

def staff_register(request):
    data = json.loads(request.body)
    account = data['account']
    tele = data['tele']
    password = data['password']
    again = data['again']
    if password != again:
        return JsonResponse({'status': 3})
    if Canteen.objects.filter(account=account).count() != 0:
        return JsonResponse({'status': 2})
    if Canteen.objects.filter(tele=tele).count() != 0:
        return JsonResponse({'status': 1})
    password = make_password(password, SALT)
    #   要上传img id怎么来？
    pic = Image(img=data['img'])
    pic.save()
    new_staff = Staff(account=account, password=password, tele=tele, img=pic,real_name=data['real_name'])
    new_staff.save()
    return JsonResponse({'status': 0})

def login(request):
    data = json.loads(request.body)
    account = data['account']
    password = data['password']
    password = make_password(password,SALT)
    identity = data['identity']
    id = -1
    status = 0
    print(identity)
    print(Identity.BUYER)
    #   admin的内容存在程序里
    if identity == Identity.BUYER:
        try:
            buyer = Buyer.objects.get(account=account)
        except:
            return JsonResponse({'status' : 1})
            #   status = 1

        if buyer.password != password:
            return JsonResponse({'status' : 2})
            #   status = 2
        else:
            id = buyer.id

    elif identity == Identity.CANTEEN:
        try:
            canteen = Canteen.objects.get(account=account)
        except:
            return JsonResponse({'status' : 1})
            #   status = 1
        if canteen.password != password:
            return JsonResponse({'status' : 2})
            #   status = 2
        else:
            id = canteen.id


    elif identity == Identity.STAFF:
        try:
            staff = Staff.objects.get(account=account)
        #   if staff is None:
        except:
            return JsonResponse({'status' : 1})
            #   status = 1
        if staff.password != password:
            return JsonResponse({'status' : 2})
            #   status = 2
        else:
            id = staff.id

    else:
        #   非法身份
        status = 3

    return JsonResponse({
        'status' : status,
        'token' : msg2token(id, identity)
    })


@check_token(Identity.BUYER,Identity.CANTEEN,Identity.BUYER)
def reset_password(request):
    token = get_token(request)
    message = token2msg(token)
    if isinstance(message,int):
        return JsonResponse({'status' : message})
    data = json.loads(request.body)
    id = message['id']
    identity = message['identity']
    old = data['old']
    new = data['new']
    again = data['again']
    status = 0

    if new != again:
        status = 2
    else:
        old = make_password(old, SALT)
        new = make_password(new,SALT)

        if identity == Identity.BUYER:
            buyer = Buyer.objects.get(id=id)
            #   password = buyer.password
            if old != buyer.password:
                status = 1
            else:
                buyer.password = new
                buyer.save()
        elif identity == Identity.STAFF:
            staff = Staff.objects.get(id=id)
            if old != staff.password:
                status = 1
            else:
                staff.password = new
                staff.save()
        elif identity == Identity.CANTEEN:
            canteen = Canteen.objects.get(id=id)
            if old != canteen.password:
                status = 1
            else:
                canteen.password = new
                canteen.save()

    return JsonResponse({'status' : status})


@check_token(Identity.BUYER,Identity.STAFF,Identity.CANTEEN)
def reset_picture(request):
    token = get_token(request)
    message = token2msg(token)
    if isinstance(message,int):
        return JsonResponse({'status' : message})
    data = json.loads(request.body)
    id = message['id']
    identity = message['identity']
    status = 0
    pic = Image(img=data['img'])
    pic.save()
    if identity == Identity.BUYER:
        buyer = Buyer.objects.get(id=id)
        buyer.img = pic
        buyer.save()
    elif identity == Identity.STAFF:
        staff = Staff.objects.get(id=id)
        staff.img = pic
        staff.save()
    elif identity == Identity.CANTEEN:
        canteen = Canteen.objects.get(id=id)
        canteen.img = pic
        canteen.save()

    return JsonResponse({'status' : status})


#   买家功能
@check_token(Identity.BUYER)
def get_all_canteens(request):
    token = get_token(request)
    message = token2msg(token)
    if isinstance(message, int):
        return JsonResponse({'status': message})

    identity = message['identity']
    if identity != Identity.BUYER:
        return JsonResponse({'status': -3})
    canteen_list = []
    canteens = Canteen.objects.all()
    for i in canteens:
        canteen_list.append({
            'id' : i.id,
            'description' : i.description,
            'location' : i.location,
            'img' : i.img.img
        })

    return JsonResponse({
        'status' : 0,
        'canteens' : canteen_list
    },json_dumps_params={'ensure_ascii': False})


@check_token(Identity.BUYER)
def get_available_dishes(request):
    token = get_token(request)
    message = token2msg(token)
    if isinstance(message, int):
        return JsonResponse({'status': message})

    identity = message['identity']
    if identity != Identity.BUYER:
        return JsonResponse({'status': -3})

    data = json.loads(request.body)
    canteen_id = data['id']
    av_dish_list = []
    dishes = Dish.objects.filter(canteen_id=canteen_id,available=True)
    for i in dishes:
        av_dish_list.append({
            'id' : i.id,
            'name' : i.name,
            'price' : i.price,
            'description' : i.description,
            'img' : i.img.img
        })
    return JsonResponse({
        'status' : 0,
        'dishes' : av_dish_list
    },json_dumps_params={'ensure_ascii': False})


@check_token(Identity.BUYER)
def build_order(request):
    token = get_token(request)
    message = token2msg(token)
    if isinstance(message, int):
        return JsonResponse({'status': message})

    identity = message['identity']
    if identity != Identity.BUYER:
        return JsonResponse({'status': -3})

    id = message['id']
    orders = Order.objects.filter(buyer_id=id,status=0)
    if orders.count() != 0:
        return JsonResponse({
            'status' : 1
        })
    else:
        buyer = Buyer.objects.get(id=id)
        order = Order(buyer=buyer)
        order.save()
        return JsonResponse({
            'status' : 0,
            'order_id' : order.id
        })


@check_token(Identity.BUYER)
def add_dish_to_order(request):
    token = get_token(request)
    message = token2msg(token)
    if isinstance(message, int):
        return JsonResponse({'status': message})

    identity = message['identity']
    if identity != Identity.BUYER:
        return JsonResponse({'status': -3})

    data = json.loads(request.body)
    id = message['id']
    try:
        order = Order.objects.get(buyer_id=id,status=0)
    except:
        order = Order(buyer_id=id,status=0)
        order.save()

    dish_id = data['dish_id']
    print("dish_id: "  ,dish_id)
    num = data['num']
    try:
        od = OrderDish.objects.get(order_id=order.id,dish_id=dish_id)
        od.num += num
    except:
        od = OrderDish(order_id=order.id, dish_id=dish_id, num=num)

    od.save()
    return JsonResponse({'status' : 0})

@check_token(Identity.BUYER)
def get_cart(request):
    token = get_token(request)
    message = token2msg(token)
    if isinstance(message, int):
        return JsonResponse({'status': message})

    identity = message['identity']
    if identity != Identity.BUYER:
        return JsonResponse({'status': -3})

    id = message['id']
    try:
        order = Order.objects.get(buyer_id=id,status=0)
    except:
        return JsonResponse({
            'status' : 1,
            'msg' : "购物车为空"
        })

    ods = OrderDish.objects.filter(order_id=order.id)
    dish_list = []
    total_price = 0
    for i in ods:
        dish = i.dish
        total_price += i.num * dish.price
        dish_list.append({
            'id' : dish.id,
            'name' : dish.name,
            'num' : i.num,
            'price' : dish.price,
            'description' : dish.description,
            'img' : dish.img.img,

        })

    return JsonResponse({
        'status' : 0,
        'total_price' : total_price,
        'dishes' : dish_list
    },json_dumps_params={'ensure_ascii': False})

@check_token(Identity.BUYER)
def change_dish_in_cart(request):
    token = get_token(request)
    message = token2msg(token)
    if isinstance(message, int):
        return JsonResponse({'status': message})

    identity = message['identity']
    if identity != Identity.BUYER:
        return JsonResponse({'status': -3})

    id = message['id']
    try:
        order = Order.objects.get(buyer_id=id, status=0)
    except:
        return JsonResponse({
            'status' : 2,
            'msg' : '购物车为空'
        })
    data = json.loads(request.body)
    dish_id = data['dish_id']
    num = data['num']

    #   print(dish_id)
    #   print(order.id)
    #   od_tem = OrderDish.objects.get(order=order)
    #   print(od_tem.dish.id)
    try:
        od = OrderDish.objects.get(order_id=order.id,dish_id=dish_id)
    except:
        return JsonResponse({'status': 1})

    if num <= 0:
        od.delete()
    else:
        od.num = num
        od.save()
    return JsonResponse({'status' : 0})

@check_token(Identity.BUYER)
def submit_order(request):
    token = get_token(request)
    message = token2msg(token)
    if isinstance(message, int):
        return JsonResponse({'status': message})

    identity = message['identity']
    if identity != Identity.BUYER:
        return JsonResponse({'status': -3})

    id = message['id']
    try:
        order = Order.objects.get(buyer_id=id, status=0)
    except:
        return JsonResponse({
            'status' : 1,
            'msg' : '购物车为空'
        })
    ods = OrderDish.objects.filter(order_id=order.id)
    if ods.count() == 0:
        return JsonResponse({'status' : 1})
    data = json.loads(request.body)
    expected_time = data['time']
    print(expected_time)
    order.expected_finish_time = datetime.strptime(expected_time,DATE_TIME_FORMAT)
    order.destination = data['destination']
    order.status = 1
    order.save()
    return JsonResponse({'status' : 0})

@check_token(Identity.BUYER)
def get_buyer_all_orders(request):
    token = get_token(request)
    message = token2msg(token)
    id = message['id']
    # 获得所有完成的订单
    orders = Order.objects.filter(buyer_id=id,status__gt=0)
    #   除了购物车
    order_list = []
    for i in orders:
        #   staff = Staff.objects.get(id=i.staff_id)
        #   ods = OrderDish.objects.filter(order_id=i.id)
        status = '未接单' if i.status == 1 else ('配送中' if i.status == 2 else '交易完成')
        #   res = get_order_info_(i.id)
        order_list.append({
            'order_id': i.id,
            'create_time': localtime(i.create_time).strftime(DATE_TIME_FORMAT),
            'status' : status,
            'destination' : i.destination,
            #   toString格式
            #   'total_price' : res[1],
            #   'dishes' : res[0]
        })

    return JsonResponse({
        'status': 0,
        'orders': order_list
    }, json_dumps_params={'ensure_ascii': False})

# 已经完成的订单
@check_token(Identity.BUYER)
def get_buyer_history_orders(request):
    token = get_token(request)
    message = token2msg(token)
    if isinstance(message, int):
        return JsonResponse({'status': message})

    identity = message['identity']
    if identity != Identity.BUYER:
        return JsonResponse({'status': -3})

    id = message['id']
    # 获得所有完成的订单
    orders = Order.objects.filter(buyer_id=id,status=3)
    order_list = []
    for i in orders:
        staff = Staff.objects.get(id=i.staff_id)
        #   ods = OrderDish.objects.filter(order_id=i.id)
        #   res = get_order_info_(i.id)
        order_list.append({
            'order_id' : i.id,
            'create_time' : localtime(i.create_time).strftime(DATE_TIME_FORMAT),
            #   toString格式
            'finish_time' :i.finish_time,
            'destination' : i.destination,
            'staff_id' : staff.id,
            'staff_name' : staff.real_name,
            'staff_tele' : staff.tele,
            #   'total_price' : res[1],
            #   'dishes' : res[0]
        })

    return JsonResponse({
        'status' : 0,
        'orders' : order_list
    },json_dumps_params={'ensure_ascii': False})

#   配送中的订单
@check_token(Identity.BUYER)
def get_buyer_delivery_orders(request):
    token = get_token(request)
    message = token2msg(token)
    id = message['id']
    orders = Order.objects.filter(buyer_id=id,status=2)
    print("here",orders)
    order_list = []
    for i in orders:
        staff = Staff.objects.get(id=i.staff_id)
        #   res = get_order_info_(i.id)
        order_list.append({
            'id': i.id,
            'create_time': localtime(i.create_time).strftime(DATE_TIME_FORMAT),
            'expected_finish_time': localtime(i.expected_finish_time).strftime(DATE_TIME_FORMAT),
            'destination' : i.destination,
            'staff_id': staff.id,
            'staff_name': staff.real_name,
            'staff_tele': staff.tele,
            #   'total_price': res[1],
            #   'dishes': res[0]
        })

    return JsonResponse({
        'status': 0,
        'orders': order_list
    })

# 未被接取的订单 可以撤销
@check_token(Identity.BUYER)
def get_not_taken_orders(request):
    token = get_token(request)
    message = token2msg(token)
    if isinstance(message, int):
        return JsonResponse({'status': message})

    #   data = json.loads(request.body)
    id = message['id']
    identity = message['identity']
    if identity != Identity.BUYER:
        return JsonResponse({'status': -3})

    orders = Order.objects.filter(buyer_id=id,status=1)
    order_list = []
    for i in orders:
        #   res = get_order_info_(i.id)
        order_list.append({
            'id' : i.id,
            'destination' : i.destination,
            'create_time' : localtime(i.create_time).strftime(DATE_TIME_FORMAT),
            'expected_finish_time' : localtime(i.expected_finish_time).strftime(DATE_TIME_FORMAT),
            #   'total_price': res[1],
            #   'dishes': res[0]
        })

    return JsonResponse({
        'status' : 0,
        'orders' : order_list
    })

@check_token(Identity.BUYER)
def cancel_order(request):
    token = get_token(request)
    message = token2msg(token)
    if isinstance(message, int):
        return JsonResponse({'status': message})

    identity = message['identity']
    if identity != Identity.BUYER:
        return JsonResponse({'status': -3})


    data = json.loads(request.body)
    order_id = data['order_id']
    try:
        order = Order.objects.get(id=order_id)
    except:
        return JsonResponse({
            'status' : 2,
            'msg' : '订单不存在或已被删除'
        })
    if order.status != 1:
        return JsonResponse({'status' : 1})
    else:
        order.delete()
        return JsonResponse({'status' : 0})


#   TODO:做评论系统 订单要不要有finish_time 做外卖员系统


# 外卖员功能

@check_token(Identity.STAFF)
def get_orders(request):

    not_taken_orders = Order.objects.filter(status=1).order_by('expected_finish_time')
    order_list = []
    for i in not_taken_orders:
        #   把order_id对应的菜品和num查出来 进行运算
        total_price = Decimal("0")
        dish_list = OrderDish.objects.filter(order_id=i.id).values('dish_id','num')
        for j in dish_list:
            dish = Dish.objects.get(id=j['dish_id'])
            total_price += dish.price * j['num']

        order_list.append({
            'order_id' : i.id,
            'total_price' : str(total_price),
            'destination' : i.destination,
            'buyer_tele' : i.buyer.tele,
            'expected_finish_time' : localtime(i.expected_finish_time).strftime(DATE_TIME_FORMAT)
        })

    return JsonResponse({
        'status' : 0,
        'orders' : order_list
    })

@check_token(Identity.STAFF)
def take_order(request):
    token = get_token(request)
    message = token2msg(token)

    id = message['id']
    data = json.loads(request.body)
    order_id = data['order_id']
    print(order_id)
    try:
        order = Order.objects.get(id=order_id)
    except:
        return JsonResponse({
            'status' : 1
        })


    if order.status != 1:
        return JsonResponse({
            'status' : 1
        })

    order.staff_id = id
    order.status = 2
    order.save()
    return JsonResponse({
        'status' : 0
    })

@check_token(Identity.STAFF)
def get_staff_history_order(request):
    token = get_token(request)
    message = token2msg(token)
    id = message['id']
    order_list = Order.objects.filter(staff_id=id,status=3)
    orders = []
    for i in order_list:
        orders.append({
            'order_id' : i.id,
            'finish_time' : localtime(i.finish_time).strftime(DATE_TIME_FORMAT),
            'buyer_tele' : i.buyer.tele,
            'destination' : i.destination
        })

    return JsonResponse({
        'status' : 0,
        'orders' : orders
    })

@check_token(Identity.STAFF)
def get_delivery_order(request):
    token = get_token(request)
    message = token2msg(token)
    id = message['id']

    #   order的user_id==id 且status == 2
    order_list = Order.objects.filter(staff_id=id,status=2)
    orders = []
    for i in order_list:
        orders.append({
            'order_id' : i.id,
            'expected_finish_time' : localtime(i.expected_finish_time).strftime(DATE_TIME_FORMAT),
            'destination' : i.destination,
            'buyer_tele' : i.buyer.tele
        })

    return JsonResponse({
        'status' : 0,
        'orders' : orders
    })

@check_token(Identity.BUYER)
def finish_order(request):
    token = get_token(request)
    message = token2msg(token)

    data = json.loads(request.body)
    order_id = data['order_id']
    try:
        order = Order.objects.get(id=order_id)
    except:
        return JsonResponse({
            'status' : 2,
            'msg' : '订单不存在'
        })
    if order.status != 2:
        return JsonResponse({
            'status' : 1
        })

    order.status=3
    order.save()

    return JsonResponse({
        'status' : 0
    })

# 评论系统 传id 查看评论

#   buyer功能
@check_token(Identity.BUYER)
def comment_on_canteen(request):
    token = get_token(request)
    message = token2msg(token)
    id = message['id']
    data = json.loads(request.body)
    canteen_id = data['canteen_id']
    content = data['content']
    comment = Comment(content=content,user_id=id)
    comment.save()

    comment_canteen = CommentCanteen(comment_id=comment.id,canteen_id =canteen_id)
    comment_canteen.save()
    return JsonResponse({
        'status' : 0
    })

@check_token(Identity.BUYER)
def comment_on_dish(request):
    token = get_token(request)
    message = token2msg(token)
    id = message['id']
    data = json.loads(request.body)

    dish_id = data['dish_id']
    content = data['content']
    #   order_dish 用buyer_id查所有

    comment = Comment(content=content, user_id=id)
    comment.save()
    comment_dish = CommentDish(comment_id=comment.id,dish_id=dish_id)
    comment_dish.save()
    return JsonResponse({
        'status' : 0
    })

@check_token(Identity.BUYER)
def comment_on_order(request):
    token = get_token(request)
    message = token2msg(token)
    id = message['id']
    data = json.loads(request.body)

    order_id = data['order_id']
    content = data['content']

    comment = Comment(content=content, user_id=id)
    comment.save()
    comment_order = CommentOrder(comment_id=comment.id, order_id=order_id)
    comment_order.save()
    return JsonResponse({
        'status': 0
    })

@check_token(Identity.BUYER)
def comment_on_comment(request):
    token = get_token(request)
    message = token2msg(token)
    id = message['id']
    data = json.loads(request.body)

    comment_id = data['comment_id']
    content = data['content']

    comment = Comment(content=content, user_id=id)
    comment.save()
    comment_comment = CommentComment(comment_id=comment.id, comment2_id=comment_id)

    comment_comment.save()
    return JsonResponse({
        'status': 0
    })

@check_token(Identity.BUYER)
def comment_on_staff(request):
    token = get_token(request)
    message = token2msg(token)
    id = message['id']
    data = json.loads(request.body)

    staff_id = data['staff_id']
    content = data['content']

    comment = Comment(content=content, user_id=id)
    comment.save()
    comment_staff = CommentStaff(comment_id=comment.id, staff_id=staff_id)

    comment_staff.save()
    return JsonResponse({
        'status': 0
    })


@check_token(Identity.BUYER)
def get_canteen_comments(request):
    token = get_token(request)
    message = token2msg(token)

    data = json.loads(request.body)

    canteen_id = data['canteen_id']
    # 连表查询 查出评论id 把id对应评论挑出来
    comment_id_list = CommentCanteen.objects.filter(canteen_id=canteen_id).values_list('comment_id',flat=True)
    comments = []
    for comment_id in comment_id_list:
        comment = Comment.objects.get(id=comment_id)
        comments.append({
            'comment_id' : comment_id,
            'nick_name' : comment.user.nick_name,
            'img' : comment.user.img.img,
            'content' : comment.content,
            'create_time' : localtime(comment.create_time).strftime(DATE_TIME_FORMAT),
        })

    return JsonResponse({
        'status' : 0,
        'comments' : comments
    },json_dumps_params={'ensure_ascii': False})

@check_token(Identity.BUYER,Identity.CANTEEN)
def get_dish_comments(request):
    token = get_token(request)
    message = token2msg(token)
    id = message['id']
    data = json.loads(request.body)

    dish_id = data['dish_id']
    comment_id_list = CommentDish.objects.filter(dish_id=dish_id).values_list('comment_id', flat=True)
    comments = []
    for comment_id in comment_id_list:
        comment = Comment.objects.get(id=comment_id)
        comments.append({
            'comment_id' : comment_id,
            'nick_name': comment.user.nick_name,
            'img': comment.user.img.img,
            'content' : comment.content,
            'create_time' : localtime(comment.create_time).strftime(DATE_TIME_FORMAT),
        })

    return JsonResponse({
        'status' : 0,
        'comments' : comments
    },json_dumps_params={'ensure_ascii': False})

@check_token(Identity.BUYER)
def get_comment_comments(request):
    token = get_token(request)
    message = token2msg(token)
    id = message['id']
    data = json.loads(request.body)

    comment_id = data['comment_id']
    comment_id_list = CommentComment.objects.filter(comment2_id=comment_id).values_list('comment_id', flat=True)
    comments = []
    for comment_id in comment_id_list:
        comment = Comment.objects.get(id=comment_id)
        comments.append({
            'comment_id': comment.id,
            'nick_name': comment.user.nick_name,
            'img': comment.user.img.img,
            'content': comment.content,
            'create_time': localtime(comment.create_time).strftime(DATE_TIME_FORMAT),
        })

    return JsonResponse({
        'status': 0,
        'comments': comments
    },json_dumps_params={'ensure_ascii': False})

@check_token(Identity.BUYER)
def get_history_comment(request):
    token = get_token(request)
    message = token2msg(token)
    id = message['id']


    comment_list = Comment.objects.filter(user_id=id)
    comments = []
    for i in comment_list:
        comments.append({
            'comment_id' : i.id,
            'content' : i.content,
            'create_time' : localtime(i.create_time).strftime(DATE_TIME_FORMAT)
        })

    return JsonResponse({
        'status' : 0,
        'comments' : comments
    },json_dumps_params={'ensure_ascii': False})

@check_token(Identity.BUYER)
def get_reply(request):
    token = get_token(request)
    message = token2msg(token)
    id = message['id']
    #   找到自己发表过的所有评论
    #   找到评论的评论
    self_comment_id_list = Comment.objects.filter(user_id=id).values_list('id',flat=True)
    reply_comment_id_list = CommentComment.objects.filter(comment2_id__in=self_comment_id_list).values_list('comment2_id',flat=True)
    comments = []
    for i in reply_comment_id_list:
        reply_comment = Comment.objects.get(id=i)
        comments.append({
            'comment_id' : i,
            'content' : reply_comment.content,
            'create_time' : reply_comment.create_time
        })

    return JsonResponse({
        'status' : 0,
        'comments' : comments
    },json_dumps_params={'ensure_ascii': False})


@check_token(Identity.STAFF)
def staff_get_comments(request):
    token = get_token(request)
    message = token2msg(token)
    id = message['id']

    comment_id_list = CommentStaff.objects.filter(staff_id=id).values_list('comment_id',flat=True)
    comments = []
    for i in comment_id_list:
        comment = Comment.objects.get(id=i)
        comments.append({
            'comment_id' : i,
            'content' : comment.content,
            'create_time' : localtime(comment.create_time).strftime(DATE_TIME_FORMAT)

        })

    return JsonResponse({
        'status' : 0,
        'comments' : comments
    },json_dumps_params={'ensure_ascii': False})

@check_token(Identity.CANTEEN)
def canteen_get_comments(request):
    token = get_token(request)
    message = token2msg(token)
    id = message['id']
    comment_id_list = CommentCanteen.objects.filter(canteen_id=id).values_list('comment_id', flat=True)
    comments = []
    for i in comment_id_list:
        comment = Comment.objects.get(id=i)
        comments.append({
            'comment_id': i,
            'content': comment.content,
            'create_time': localtime(comment.create_time).strftime(DATE_TIME_FORMAT)

        })

    return JsonResponse({
        'status': 0,
        'comments': comments
    })


#   食堂功能
@check_token(Identity.CANTEEN)
def add_dish(request):
    token = get_token(request)
    message = token2msg(token)
    if isinstance(message, int):
        return JsonResponse({'status': message})

    data = json.loads(request.body)
    id = message['id']
    identity = message['identity']
    if identity != Identity.CANTEEN:
        return JsonResponse({'status' : -3})
    canteen = Canteen.objects.get(id=id)
    if canteen is None:
        return JsonResponse({'status' : -4})
    pic = Image(img=data['img'])
    pic.save()
    name = data['name']
    price = data['price']
    description = data['description']
    dish = Dish(name=name,price=price,description=description,img_id=pic.id,canteen_id=id)
    dish.save()
    # 存tags
    tags = data['tags']
    print(tags)
    for i in tags:
        #   直接get
        try:
            tag = Tag.objects.get(content=i)
            tag_id = tag.id
        except:
            new_tag = Tag(content=i)
            new_tag.save()
            tag_id = new_tag.id

        tag_dish = TagDish(tag_id=tag_id,dish_id=dish.id)
        tag_dish.save()

    return JsonResponse({'status' : 0})


@check_token(Identity.CANTEEN)
def get_all_dishes(request):
    token = get_token(request)
    message = token2msg(token)
    if isinstance(message, int):
        return JsonResponse({'status': message})

    #   data = json.loads(request.body)
    id = message['id']
    identity = message['identity']
    if identity != Identity.CANTEEN:
        return JsonResponse({'status': -3})

    dish_list = []
    dishes = Dish.objects.filter(canteen_id=id)
    for i in dishes:
        dish_list.append({
            'id' : i.id,
            'name' : i.name,
            'price' : i.price,
            'description' : i.description,
            'available' : i.available,
            'img' : i.img.img
        })

    return JsonResponse({
        'status' : 0,
        'dishes' : dish_list
    },json_dumps_params={'ensure_ascii': False})
    #   返回一个list就可以 list里面存dict

@check_token(Identity.CANTEEN)
def change_dish(request):
    token = get_token(request)
    message = token2msg(token)
    if isinstance(message, int):
        return JsonResponse({'status': message})
    identity = message['identity']
    if identity != Identity.CANTEEN:
        return JsonResponse({'status': -3})

    data = json.loads(request.body)
    pic = Image(img=data['img'])
    pic.save()

    dish_id = data['id']
    try:
        dish = Dish.objects.get(id=dish_id)
    except:
        return JsonResponse({
            'status' : 1,
            'msg' : '菜品不存在'
        })
    dish.name = data['name']
    dish.price = data['price']
    dish.description = data['description']
    dish.available = data['available']
    dish.img_id = pic.id
    dish.save()
    return JsonResponse({'status' : 0})

# 收藏功能
@check_token(Identity.BUYER)
def favorite_dish(request):
    token = get_token(request)
    message = token2msg(token)

    data = json.loads(request.body)
    id = message['id']
    dish_id = data['dish_id']
    note = data['note']
    if Favorite.objects.filter(user_id=id,dish_id=dish_id).exists():
        return JsonResponse({
            'status' : 1 #  已经收藏过
        })

    f = Favorite(user_id=id,dish_id=dish_id,note=note)
    f.save()

    return JsonResponse({
        'status' : 0
    })

@check_token(Identity.BUYER)
def get_favorite(request):
    token = get_token(request)
    message = token2msg(token)
    id = message['id']

    dish_id_list = Favorite.objects.filter(user_id=id).values_list('dish_id',flat=True)
    dishes = []
    for i in dish_id_list:
        dish = Dish.objects.get(id=i)
        img = dish.img.img
        dishes.append({
            'dish_id' : i,
            'name' : dish.name,
            'img' : img,
            'description' : dish.description,
            'price' : dish.price
        })

    return JsonResponse({
        'status' : 0,
        'dishes' : dishes
    },json_dumps_params={'ensure_ascii': False})


#   管理员功能

@check_token(Identity.BUYER)
def get_all_comments(request):
    token = get_token(request)
    msg = token2msg(token)
    id = msg['id']
    if not Admin.objects.filter(user_id=id).exists():
        return JsonResponse({
            'status' : 1,
            'msg' : 'you are not permitted to access'
        })

    comments = Comment.objects.all()
    comment_list = []
    for i in comments:
        comment_list.append({
            'comment_id' : i.id,
            'content' : i.content
        })

    return JsonResponse({
        'status' : 0,
        'comments' : comment_list
    },json_dumps_params={'ensure_ascii': False})

@check_token(Identity.BUYER)
def delete_comment(request):
    token = get_token(request)
    msg = token2msg(token)
    id = msg['id']
    if not Admin.objects.filter(user_id=id).exists():
        return JsonResponse({
            'status': 1,
            'msg': 'you are not permitted to access'
        })

    data = json.loads(request.body)
    comment_id = data['comment_id']
    try:
        comment = Comment.objects.get(id=comment_id)
    except:
        return JsonResponse({
            'status' : 1,
            'msg':'评论不存在'
        })
    comment.delete()
    return JsonResponse({
        'status' : 0
    })

#   append
@check_token(Identity.BUYER)
def get_pic_nick(request):
    token = get_token(request)
    message = token2msg(token)

    id = message['id']
    try:
        buyer = Buyer.objects.get(id=id)
    except:
        return JsonResponse({
            'status' : 1
        })

    return JsonResponse({
        'status' : 0,
        'img' : buyer.img.img,
        'nick' : buyer.nick_name
    })

@check_token(Identity.STAFF,Identity.CANTEEN,Identity.BUYER)
def get_pic(request):
    token = get_token(request)
    message = token2msg(token)

    id = message['id']
    identity = message['identity']
    if identity is Identity.STAFF:
        try:
            staff = Staff.objects.get(id=id)
        except:
            return JsonResponse({
                'status': 1
            })

        return JsonResponse({
            'status' :0,
            'img' : staff.img.img
        })
    elif identity is Identity.BUYER:
        try:
            buyer = Buyer.objects.get(id=id)
        except:
            return JsonResponse({
                'status': 1
            })

        return JsonResponse({
            'status': 0,
            'img': buyer.img.img
        })
    else:
        try:
            canteen = Canteen.objects.get(id=id)
        except:
            return JsonResponse({
                'status': 1
            })

        return JsonResponse({
            'status': 0,
            'img': canteen.img.img
        })

@check_token(Identity.BUYER)
def delete_favorite(request):
    token = get_token(request)
    message = token2msg(token)

    id = message['id']
    data = json.loads(request.body)
    dish_id = data['dish_id']

    try:
        f = Favorite.objects.get(user_id=id,dish_id=dish_id)
    except:
        return JsonResponse({
            'status' : 1 #  之前未收藏过
        })
    #   前面校验一下 一个人只能收藏同种菜品一次
    f.delete()
    return JsonResponse({
        'status' : 0
    })

@check_token(Identity.BUYER)
def recommend_dishes(request):
    token = get_token(request)
    message = token2msg(token)

    id = message['id']

    #   初始化user_tags[i] 保存当前用户每个tag使用次数
    #   收藏算1次 购买该菜品的次数 * 2
    #   用tag_id直接当下标

    # tag_items 记录是否某个商品是否打过该标签
    # 对菜品来做循环 直接用菜品的id当键值 记录每个商品的score
    # 推荐最大的6个
    tag_time = {}
    dish_score = {}
    tag_id_list = Tag.objects.all().values_list('id',flat=True)
    #初始化每个tag使用次数
    for var in tag_id_list:
        tag_time[var] = 0

    dish_id_list = Dish.objects.all().values_list('id',flat=True)
    # 初始化每个dish的score
    for var in dish_id_list:
        dish_score[var] = 0

    favorite_dish_id_list = Favorite.objects.filter(user_id=id).values_list('dish_id',flat=True)
    # 得到收藏dish_id 当前user计算每个tag的使用次数
    for var in favorite_dish_id_list:
        dish_tag_id_list = TagDish.objects.filter(dish_id=var).values_list('tag_id',flat=True)
        # dish对应的所有tag的id
        for tag_id in dish_tag_id_list:
            tag_time[tag_id] = tag_time[tag_id] + 1

    for var in dish_id_list:
        #   首先该菜品的tag_id
        dish_tag_id_list = TagDish.objects.filter(dish_id=var).values_list('tag_id',flat=True)
        for tag_id in dish_tag_id_list:
            dish_score[var] = dish_score[var] + tag_time[tag_id]

    dish_score_list = []
    for key,value in dish_score.items():
        dish_score_list.append((value,key))

    sort_by_score = sorted(dish_score_list)

    dish_list = []

    cnt = 0
    for var in sort_by_score:
        if cnt == 6:
            break
        dish_id = var[1]
        #第二个元素，即key，即dish_id
        dish = Dish.objects.get(id=dish_id)
        dish_list.append({
            'dish_id' : dish_id,
            'description' : dish.description,
            'name' : dish.name,
            'price' : dish.price,
            'img' : dish.img.img
        })
        cnt = cnt + 1

    return JsonResponse({
        'status' : 0,
        'dish_list' : dish_list
    })

@check_token(Identity.BUYER,Identity.STAFF)
def get_order_info(request):
    data = json.loads(request.body)
    order_id = data['order_id']
    #   返回订单信息，和订单内菜品信息
    try:
        order = Order.objects.get(id=order_id)
    except:
        return JsonResponse({
            'status' : 1,
            'msg' : '订单不存在'
        },json_dumps_params={'ensure_ascii': False})

    total_price = Decimal("0")
    dish_list = OrderDish.objects.filter(order_id=order_id).values('dish_id', 'num')
    dishes = []
    for j in dish_list:
        dish = Dish.objects.get(id=j['dish_id'])
        total_price += dish.price * j['num']
        dishes.append({
            'name' : dish.name,
            'num' : j['num'],
            'description' : dish.description,
            'img' : dish.img.img,
            'price' : dish.price
        })

    '''
    destination = '',
    staff_name = '',
    staff_tele = ''
    if order.status == 1:
        destination = order.destination,
    else:
        destination = order.destination,
        staff_name = order.staff.real_name,
        staff_tele = order.staff.tele
    #   后三项直接为空
    '''
    return JsonResponse({
        'status' : 0,
        'total_price' : total_price,
        'dishes' : dishes,
        'destination' : order.destination,
    },json_dumps_params={'ensure_ascii': False})

def get_order_info_(order_id:int):
    order = Order.objects.get(id=order_id)
    total_price = Decimal("0")
    dish_list = OrderDish.objects.filter(order_id=order_id).values('dish_id', 'num')
    dishes = []
    for j in dish_list:
        dish = Dish.objects.get(id=j['dish_id'])
        total_price += dish.price * j['num']
        dishes.append({
            'name' : dish.name,
            'num' : j['num'],
            'img' : dish.img.img,
            'price' : dish.price
        })
    return [dishes,total_price]

@check_token(Identity.BUYER)
def judge_favorite(request):
    token = get_token(request)
    message = token2msg(token)
    id = message['id']
    data = json.loads(request.body)

    dish_id = data['dish_id']

    if Favorite.objects.filter(user_id=id,dish_id=dish_id).exists():
        return JsonResponse({
            'status' : 0,
            'exist' : True
        })

    return JsonResponse({
        'status': 0,
        'exist': False
    })

@check_token(Identity.CANTEEN)
def get_canteen_info(request):
    '''
    "tele" : 119,
"password" : "123456",
"again" : "123456",
"img" : "",
"description" : "好吃",
"location" : "新北",
    '''

    token = get_token(request)
    msg = token2msg(token)
    id = msg['id']
    canteen = Canteen.objects.get(id=id)
    return JsonResponse({
        'status' : 0,
        'tele' : canteen.tele,
        'img' : canteen.img.img,
        'description' : canteen.description,
        'location' : canteen.location
    })

@check_token(Identity.STAFF)
def get_staff_info(request):
    token = get_token(request)
    msg = token2msg(token)
    id = msg['id']
    #   canteen = Canteen.objects.get(id=id)
    staff = Staff.objects.get(id=id)
    return JsonResponse({
        'status': 0,
        'tele' : staff.tele,
        'real_name' : staff.real_name,
        'img': staff.img.img
    })

