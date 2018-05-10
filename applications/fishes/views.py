from django.shortcuts import render, HttpResponse, get_object_or_404
import time, json
from applications.users import models
from .models import FishPool
from django.db.models import Q
from django.views import View
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
    return render(request, "fishes/product_info.html")


def userInfoView(request):
    '''用户信息产看'''

    if request.GET.get('offset') is None:
        return render(request, "fishes/user_info.html")

    search = request.GET.get('search')
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    offset = request.GET.get('offset')
    limit = request.GET.get('limit')

    users = None
    if search is not None:
        users = models.GrouperUser.objects.filter(Q(username__contains=search) | Q(employeeID=search))
    else:
        users = models.GrouperUser.objects.all()

    if sort is not None:
        if order == 'asc':
            users = users.order_by('-' + sort)
        else:
            users = users.order_by(sort)

    total = users.count()

    data = []
    for user in users:
        if not user.is_active:
            continue
        last_login = None
        if user.last_login is not None:
            last_login = user.last_login.strftime('%Y-%m-%d %H:%M:%S')
        temp = {
            'id': user.id,
            'username': user.username,
            'employeeID': user.employeeID,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'last_login':  last_login,
        }
        data.append(temp)

    result = {'total': total, 'rows': data[0+int(offset):0+int(offset)+int(limit)]}
    return HttpResponse(json.dumps(result))


def userDetailView(request, uid):
    '''用户详细信息'''
    user = models.GrouperUser.objects.filter(id=uid).first()
    result = {"id": user.id,
              "username": user.username,
              "employeeID": user.employeeID
              }
    return HttpResponse(json.dumps(result))


class AddUserView(View):
    """添加用户信息"""

    def get(self, request):
        return render(request, "fishes/add_user.html")

    def post(self, request):

        result = {"status": False, "message": '添加数据失败，请重试！'}
        employeeID = request.POST.get('val-employeeID')
        username = request.POST.get('val-username')
        password = request.POST.get('val-password')
        phonenum = request.POST.get('val-phonenum')

        is_manager = False
        if request.POST.get('val-is-manager') == '是':
            is_manager = True

        if models.GrouperUser.objects.filter(employeeID=employeeID).exists():
            result['message'] = '该员工号已经存在！'
        else:
            user = models.GrouperUser.objects.create_user(employeeID=employeeID,
                                                          username=username,
                                                          password=password,
                                                          is_superuser=is_manager,
                                                          phoneNum=phonenum)
            if user is not None:
                result['status'] = True
                result['message'] = '添加用户成功！'

        return HttpResponse(json.dumps(result))


def deleteUserView(request):
    '''删除用户'''
    employeeIDs = request.POST.getlist('employeeIDs')
    result = {'status': False, 'message': '删除失败，请重试！'}
    for employeeID in employeeIDs:
        user = get_object_or_404(models.GrouperUser, employeeID=employeeID)
        user.is_active = False
        user.save()
    result['status'] = True
    result['message'] = '删除成功！'
    return HttpResponse(json.dumps(result))



def fishPoolInfoView(request):
    '''产看鱼池信息'''
    if request.GET.get('offset') is None:
        return render(request, "fishes/fish_pool_info.html")

    search = request.GET.get('search')
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    offset = request.GET.get('offset')
    limit = request.GET.get('limit')

    fish_pools = None
    if search is not None and search.isdigit():
        fish_pools = FishPool.objects.filter(Q(num=search) | Q(fish_batch=search))
    else:
        fish_pools = FishPool.objects.all()

    if sort is not None:
        if order == 'asc':
            fish_pools = fish_pools.order_by('-' + sort)
        else:
            fish_pools = fish_pools.order_by(sort)

    total = fish_pools.count()

    data = []
    for fish_pool in fish_pools:
        temp = {
            'id': fish_pool.id,
            'num': fish_pool.num,
            'radius': fish_pool.radius,
            'depth': fish_pool.depth,
            'PH': fish_pool.PH,
            'temperature':  fish_pool.temperature,
            'fish_batch': fish_pool.fish_batch
        }
        data.append(temp)

    result = {'total': total, 'rows': data[0+int(offset):0+int(offset)+int(limit)]}
    return HttpResponse(json.dumps(result))


def fishPoolDetailView(request, pid):
    '''鱼池详细信息'''
    return HttpResponse("OK")


class AddFishPoolView(View):
    '''添加鱼池信息'''

    def get(self, request):
        fish_num_list = FishPool.objects.all().values('num')
        available_num = set(i for i in range(1, 100+1))
        using_num = set()
        for item in fish_num_list:
            using_num.add(item.get('num'))
        available_num = list(available_num - using_num)
        return render(request, "fishes/add_fish_pool.html", {"available_num": available_num})

    def post(self, request):
        result = {"status": False, "message": "添加数据失败，请重试！"}
        pool = {
            "num": request.POST.get("val-num"),
            "radius": request.POST.get("val-radius"),
            "depth": request.POST.get("val-depth"),
            "PH": request.POST.get("val-ph"),
            "temperature": request.POST.get("val-temperature")
        }

        pool_created = FishPool.objects.create(**pool)
        if pool_created is not None:
            result['status'] = True
            result['message'] = '添加鱼池成功！'

        return HttpResponse(json.dumps(result))


def deleteFishPool(request):
    '''删除鱼池'''
    pool_nums = request.POST.getlist('pool_nums')
    result = {'status': False, 'message': '删除失败，请重试！'}
    for pool_num in pool_nums:
        fish_pool = get_object_or_404(FishPool, num=int(pool_num))
        fish_pool.delete()
    result['status'] = True
    result['message'] = '删除成功！'
    return HttpResponse(json.dumps(result))


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