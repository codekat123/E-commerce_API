from celery import shared_task
from inventory.models import Product
from ..models import Notification , NotificationAudience

@shared_task(bind=True, max_retries=3,autoretry={'exc': Exception, 'countdown': 60})
def send_product_review_notification(self, product_id):
    try:
        product = Product.objects.get(pk=product_id)


        body = (
            f"New product added: {product.name}\n"
            f"Description: {product.description}\n"
            f"Price: ${product.price}\n"
            f"Available Stock: {product.quantity}\n"
            f"vendor: {product.vendor.full_name}\n"
            f"Category: {product.category.name}\n"
            f"Added on: {product.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )


        return Notification.objects.create(
            title=f"New Product: {product.name}",
            body=body,
            recipient=None,
            audience=NotificationAudience.MANAGEMENT,
        )
    except Product.DoesNotExist:
        self.retry(exc=Exception(f"Product with id {product_id} does not exist."))
    except Exception as e:
        self.retry(exc=e)