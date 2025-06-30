from urappiapp.models import *

class OrderSerializer:
    @staticmethod
    def to_json(order):
        return {
            "orderID": order.id,
            "customer": order.customer.apodo,
            "deliveredAt": order.deliveredAt,
            "createdAt": order.createdAt,
            "deliveryLocation": order.shop.location,
            "status": order.status,
            "shop": order.shop.shopName,
            "itemQuantity": sum(1 for item in order.items.all()),
            "total": sum(item.price * item.quantity for item in order.items.all()), # order.items pq related_name = items
            "imageURL":"svg/user1.webp",
            "product_list": [
                OrderItemSerializer.to_json(item) for item in order.items.all()
            ]
        }
    
class OrderItemSerializer:
    @staticmethod
    def to_json(item):
        return {
            "productName": item.product.productName,
            "description": item.product.description,
            "priceCLP": item.product.priceCLP,
            "prodImage": item.product.prodImage,
        }