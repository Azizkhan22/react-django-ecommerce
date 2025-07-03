import random
import string
import threading
from django.utils.dateformat import DateFormat
from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.utils import IntegrityError
from django.views.generic import ListView, DetailView, View

from django.db.models import Avg
from django.shortcuts import redirect
from django.urls import reverse

from django.contrib.sessions.models import Session
from django.utils import timezone
from datetime import timedelta

from .models import Item

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔄 Cache slides
        slides = cache.get('slides')
        if not slides:
            slides = Slide.objects.all()
            cache.set('slides', slides, 60 * 60)  # Cache for 1 hour
        context['slides'] = slides

        # 🔄 Cache categories
        categories = cache.get('categories')
        if not categories:
            categories = Category.objects.all().order_by('name')
            cache.set('categories', categories, 60 * 60)
        context['categories'] = categories

        # 🔄 Cache category items
        category_items = {}
        for category in categories:
            cached_items_key = f'category_items_{category.id}'
            items = cache.get(cached_items_key)
            if not items:
                items = Item.objects.filter(category=category, is_visible_on_homepage=True)[:4]
                cache.set(cached_items_key, items, 60 * 60)  # 1 hour
            category_items[category] = items
        context['category_items'] = category_items

        # 🔄 Cache best selling items
        best_selling = cache.get('best_selling')
        if not best_selling:
            best_selling = BestSelling.objects.all()[:4]
            cache.set('best_selling', best_selling, 60 * 60)
        context['best_selling'] = best_selling

        # 🔄 Cache bundles
        bundles = cache.get('bundles')
        if not bundles:
            bundles = Bundle.objects.all()[:4]
            cache.set('bundles', bundles, 60 * 60)
        context['bundles'] = bundles

        return context

def buy_now(request, slug):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            size = data.get('size')
            quantity = data.get('quantity')
            product = get_object_or_404(Item, slug=slug)

            if request.user.is_authenticated:
                user = request.user
                session = None  # No session key needed for logged-in users
            else:
                user = None
                session_key = request.session.session_key                
                if not session_key:
                    request.session.create()
                    session_key = request.session.session_key
                session, created = Session.objects.get_or_create(session_key=session_key)

            BuyNow.objects.filter(user=user, session=session).delete()

            # Create a new OrderItem
            order_item = OrderItem.objects.create(
                item=product,
                user=user if user else None,  # Only assign user if logged in                
                quantity=quantity,
                size=size
            )

            if not order_item.item.stock.get(order_item.size, 0) >= order_item.quantity:
                messages.warning(request,f"Max stock reached for {order_item.item.title} (Size: {order_item.size}), Lower the quantity")
                return redirect(request.META.get('HTTP_REFERER'))

            # Create a new BuyNow entry
            BuyNow.objects.create(user=user, session=session, order_item=order_item)

            return JsonResponse({
                "success": True,
                "redirect_url": "/buynow-checkout/"
            })
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data"}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

class OrderSummary(DetailView):
    model = Order
    template_name = "order-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
                
        order = self.get_object()
        context['items'] = order.items.all()
        context['order'] = order
        return context


    email = request.GET.get("email_address", "No email provided")    
    # Fetch Order and PaymentWay objects
    order = get_object_or_404(Order, id=order_id)
    payment_way = get_object_or_404(Payment, id=payment_way_id)
    cart = get_object_or_404(Cart, id = cart_id)

    # Extract payment details from GET parameters
    trans_id = request.GET.get("transaction_id")
    err_code = request.GET.get("err_code")
    err_msg = request.GET.get("err_msg")    

    # Verify transaction success
    if err_code not in ["000", "00"]:
        messages.error(request, f"Transaction Failed: {err_msg}")
        return redirect(reverse("core:payment-failed"))  # Redirect to failure page

    # Update payment details
    payment_way.amount = order.total_price
    payment_way.status = Payment.paymentstatus.ONLINE
    payment_way.transaction_id = trans_id
    payment_way.save()

    # Link payment to order
    order.payment = payment_way
    order.save()
    cart.delete()

    # Send confirmation emails asynchronously
    email_thread_1 = threading.Thread(target=EmailService.send_email, args=(order.name, order, email))
    email_thread_2 = threading.Thread(target=EmailService.send_email_admin, args=(order.name, order, "orders@elevenattire.com"))

    email_thread_1.start()
    email_thread_2.start()

    # Show success message and redirect to confirmation page
    messages.success(request, "Order Placed Successfully!")
    return redirect(reverse('core:order-summary', kwargs={'pk': order.id}))  