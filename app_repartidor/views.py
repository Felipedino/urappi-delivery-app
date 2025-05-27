from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from urappiapp.models import Order
from urappiapp.serializers import *
from django.views.decorators.http import require_POST , require_GET


def repartidor_perfil(request):
    orders = Order.objects.filter(status = 1)
    ##usuario = 

    pending_orders = [OrderSerializer.to_json(order) for order in orders]
    
    context = {
        'pending_orders': pending_orders
    }
    


    return render(request, 'app_repartidor/deliverer.html', context)

@require_POST
def accepted_order(request):
    id = request.POST.get('order_id')
    if id:
        try:
            order_to_be_modified = get_object_or_404(Order, orderID =id)
            order_to_be_modified.status = 1
            order_to_be_modified.save()
            messages.success(request, f'Pedido aceptado con éxito')
            return redirect('deliverer')
        except :
            messages.error(request, f'Error al aceptar el pedido: {Exception}')
    else:
        messages.error(request, f'Error en ID pedido')
    return redirect('order_selected')



def order_details(request,order_id):
    
    

    selected_order = get_object_or_404(Order, orderID = order_id)
    order_items = selected_order.items.all() 

    product_list = []
    for item in order_items:
        product_list.append({
            "productName": item.product.productName, 
            "priceCLP": item.price,                   
            "description": item.product.description,  
            "imageURL": item.product.imageURL,       
            "quantity": item.quantity                 
        })

    info = {
        "orderID": selected_order.orderID,
        "status": selected_order.status,
        "customer": selected_order.customer.apodo if selected_order.customer.apodo else selected_order.customer.username, 
        "location": selected_order.deliveryLocation, 
        "time": selected_order.createdAt.strftime("%H:%M"), 
        "createdAt": selected_order.createdAt.strftime("%Y-%m-%d"),
        "product_list": product_list, 
        "bill": f"{sum(item.price * item.quantity for item in order_items)}CLP",
        "shop":  selected_order.shop.shopName
    }

    
        
         
    return render(request, 'app_repartidor/order_selected.html', info) 
