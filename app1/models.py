from django.db import models

# Create your models here.
class Image(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.TextField()

class User(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=128)
    tele = models.BigIntegerField(unique=True)
    img = models.ForeignKey(Image,on_delete=models.CASCADE)

    class Meta:
        abstract = True




class Buyer(User):
    nick_name = models.CharField(max_length=10)


class Staff(User):
    real_name = models.CharField(max_length=10)


class Canteen(User):
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=20)



class Dish(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    description = models.CharField(max_length=200)
    img = models.ForeignKey(Image,on_delete=models.CASCADE)
    canteen = models.ForeignKey(Canteen,on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

#   TODO:给用户查订单加一个额外的展示属性
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)   # 每次save都会更新
    expected_finish_time = models.DateTimeField(null=True)
    finish_time = models.DateTimeField(auto_now=True)
    # 要不要完成时间？
    status = models.IntegerField(default=0)
    #   status 0新建未submit 1submit未接单 2接单在配送 3配送完成
    staff = models.ForeignKey(Staff,on_delete=models.SET_NULL,null=True)    # 可以为空 只在status为2时有效
    destination = models.CharField(max_length=50)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=1000)
    create_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Buyer,on_delete=models.SET_NULL,null=True)


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=5)

class CommentAbstract(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)

    class Meta:
        abstract = True

class CommentStaff(CommentAbstract):
    #   id = models.AutoField(primary_key=True)
    #   comment_id = models.IntegerField()
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE)


class CommentOrder(CommentAbstract):
    #   id = models.AutoField(primary_key=True)
    #   comment_id = models.IntegerField()
    order = models.ForeignKey(Order,on_delete=models.CASCADE)


class CommentDish(CommentAbstract):
    #   id = models.AutoField(primary_key=True)
    #   comment_id = models.IntegerField()
    dish = models.ForeignKey(Dish,on_delete=models.CASCADE)


class CommentCanteen(CommentAbstract):
    #   id = models.AutoField(primary_key=True)
    #   comment_id = models.IntegerField()
    canteen = models.ForeignKey(Canteen,on_delete=models.CASCADE)


class CommentComment(CommentAbstract):
    #   id = models.AutoField(primary_key=True)
    #   comment1_id = models.IntegerField()
    comment2 = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='comment2_id')


class Favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish,on_delete=models.CASCADE)
    note = models.CharField(max_length=10)  # 收藏的note可能冗余了


class OrderDish(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish,on_delete=models.CASCADE)
    num = models.IntegerField()


class TagDish(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish,on_delete=models.CASCADE)





class Admin(models.Model):
    user_id = models.IntegerField()
    #不再增加admin identity