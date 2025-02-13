from django.shortcuts import render
from datetime import datetime, timedelta
import random

def main(request):
    '''Show main page'''

    template_name = "formdata/main.html"
    return render(request, template_name)

def order(request):
    '''Show order page'''

    template_name = "formdata/order.html"

    menu_items = {
        'incredible hamburger': '9999',
        'incredible apple': '9999',
        'incredible mystery stew': '9999',
        'definetly not steak ': '9999',
        'super special water': '9999',
        'potentially harmful brew': '9999',
    }
    item = random.choice(list(menu_items.items()))

    context = {
        'daily_special' : item[0],
        'ds_price': item[1],
    }

    return render(request, template_name, context=context)


def confirmtion(request):
    '''Process the form submission and generate a result.'''

    template_name = "formdata/confirmation.html"

    if request.method == "POST":
        customer_name = request.POST.get("customer_name", "")
        customer_phone = request.POST.get("customer_phone", "")
        customer_email = request.POST.get("customer_email", "")
        special_instructions = request.POST.get("special_instructions", "")


        menu_prices = {
            "Pizza": 500.00,
            "Pizza with Greens": 2.50,
            "Coffee": 20.45,
            "Pancakes": 25.45,
            "400 Brews": 3.50
        }

        ordered_items = {}  
        total_price = 0.00  

        daily_special_name = request.POST.get("daily_special", "")
        if daily_special_name == 'on':
            ordered_items["Daily Special"] = f"${9999}"
            total_price += 9999

        # Logic to make sure you either get Pizza or Pizza with greens if selected, not two seperate items.
        if "pizza_greens" in request.POST:
            ordered_items["Pizza with Greens"] = f"${menu_prices['Pizza with Greens']:.2f}"
            total_price += menu_prices["Pizza"]
            total_price += menu_prices["Pizza with Greens"]
        elif 'pizza_greens' not in request.POST and 'pizza' in request.POST:
            ordered_items["Pizza"] = f"${menu_prices['Pizza']:.2f}"
            total_price += menu_prices["Pizza"]

        if "coffee" in request.POST:
            ordered_items["Coffee"] = f"${menu_prices['Coffee']:.2f}"
            total_price += menu_prices["Coffee"]

        if "pancakes" in request.POST:
            ordered_items["Pancakes"] = f"${menu_prices['Pancakes']:.2f}"
            total_price += menu_prices["Pancakes"]

        if "brews" in request.POST:
            ordered_items["400 Brews"] = f"${menu_prices['400 Brews']:.2f}"
            total_price += menu_prices["400 Brews"]

        random_wait_time = random.randint(30, 60)  
        order_ready_time = datetime.now() + timedelta(minutes=random_wait_time)
        formatted_time = order_ready_time.strftime("%I:%M %p").lstrip("0")  

        context = {
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "customer_email": customer_email,
            "special_instructions": special_instructions,
            "ordered_items": ordered_items,  
            "order_ready_time": formatted_time,  
            "total_price": f"${total_price:.2f}"  
        }

        return render(request, template_name, context=context)

    return render(request, template_name)
