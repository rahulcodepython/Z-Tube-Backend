from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
import uuid

User = get_user_model()


class Category(models.Model):
    key = models.CharField(max_length=255, unique=True, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]


class SubCategory(models.Model):
    key = models.CharField(max_length=255, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"
        ordering = ["name"]


class Review(models.Model):
    id = models.CharField(max_length=1000, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ratings = models.IntegerField(default=0, choices=((i, i) for i in range(0, 6)))
    massege = models.TextField()

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs) -> None:
        self.id = self.id if self.id else f"review+{uuid.uuid4()}"
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["-ratings"]


class Product(models.Model):
    id = models.CharField(max_length=1000, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(default=0)
    offer = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="product_category"
    )
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, related_name="product_subcategory"
    )
    images = ArrayField(
        models.CharField(max_length=100),
        size=4,
        blank=True,
        default=list,
        editable=True,
    )
    quanity = models.IntegerField(default=0)
    total_reviewer = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    five_star = models.IntegerField(default=0)
    four_star = models.IntegerField(default=0)
    three_star = models.IntegerField(default=0)
    two_star = models.IntegerField(default=0)
    one_star = models.IntegerField(default=0)
    availibility = models.CharField(
        max_length=100, choices=models.TextChoices("Availibility", "instock outofstock")
    )
    reviews = models.ManyToManyField(
        "Review", related_name="product_reviews", blank=True
    )

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs) -> None:
        self.id = self.id if self.id else f"poduct+{uuid.uuid4()}"
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Wishlist(models.Model):
    id = models.CharField(max_length=1000, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs) -> None:
        self.id = self.id if self.id else f"wishlist+{uuid.uuid4()}"
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"


class CartItem(models.Model):
    id = models.CharField(max_length=1000, primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs) -> None:
        self.id = self.id if self.id else f"cartitem+{uuid.uuid4()}"
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"


class Cart(models.Model):
    id = models.CharField(max_length=1000, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartItem)
    subtotal = models.IntegerField(default=0)
    tax = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    shipping = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs) -> None:
        self.id = self.id if self.id else f"cart+{uuid.uuid4()}"
        self.total = self.subtotal + self.tax + self.shipping - self.discount
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartItem)
    subtotal = models.IntegerField(default=0)
    date = models.CharField(max_length=500)
    payment = models.TextChoices("Payment", "CashOnDelivery Online")
    status = models.TextChoices("Status", "Pending Processing Shipped Delivered")
    payment_status = models.TextChoices("Payment Status", "Pending Paid")

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs) -> None:
        self.id = self.id if self.id else f"order+{uuid.uuid4()}"
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
