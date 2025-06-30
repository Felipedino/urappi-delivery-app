from urappiapp.models import *

# Methods to encapsulate notification logic
class NotificationBroker:

    # Creates a notification object in the database
    # and sends the notification to the user
    @staticmethod
    def notificateAcceptedOrder(order, deliverer, user):
        pass

    @staticmethod
    def notificateDeliveredOrder(order, deliverer, user):
        pass
    
    @staticmethod
    def notificateCanceledOrder(order, user):
        pass
