from django.shortcuts import render, redirect, get_object_or_404, messages
from urappiapp.models import Order, Deliverer , Delivery
from django.views.decorators.http import require_POST


def repartidor_perfil(request):
    pending_orders = Order.objects.filter(status = 1)
   
    return render(request, 'templates/deliverer.html', pending_orders)

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



@require_POST
def order_details(request, order_id):
    selected_order = get_object_or_404(Order, orderID =order_id)

    items_list = 0
    info = {
        'customer': selected_order.customer_name,
        'customerID': selected_order.customer_id,
        'orderID' :selected_order.orderID,
        'product_list': items_list,
        'deliverAt': selected_order.deliveredAt,

        }
    return render(request, 'templates/order_selected.html', info) 
