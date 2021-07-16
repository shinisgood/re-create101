from django.db import models


class User(models.Model):
    email = models.CharField(max_length=128)
    korean_name = models.CharField(max_length=64)
    password = models.CharField(max_length=64, default="")
    kakao_id = models.IntegerField(default=None, null=True)
    coupon = models.ManyToManyField("Coupon", through="UserCoupon")
    comment = models.ManyToManyField("Review", through="Comment")
    like = models.ManyToManyField("Course", through="Like")
    look = models.ManyToManyField("Course", through="Look")

    class Meta:
        db_table = "users"


class Coupon(models.Model):
    name = models.CharField(max_length=128)
    discount_rate = models.IntegerField()

    class Meta:
        db_table = "coupons"


class UserCoupon(models.Model):
    coupon = models.ForeignKey("Coupon", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    class Meta:
        db_table = "user_coupon"


class Comment(models.Model):
    review = models.ForeignKey("courses.Review", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    text = models.TextField(default=None)

    class Meta:
        db_table = "comments"


class Like(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    class Meta:
        db_table = "likes"


class Look(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    class Meta:
        db_table = "looks"


class Course(models.Model):
    target = models.ForeignKey("Target", on_delete=models.CASCADE)
    # 설명에 html 코드가 들어갑니다.
    description = models.TextField()
    # 이미지는 한장만 사용됩니다.
    thumbnail = models.FileField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.CharField(max_length=300)
    sub_category = models.ForeignKey("SubCategory", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    month = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    review = models.ManyToManyField("User")

    class Meta:
        db_table = "courses"


class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = "categories"


class SubCategory(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    class Meta:
        db_table = "sub_categories"


class Target(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = "targets"


class Review(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        db_table = "reviews"
