from urappiapp.models import *

# Methods to encapsulate notification logic
class NotificationBroker:

    # Creates a notification object in the database
    # and sends the notification to the user
    @staticmethod
    def notificateAcceptedOrder(order, deliverer, user):
        notification = Notification(
            user=user,
            deliverer=deliverer,
            order=order,
            type="aceptado",
            status="unread",
            message=f"Tu pedido de {order.shop.shopName} ya ha sido aceptado por uno de nuestros repartidores."
        )
        notification.save()

    @staticmethod
    def notificateDeliveredOrder(order, deliverer, user):
        notification = Notification(
            user=user,
            deliverer=deliverer,
            order=order,
            type="entregado",
            status="unread",
            message=f"Tu pedido de {order.shop.shopName} ha sido entregado!."
        )
        notification.save()
    
    @staticmethod
    def notificateCanceledOrder(order, user):
        notification = Notification(
            user=user,
            order=order,
            type="cancelado",
            status="unread",
            message=f"Tu pedido de {order.shop.shopName} ha sido cancelado."
        )
        notification.save()
