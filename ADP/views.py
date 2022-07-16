from django.shortcuts import render
from cart.models import Cart




def home(request):
    session_id = Cart.objects.new_or_get(request)
    context = {'session_id': session_id}
    return render(request, 'home.html', context)