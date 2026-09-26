from django import forms
from .models import ReviewModel
from shop.models import ProductModel

class SubmitReviewForm(forms.ModelForm):

    class Meta:
        model = ReviewModel
        fields = ["product", "description", "rate"]

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")

        try:
            ProductModel.objects.filter(id=product.id, status=True)
        except ProductModel.DoesNotExist:
            raise forms.ValidationError("محصول یافت نشد")
        return cleaned_data