import requests
from celery import shared_task
from django.conf import settings
from .models import Product, Offer


@shared_task
def update_offers():
    access_token = get_access_token()
    if not access_token:
        return
    products = Product.objects.all()
    for product in products:
        response = requests.get(
            f"{settings.OFFERS_MS_URL}/products/{product.id}/offers",
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )
        if response.status_code == 200:
            offers = response.json()
            for offer in offers:
                Offer.objects.update_or_create(
                    id=offer['id'],
                    defaults={
                        "product": product,
                        "price": offer['price'],
                        "items_in_stock": offer['items_in_stock']
                    }
                )


def get_access_token():
    response = requests.post(
        f"{settings.OFFERS_MS_URL}/auth"
    )
    if response.status_code == 201:
        return response.json().get("access_token")
    return None