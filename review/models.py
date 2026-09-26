from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Avg

from accounts.models import User
from shop.models import ProductModel

# Create your models here.


class ReviewModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_review")
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="product_review")
    description = models.TextField()
    rate = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])

    class ReviewStatus(models.TextChoices):
        PENDING = "pending", "در انتظار تایید"
        ACCEPTED = "accepted", "تایید شده"
        REJECTED = "rejected", "رد شده"

    status = models.CharField(max_length=20, choices=ReviewStatus.choices, default=ReviewStatus.PENDING.value)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} {self.product.name}"

    class Meta:
        ordering = ["-created_date"]


@receiver(post_save, sender=ReviewModel)
def calculate_avrage_rate(sender, instance, created, **kwargs):

    if instance.status == ReviewModel.ReviewStatus.ACCEPTED.value:
        product = instance.product

        avrage_rating = ReviewModel.objects.filter(product=product,
                                                  status=ReviewModel.ReviewStatus.ACCEPTED.value
                                                  ).aggregate(Avg("rate"))["rate__avg"]

        product.avg_rate = round(avrage_rating,1)
        product.save()