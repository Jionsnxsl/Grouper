from django.shortcuts import render, HttpResponse

# Create your views here.


def homepage(request):
    '''主页'''
    return render(request, "homepage.html")


def search_view(request):
    '''搜索结果'''
    fish_batch = request.GET.get("fish_batch")
    result = {"fish_batch": fish_batch}
    return render(request, "search_result.html", result)


def adminView(request):
    '''后台管理首页'''
    return render(request, "fishes/fish_admin.html")


def productInfoView(request):
    '''产品信息查看'''
    print("call product info view ", request.META.get("HTTP_X_PJAX", None))
    # import time
    # time.sleep(3)
    return render(request, "fishes/product_info.html")


def userInfoView(request):
    return render(request, "fishes/user_info.html")


def addUserView(request):
    return render(request, "fishes/add_user.html")


def fishPoolInfoView(request):
    return render(request, "fishes/fish_pool_info.html")


def addFishPoolView(request):
    return render(request, "fishes/add_fish_pool.html")


def generateERCodeView(request):
    return render(request, "fishes/generate_ERcode.html")