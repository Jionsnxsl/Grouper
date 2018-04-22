from django.shortcuts import render, HttpResponse

# Create your views here.


def homepage(request):
    return render(request, "homepage.html")


def search_view(request):
    fish_batch = request.GET.get("fish_batch")
    result = {"fish_batch": fish_batch}
    return render(request, "search_result.html", result)

def adminView(request):
    return render(request, "fishes/fish_admin.html")

def ProductInfoView(request):
    print("call product info view ", request.META.get("HTTP_X_PJAX", None))
    # import time
    # time.sleep(3)
    return render(request, "fishes/productinfo.html")
