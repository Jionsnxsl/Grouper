from django.shortcuts import render, HttpResponse
import time
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
    time.sleep(2)
    return render(request, "fishes/product_info.html")


def userInfoView(request):
    '''用户信息产看'''
    time.sleep(1)
    return render(request, "fishes/user_info.html")


def addUserView(request):
    '''添加用户信息'''
    time.sleep(1)
    return render(request, "fishes/add_user.html")


def fishPoolInfoView(request):
    '''产看鱼池信息'''
    time.sleep(2)
    return render(request, "fishes/fish_pool_info.html")


def addFishPoolView(request):
    '''添加鱼池信息'''
    time.sleep(2)
    return render(request, "fishes/add_fish_pool.html")


def generateERCodeView(request):
    '''生成产品二维码'''
    time.sleep(1)
    return render(request, "fishes/generate_ERcode.html")


def thirdPartTestReportView(request):
    '''第三方检测报告管理'''
    time.sleep(1)
    return render(request, "fishes/third_part_test_report.html")

def feedbackNOTReplyView(request):
    '''未回复反馈'''
    return render(request, "fishes/feedback_not_reply.html")


def feedbackReplyView(request):
    '''已回复反馈'''
    return render(request, "fishes/feedback_reply.html")


def sysSetForHomepageView(request):
    '''网站首页内容设置'''
    return render(request, "fishes/sysset_for_homepage.html")


def sysSetForSearchResultView(request):
    '''搜索结果页面设置'''
    return render(request, "fishes/sysset_for_serach_result.html")