from django.shortcuts import render, HttpResponse, get_object_or_404, Http404, HttpResponseRedirect
import time, json, random, datetime
from applications.users import models
from .models import FishPool, FishInfo, TransInfo, ProcessInfo
from django.db.models import Q
from django.views import View
from django.urls import reverse
from django.db import transaction
import qrcode
from django.utils.encoding import escape_uri_path
from django.contrib.auth.decorators import login_required
# Create your views here.


def homepage(request):
    """主页"""
    return render(request, "homepage.html")


def search_view(request):
    """搜索结果"""
    fish_batch = request.GET.get("fish_batch")
    result = {"fish_batch": fish_batch}
    return render(request, "search_result.html", result)


def adminView(request):
    """后台管理首页"""
    return render(request, "fishes/fish_admin.html")


def productInfoView(request):
    """产品信息查看"""
    print("call product info view ", request.META.get("HTTP_X_PJAX", None))
    return render(request, "fishes/product_info.html")


class fishPoolView(View):
    """扫描鱼池二维码"""

    def get(self, request):
        result = {'status': False, 'message': '请扫描鱼池上的二维码进行操作！'}
        path = request.path_info.lstrip('/')
        url = request.build_absolute_uri()
        print(url)
        print(path)
        pid = request.GET.get('pid', None)
        try:
            pool_id = int(pid)
        except Exception:
            raise Http404("鱼池信息获取失败！")
        pool = get_object_or_404(FishPool, id=pool_id)

        if pool.in_using:
            # 鱼池中有鱼
            return render(request, 'fishes/verified_operation_mobile.html', {'pool_id': pool.id})
        else:
            # 鱼池中没有鱼
            now = datetime.datetime.now()
            ran_num = random.randint(1000, 10000)
            product_num = str(now.year)+str(now.month)+str(now.day)+str(ran_num)
            return render(request, 'fishes/add_product_mobile.html', {'pool_id': pool_id, "product_num": product_num})

    def post(self, request):
        operation = request.POST.get('operation')
        if operation == 'tans':
            url = "{0}?pid={1}".format(reverse('fishes:tranproduct'), request.POST.get("pool_id"))
            return HttpResponseRedirect(url)
        elif operation == 'export':
            url = "{0}?pid={1}".format(reverse('fishes:processproduct'), request.POST.get("pool_id"))
            return HttpResponseRedirect(url)
        else:
            return Http404('请重试！')


def addProductView(request):
    """添加产品信息(入料)"""
    result = {"status": False, "message": '添加数据失败，请重试！'}
    fish_pool = FishPool.objects.filter(id=int(request.POST.get("val-poolID"))).first()
    data = {
        "pool_num_id": fish_pool.id,
        "fish_batch": request.POST.get("val-productNum"),
        "name": request.POST.get("val-typename"),
        "specification": request.POST.get("val-specification"),
        "number": int(request.POST.get("val-fishnum")),
        "total_mass": float(request.POST.get("val-totalmass")),
    }

    fish_info = FishInfo.objects.create(**data)

    if fish_info is not None:
        fish_pool.in_using = True
        fish_pool.save()
        result['status'] = True
        result['message'] = '添加数据成功。'
        return HttpResponse(json.dumps(result))
    else:
        return HttpResponse(json.dumps(result))


class TranProductView(View):
    """转移鱼池"""

    def get(self, request):
        pid = int(request.GET.get('pid'))
        avail_pool = FishPool.objects.filter(in_using=False).values('num').order_by('num')
        fish_pool = FishPool.objects.filter(id=pid).first()
        result = {
            'source_pool': fish_pool.num,
            'avail_pool': avail_pool,
        }
        return render(request, 'fishes/trans_product_mobile.html', result)


    def post(self, request):
        result = {'status': False, 'message': '转移失败，请重试！'}

        pnum = int(request.POST.get('val-sourcepool'))
        source_fish_pool = FishPool.objects.filter(num=pnum)

        target_pool_num = int(request.POST.get('val-targetpool'))
        target_fish_pool = FishPool.objects.filter(num=target_pool_num)

        # fish = fish_pool.fishinfo_set.all()
        # print(fish)
        # TODO 反向查询
        fishinfo_id = int(source_fish_pool.values('fishinfo__id')[0].get('fishinfo__id'))
        fish_info = FishInfo.objects.filter(id=fishinfo_id)

        data = {
            'source_pool_id': source_fish_pool.first().id,
            'target_pool_id': target_fish_pool.first().id,
            'fish_info_id': fishinfo_id,
        }

        try:
            # 将来源鱼池状态置为未使用
            # 将目的鱼池状态置为使用
            # 将鱼的存放位置改为目的鱼池
            with transaction.atomic():
                source_fish_pool.update(in_using=False)
                target_fish_pool.update(in_using=True)
                fish_info.update(pool_num_id=target_fish_pool.first().id)
                TransInfo.objects.create(**data)
        except Exception as e:
            return HttpResponse(json.dumps(result))

        result['status'] = True
        result['message'] = '转移成功。'
        return HttpResponse(json.dumps(result))


class ProcessProductView(View):
    """领料加工"""

    def get(self, reqeust):
        pool_id = int(reqeust.GET.get("pid"))
        fish_pool = FishPool.objects.get(id=pool_id)
        fish_info = fish_pool.fishinfo.all().first()

        result = {
            'pool_num': fish_pool.num,
            'fish_batch': fish_info.fish_batch
        }

        return render(reqeust, 'fishes/process_product_mobile.html', result)

    def post(self, reqeust):

        result = {'status': False, 'message': '领料失败，请重试！'}
        # 将鱼所在的鱼池置为空
        # 将鱼的信息表中鱼池置为空
        # 向加工表写入一条数据
        pool_num = int(reqeust.POST.get("pool_num"))
        fish_batch = int(reqeust.POST.get("fish_batch"))

        fish_pool = FishPool.objects.get(num=pool_num)
        fish_info = FishInfo.objects.get(fish_batch=fish_batch)

        try:
            with transaction.atomic():
                fish_pool.in_using = False
                fish_pool.save()

                fish_info.is_stocking = False
                fish_info.is_processing = True
                fish_info.save()

                ProcessInfo.objects.create(fish_info_id=fish_info.id)

        except Exception as e:
            return HttpResponse(json.dumps(result))

        result['status'] = True
        result['message'] = '领料成功，请及时处理！'
        return HttpResponse(json.dumps(result))

def userInfoView(request):
    """用户信息产看"""

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
    """用户详细信息"""
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
    """删除用户"""
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
    """查看鱼池信息"""
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
            'in_using': fish_pool.in_using
        }
        data.append(temp)

    result = {'total': total, 'rows': data[0+int(offset):0+int(offset)+int(limit)]}
    return HttpResponse(json.dumps(result))


def fishPoolQRCode(request, pid):
    """生成鱼池对应的二维码"""
    from django.utils.six import BytesIO
    url = "http://" + request.get_host() + reverse("fishes:fishpool")+"?pid="+pid
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()
    file = "鱼池" + pid + "号的二维码" + ".png"
    response = HttpResponse(image_stream)
    response['Content-Type'] = 'application/image'
    response['Content-Disposition'] = "attachment; filename*=utf-8''{0}".format(escape_uri_path(file))
    # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file)
    return response



class AddFishPoolView(View):
    """添加鱼池信息"""

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
    """删除鱼池"""
    pool_nums = request.POST.getlist('pool_nums')
    result = {'status': False, 'message': '删除失败，请重试！'}
    for pool_num in pool_nums:
        fish_pool = get_object_or_404(FishPool, num=int(pool_num))
        fish_pool.delete()
    result['status'] = True
    result['message'] = '删除成功！'
    return HttpResponse(json.dumps(result))


def generateERCodeView(request):
    """生成产品二维码"""
    time.sleep(1)
    return render(request, "fishes/generate_ERcode.html")


def thirdPartTestReportView(request):
    """第三方检测报告管理"""
    time.sleep(1)
    return render(request, "fishes/third_part_test_report.html")

def feedbackNOTReplyView(request):
    """未回复反馈"""
    return render(request, "fishes/feedback_not_reply.html")


def feedbackReplyView(request):
    """已回复反馈"""
    return render(request, "fishes/feedback_reply.html")


def sysSetForHomepageView(request):
    """网站首页内容设置"""
    return render(request, "fishes/sysset_for_homepage.html")


def sysSetForSearchResultView(request):
    """搜索结果页面设置"""
    return render(request, "fishes/sysset_for_serach_result.html")