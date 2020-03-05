from django.shortcuts import render

# Create your views here.


def post_list(request):
    return render(request, 'garage/main.html', {})


def algo(request):
    return render(request, 'garage/algo.html', {})





