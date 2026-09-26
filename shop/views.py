from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from django.core.exceptions import FieldError
from .models import ProductModel, ProductVariant, CategoryModel, SizeProductModel, ColorProductModel
from review.models import ReviewModel
# Create your views here.

class ProductsView(ListView):
    template_name = "shop/products.html"
    paginate_by = 9

    def get_queryset(self):
        queryset = ProductModel.objects.filter(status=True)
        if category := self.request.GET.get("category"):
            queryset = queryset.filter(category__name=category)
        if sort := self.request.GET.get("sort"):
            try:
                queryset = queryset.order_by(sort)
            except FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = CategoryModel.objects.all()
        return context
    

class ProductDetailView(DetailView):
    queryset = ProductModel.objects.filter(status=True)
    template_name = "shop/product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["review"] = ReviewModel.objects.filter(product=product, status=ReviewModel.ReviewStatus.ACCEPTED.value)
        context["sizes"] = SizeProductModel.objects.filter(size_products__product=product).distinct()
        context["colors"] = ColorProductModel.objects.filter(color_products__product=product).distinct()
        size = self.request.GET.get("size")
        color = self.request.GET.get("color")
        try:
            if size and color:
                context["variant"] = ProductVariant.objects.get(product__id=product.id, size__id=size, color__id=color)
            else:
                context["variant"] = None
        except ProductVariant.DoesNotExist:
            context["variant"] = None
        return context