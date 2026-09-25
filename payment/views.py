
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.db import transaction

from .models import PaymentModel
from .zarinpal import ZarinPalSandbox

from order.models import OrderModel
from shop.models import ProductVariant
from cart.models import CartModel
from cart.cart import CartSession


class PaymentVerifyView(View):

    def get(self, request, *args, **kwargs):

        authority_id = request.GET.get("Authority")
        status = request.GET.get("Status")

        if not authority_id:
            return render(request, "order/failed.html")

        payment_obj = get_object_or_404(
            PaymentModel,
            authority_id=authority_id
        )

        if payment_obj.status == PaymentModel.PaymentStatusType.PAID:
            return render(request, "order/success.html")

        order = get_object_or_404(
            OrderModel,
            payment=payment_obj
        )

        if status != "OK":

            with transaction.atomic():

                payment_obj = PaymentModel.objects.select_for_update().get(
                    id=payment_obj.id
                )

                order = OrderModel.objects.select_for_update().get(
                    id=order.id
                )

                if payment_obj.status == PaymentModel.PaymentStatusType.PAID:
                    return render(request, "order/success.html")

                payment_obj.status = (
                    PaymentModel.PaymentStatusType.CANCELED
                )

                payment_obj.save(
                    update_fields=["status"]
                )

                order.status = (
                    OrderModel.OrderStatusTypeModel.CANCELED
                )

                order.save(
                    update_fields=["status"]
                )

            return render(request, "order/failed.html")


        zarinpal = ZarinPalSandbox()

        response = zarinpal.payment_verify(
            int(payment_obj.amount),
            authority_id
        )

        data = response.get("data", {})
        response_code = data.get("code")

        if response_code != 100:

            with transaction.atomic():

                payment_obj = PaymentModel.objects.select_for_update().get(
                    id=payment_obj.id
                )

                order = OrderModel.objects.select_for_update().get(
                    id=order.id
                )

                if payment_obj.status == PaymentModel.PaymentStatusType.PAID:
                    return render(request, "order/success.html")

                payment_obj.ref_id = data.get("ref_id")
                payment_obj.response_code = response_code
                payment_obj.status = (
                    PaymentModel.PaymentStatusType.CANCELED
                )
                payment_obj.response_json = response

                payment_obj.save()

                order.status = (
                    OrderModel.OrderStatusTypeModel.CANCELED
                )

                order.save(
                    update_fields=["status"]
                )

            return render(request, "order/failed.html")


        try:

            with transaction.atomic():

                payment_obj = PaymentModel.objects.select_for_update().get(
                    id=payment_obj.id
                )

                if payment_obj.status == PaymentModel.PaymentStatusType.PAID:
                    return render(request, "order/success.html")

                order = OrderModel.objects.select_for_update().get(
                    id=order.id
                )


                for item in order.order_items.all():

                    product = (
                        ProductVariant.objects
                        .select_for_update()
                        .get(id=item.product_variant_id)
                    )

                    if product.stock < item.quantity:
                        raise ValueError(
                            "Not enough product stock."
                        )

                    product.stock -= item.quantity

                    product.save(
                        update_fields=["stock"]
                    )

                payment_obj.ref_id = data.get("ref_id")
                payment_obj.response_code = response_code
                payment_obj.status = (
                    PaymentModel.PaymentStatusType.PAID
                )
                payment_obj.response_json = response

                payment_obj.save()


                order.status = (
                    OrderModel.OrderStatusTypeModel.PAID
                )

                order.save(
                    update_fields=["status"]
                )

                if order.coupon:
                    order.coupon.used_by.add(order.user)


                cart = CartModel.objects.filter(
                    user=order.user
                ).first()

                if cart:
                    cart.cart_items.all().delete()

        except ValueError:
            return render(request, "order/failed.html")
        
        CartSession(request.session).clear()

        return render(request, "order/success.html")
