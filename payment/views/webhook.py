# from django.conf import settings

# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
#     endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

#     event = stripe.Webhook.construct_event(
#         payload, sig_header, endpoint_secret
#     )

#     if event["type"] == "checkout.session.completed":
#         session = event["data"]["object"]
#         order_id = session["metadata"]["order_id"]

#         Order.objects.filter(id=order_id).update(status="paid")

#     return HttpResponse(status=200)