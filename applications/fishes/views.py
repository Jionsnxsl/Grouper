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
    return render(request, "fishes/productinfo.html")


def userInfoView(request):
    return render(request, "fishes/userinfo.html")

def addUserView(request):
    return render(request, "fishes/adduser.html")
