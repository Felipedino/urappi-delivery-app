from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from urappiapp.models import Order, Deliverer , Delivery
from django.views.decorators.http import require_POST , require_GET


def repartidor_perfil(request):
    orders = Order.objects.filter(status = 1)
    
    ##usuario = 

    pending_orders =[
        {
            "orderID": "001",
            "customer": "Daniel Cáceres",
            "deliverAt": "B0120",
            "time": "11:00",
            "createdAt": "La Sonia",
            "bill" : "4000CLP",
            "imageURL":"svg/user1.webp"
            },
            {
            "orderID": "004",
            "customer": "Juan Pedro",
            "deliverAt": "Centro Modelamiento Matemático",
            "time": "15:00",
            "createdAt": "La Cafeta",
            "bill" : "8000CLP",
            "imageURL":"svg/user2.jpg"
            },
            {
            "orderID": "01234",
            "customer": "Javiera Gonzalez",
            "deliverAt": "Cancha -3",
            "time": "19:00",
            "createdAt": "La Cafeta",
            "bill" : "2000CLP",
            "imageURL":"svg/user3.jpg"
            },

            ]
    context = {
        'pending_orders': pending_orders
    }
    


    return render(request, 'deliverer.html', context)

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



@require_GET
def order_details(request):
    
    productos=[ {
            "ProductName": "Chocolate Trencito",
            "priceCLP": 3000,
            "description": "Barra de chocolate de leche",
            "imageURL":"svg/trencito.avif"
        },
        {
            "ProductName": "Café Capuccino",
            "priceCLP": 3500,
            "description": "Café de maquina Marley",
            "imageURL":"svg/capuccino.jpg"

            
            }
        
        ]
    

    #selected_order = get_object_or_404(Order, orderID = order_id)

    #info = {
     #   'customer': selected_order.customer_name,
       # 'orderID' :selected_order.orderID,
        #'product_list': productos,
        #'deliverAt': selected_order.deliveredAt,
        # "time" : 19:00,
        #"createdAt" : selected_order.createdAt
        #"Status": selected_order.status,
        #"bill" : "500CLP"
        #}

    info ={
        "orderID":"001",
            "Status": "Disponible",
            "customer": "Javiera Gonzalez",
            "deliverAt": "Cancha -3",
            "time": "19:00",
            "createdAt": "La Cafeta",
            "product_list":productos,
            "bill": "500CLP"
            }
        
        
         
    return render(request, 'order_selected.html', info) 
