from . import views
from django.urls import path


urlpatterns = [
    # 登录相关
    path('buyerRegister',views.buyer_register),
    path('login',views.login),
    path('canteenRegister',views.canteen_register),
    path('staffRegister',views.staff_register),
    path('resetPassword',views.reset_password),
    path('resetPic',views.reset_picture),

    #   buyer功能
    path('getAllCanteens',views.get_all_canteens),
    path('getAvDishes',views.get_available_dishes),
    #   订单会不会买到不同食堂里?会
    path('buildOrder',views.build_order),
    path('addDishToOrder',views.add_dish_to_order),
    path('getCart',views.get_cart),

    path('changeDishInCart',views.change_dish_in_cart),
    path('submitOrder',views.submit_order),
    path('getBuyerHistoryOrders',views.get_buyer_history_orders),
    # 查看订单中详细菜品信息
    path('getNotTakenOrders',views.get_not_taken_orders),
    path('cancelOrder',views.cancel_order),

    # staff功能
    path('getOrders',views.get_orders),
    path('takeOrder',views.take_order),
    path('getStaffHistoryOrder',views.get_staff_history_order),
    path('getDeliveryOrder',views.get_delivery_order),# 这个没实现
    path('finishOrder',views.finish_order),

    #   食堂
    path('addDish',views.add_dish),
    path('getAllDishes',views.get_all_dishes),
    path('changeDish',views.change_dish),

    #   收藏系统
    path('favoriteDish',views.favorite_dish),
    path('getFavorite',views.get_favorite),

    #   Admin
    path('getAllComments',views.get_all_dishes),
    path('deleteComment',views.delete_comment),

    #   评论系统
    path('commentOnCanteen',views.comment_on_canteen),
    path('commentOnDish',views.comment_on_dish),
    path('commentOnStaff',views.comment_on_staff),
    path('commentOnOrder',views.comment_on_order),
    path('commentOnComment',views.comment_on_comment),
    path('getCanteenComments',views.get_canteen_comments),
    path('getDishComments',views.get_dish_comments),
    path('getCommentComments',views.get_comment_comments),
    path('getHistoryComment',views.get_history_comment),
    path('getReply',views.get_reply),
    path('staffGetComments',views.staff_get_comments),
    path('canteenGetComments',views.canteen_get_comments)
]