from datetime import date

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator

from urappiapp.models import Order
from urappiapp.serializers import *

from urappiapp.util import NotificationBroker

## Renderizamos páginas para repartidores, con órdenes pendientes
def repartidor_perfil(request):
    orders = Order.objects.filter(status=1)
    ordersPerPage = 7
    paginator = Paginator(orders, ordersPerPage)
    #Desplegar las ordenes pendientes
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    pending_orders = [OrderSerializer.to_json(order) for order in page_obj]

    context = {
        "usuario": request.user,
        "pending_orders": pending_orders,
        "page_obj": page_obj}

    return render(request, "app_repartidor/deliverer.html", context)

##Lógica para aceptar una orden, cambiar su estatus y redireccionar a html de detalles.

@require_POST
def accepted_order(request):
    order_id = request.POST.get("order_id")
    action = request.POST.get("action")
    deliverer = request.user
    
    #manejar error de id inválida
    if not order_id:
        messages.error(request, "Error: ID de pedido no encontrado")
        return redirect("app_repartidor:repartidor_perfil")
    
    #manejar error sin acción generada (buttons)
    if not action:
        messages.error(request, "Error: Acción no especificada")
        return redirect("app_repartidor:repartidor_perfil")
    
    try:
        #Lógica para modificar la orden según acción
        order_to_be_modified = get_object_or_404(Order, id=order_id)    
        #Si se acepta, cambiar estatus del pedido     
        if action == "accept":
            order_to_be_modified.status = 2  # Estado aceptado
            order_to_be_modified.save()
            messages.success(request, "Pedido aceptado con éxito")

            # send notification
            user = order_to_be_modified.customer
            NotificationBroker.notificateAcceptedOrder(order_to_be_modified, deliverer, user)

            return redirect('app_repartidor:estado_order', order_id=order_id)
        
        #Si se rechaza, mantener estatus del pedido     
        elif action == "reject":
            order_to_be_modified.status = 1
            order_to_be_modified.save()
            messages.success(request, "Pedido rechazado")
            return redirect("app_repartidor:repartidor_perfil")
            
        else:
            messages.error(request, f"Acción no válida: {action}")
            return redirect("app_repartidor:repartidor_perfil")
            
    except Exception as e:
        messages.error(request, f"Error al procesar el pedido: {str(e)}")
    
    return redirect("app_repartidor:repartidor_perfil")

##Renderizar una página con más detalles sobre las órdenes pendientes
def order_details(request, order_id):
    ##lógica de búsqueda con order id

    selected_order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order__id=order_id)
    #Producto elegidos por el cliente
    product_list = [
        {
            "productName": item.product.productName,
            "priceCLP": item.price,
            "description": item.product.description,
            "prodImage": item.product.prodImage,
            "quantity": item.quantity,
        }
        for item in order_items
    ]
    #información a desplegar en la vista de detalles de orden

    info = {
        "usuario": request.user,
        "orderID": selected_order.id,
        "status": selected_order.status,
        "customer": (
            selected_order.customer.apodo
            if selected_order.customer.apodo
            else selected_order.customer.username
        ),
        "location": selected_order.deliveryLocation,
        "time": selected_order.createdAt.strftime("%H:%M"),
        "createdAt": selected_order.createdAt.strftime("%Y-%m-%d"),
        "product_list": product_list,
        "bill": f"{sum(item.price * item.quantity for item in order_items)}CLP",
        "shop": selected_order.shop.shopName,
    }

    return render(request, "app_repartidor/order_selected.html", info)

# Renderizar página de resumen de la orden para el repartidor
def estado_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # 
    context = {
        "usuario": request.user,
        'order': order
        }
    return render(request, 'app_repartidor/estado_order.html', context)

#Lógica de  entrega de pedido por el repartidor
@require_POST
def delivery_action(request):
    order_id = request.POST.get("order_id")
    print("ID recibido :", order_id)
    action = request.POST.get("action")
    #Manejar errores de id y acción por parte del repartidor
    if not order_id or not action:
        messages.error(request, "Error: Datos incompletos")
        return redirect("app_repartidor:repartidor_perfil")
    
    try:
        #Lógica para modificar la orden según acción del repartidor.
        order = get_object_or_404(Order, id=order_id)
        
        #Si entrega, estatus del pedido será Entregado(3)
        if action == "accept":
            order.status = 3  # Estado entregado
            order.save()
            messages.success(request, "Pedido marcado como entregado")
        
        
        #Si no entrega, estatus del pedido vuelve a pendiente, podría haber cola de prioridad.
    
        elif action == "reject":
            order.status = 1  # Estado en espera
            order.save()
            messages.success(request, "Entrega cancelada")
            
        return redirect("app_repartidor:repartidor_perfil")
        
    except Exception as e:
        messages.error(request, f"Error al procesar la acción: {str(e)}")
        return redirect("app_repartidor:repartidor_perfil")