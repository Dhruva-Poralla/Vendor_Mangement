from .models import PurchaseOrder


def calculate_average_response_time(vendor):
    pos = PurchaseOrder.objects.filter(vendor=vendor)
    response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in pos]
    return sum(response_times) / len(response_times)

