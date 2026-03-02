from order.models import OrderItem , OrderStatus
from django.http import HttpResponse
import csv



def generate_csv_report_sales(vendor, start_date, end_date):
    queryset = (
        OrderItem.objects
        .filter(
            product__vendor=vendor,
            created_at__range=(start_date, end_date),
            order__status=OrderStatus.PAID,
        )
        .select_related('product', 'order', 'order__customer')
    )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'full_name',
        'phone_number',
        'email',
        'product_name',
        'quantity',
        'total_price',
        'date',
    ])

    for item in queryset.iterator():
        writer.writerow([
            item.order.customer.full_name,
            item.order.customer.phone_number,
            item.order.customer.email,
            item.product.name,
            item.quantity,
            item.total_price,
            item.created_at.date(),
        ])

    return response
