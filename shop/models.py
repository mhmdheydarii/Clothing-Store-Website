from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

# Create your models here.
class CategoryModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, unique=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-created_date"]


class ProductModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, unique=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    discount_percent = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    description = models.TextField()
    brief_description = models.TextField()
    category = models.ForeignKey(CategoryModel, on_delete=models.PROTECT, related_name="category_products")
    avg_rate = models.FloatField(default=0.0)

    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-created_date"]
    
    def get_price(self):
        discount_amount = (self.price * Decimal(self.discount_percent)) / Decimal(100)
        discounted_price = self.price - discount_amount
        return int(discounted_price)

    def get_colors(self):
        return ColorProductModel.objects.filter(
            color_products__product=self
        ).distinct()



class SizeProductModel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class ColorProductModel(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class ImagesProductModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="product/images")
    is_main = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name


class ProductVariant(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="product_variants")
    size = models.ForeignKey(SizeProductModel, on_delete=models.PROTECT, related_name="size_products")
    color = models.ForeignKey(ColorProductModel, on_delete=models.PROTECT, related_name="color_products")
    stock = models.PositiveIntegerField(default=1)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} + {self.size.name} + {self.color.name}"
    
    class Meta:
        ordering = ["-created_date"]