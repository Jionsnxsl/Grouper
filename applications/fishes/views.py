from django.shortcuts import render, HttpResponse, get_object_or_404, Http404, HttpResponseRedirect
import time, json, random, datetime
from applications.users import models
from .models import FishPool, FishInfo, TransInfo, ProcessInfo, ProductInfo, Variety
from django.db.models import Q
from django.views import View
from django.urls import reverse
from django.db import transaction
import qrcode
from django.utils.encoding import escape_uri_path
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import timedelta
from django.utils.six import BytesIO
import ast
from .utils import delete_image
from django.contrib.auth.decorators import login_required
# Create your views here.


def Homepage(request):
    """主页"""
    return render(request, "homepage.html")


def SearchView(request):
    """搜索结果"""
    # if request.GET.get("fish_batch"):
    #     fish_batch = request.GET.get("fish_batch")
    #     result = {"fish_batch": fish_batch}
    #     return render(request, "search_result.html", result)
    if request.GET.get("pid"):
        product_id = request.GET.get("pid")
        product_info_obj = ProductInfo.objects.filter(id=int(product_id)).first()
        fish_info_obj = product_info_obj.fish_info
        process_info_obj = product_info_obj.process_info

        product_info_data = {
            "product_id": product_id,
            "product_batch": product_info_obj.product_batch,
            "product_date": product_info_obj.product_date,
        }

        fish_info_data = {
            "fish_batch": fish_info_obj.fish_batch,
            "stock_date": fish_info_obj.stock_date,
            "number": fish_info_obj.number,
            "total_mass": fish_info_obj.total_mass,
            "name": fish_info_obj.name,
            "specification": fish_info_obj.specification,
            "test_report_stock": fish_info_obj.test_report_stock,
            "test_report_third": fish_info_obj.test_report_third,
            "stock_scene": fish_info_obj.stock_scene
        }

        trans_infos = fish_info_obj.transinfo.all()

        process_info_data = {
            "process_date": process_info_obj.process_date,
            "pack_environment": process_info_obj.pack_environment,
            "process_environment": process_info_obj.process_environment,
            "get_scene": process_info_obj.get_scene,
            "test_report_process": process_info_obj.test_report_process
        }

        data = {
            "product_info_data": product_info_data,
            "fish_info_data": fish_info_data,
            "trans_infos": trans_infos,
            "process_info_data": process_info_data,
            "is_product_detail": True
        }

        return render(request, "search_result.html", data)
        # return HttpResponse(json.dumps(result))


def AdminView(request):
    """后台管理首页"""
    return render(request, "fishes/fish_admin.html")


def ProductInfoView(request):
    """
    产品信息查看
    :param request: 
    :return: 
    """
    # print("call product info view ", request.META.get("HTTP_X_PJAX", None))
    # return render(request, "fishes/product_info.html")

    # 如果请求中没有“offset”说明是请求产品信息查看页面
    # 否则，是请求产品信息
    if request.GET.get('offset') is None:
        return render(request, "fishes/product_info.html")

    search = request.GET.get('search')
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    offset = request.GET.get('offset')
    limit = request.GET.get('limit')

    products = None
    if search is not None:
        products = ProductInfo.objects.filter(Q(product_batch__contains=search) | Q(product_date__contains=search)
                                              | Q(fish_info__fish_batch__contains=search))
    else:
        products = ProductInfo.objects.all()

    if sort is not None:
        if order == 'asc':
            products = products.order_by('-' + sort)
        else:
            products = products.order_by(sort)

    total = products.count()

    data = []
    for product in products:
        temp = {
            'id': product.id,
            'product_batch': product.product_batch,
            'fish_batch': product.fish_info.fish_batch,
            'product_date': product.product_date.strftime("%Y-%m-%d"),
        }
        data.append(temp)

    result = {'total': total, 'rows': data[0 + int(offset):0 + int(offset) + int(limit)]}
    return HttpResponse(json.dumps(result))


@method_decorator(csrf_exempt, name='dispatch')
class ProductDetailView(View):
    """产品信息详细"""

    def get(self, request):
        product_id = request.GET.get("pid")
        product_info_obj = ProductInfo.objects.filter(id=int(product_id)).first()
        fish_info_obj = product_info_obj.fish_info
        process_info_obj = product_info_obj.process_info

        product_info_data = {
            "product_id": product_id,
            "product_batch": product_info_obj.product_batch,
            "product_date": product_info_obj.product_date,
        }

        fish_info_data = {
            "fish_batch": fish_info_obj.fish_batch,
            "stock_date": fish_info_obj.stock_date,
            "number": fish_info_obj.number,
            "total_mass": fish_info_obj.total_mass,
            "name": fish_info_obj.name,
            "specification": fish_info_obj.specification,
            "test_report_stock": fish_info_obj.test_report_stock,
            "test_report_third": fish_info_obj.test_report_third,
            "stock_scene": fish_info_obj.stock_scene
        }

        trans_infos = fish_info_obj.transinfo.all()

        process_info_data = {
            "process_date": process_info_obj.process_date,
            "pack_environment": process_info_obj.pack_environment,
            "process_environment": process_info_obj.process_environment,
            "get_scene": process_info_obj.get_scene,
            "test_report_process": process_info_obj.test_report_process
        }

        data = {
            "product_info_data": product_info_data,
            "fish_info_data": fish_info_data,
            "trans_infos": trans_infos,
            "process_info_data": process_info_data,
            "is_product_detail": True
        }

        return render(request, "fishes/product_info_detail.html", data)

    def post(self, request):
        result = {
            "status": "ERROR",
            "msg": " "
        }
        path = request.get_full_path()
        if path.find("delete") != -1:  # 请求删除图片
            pid = int(request.POST.get("pid"))
            attr_name = request.POST.get("attr_name")
            product_info_obj = ProductInfo.objects.filter(id=pid).first()
            if delete_image(product_info_obj, attr_name):
                result["status"] = "SUCCESS"
                result["msg"] = "删除成功"
            else:
                result["msg"] = "删除失败，请刷新后重试！"
        else:
            pass

        return HttpResponse(json.dumps(result))



@csrf_exempt
def ImageUploadView(request):
    '''对图片上传进行处理'''
    pid = int(request.POST.get("pid"))
    attr_name = request.POST.get("attr_name")
    product_info_obj = ProductInfo.objects.filter(id=int(pid)).first()
    fish_info_obj = product_info_obj.fish_info
    process_info_obj = product_info_obj.process_info

    result = {
        "status": "SUCCESS",
        "msg": "上传成功！"
    }

    try:
        if attr_name == "pack_environment":
            process_info_obj.pack_environment = request.FILES.get("pack_environment")
            process_info_obj.save()
        elif attr_name == "test_report_stock":
            fish_info_obj.test_report_stock = request.FILES.get("test_report_stock")
            fish_info_obj.save()
        elif attr_name == "test_report_third":
            fish_info_obj.test_report_third = request.FILES.get("test_report_third")
            fish_info_obj.save()
        elif attr_name == "stock_scene":
            fish_info_obj.stock_scene = request.FILES.get("stock_scene")
            fish_info_obj.save()
        elif attr_name == "process_environment":
            process_info_obj.process_environment = request.FILES.get("process_environment")
            process_info_obj.save()
        elif attr_name == "get_scene":
            process_info_obj.get_scene = request.FILES.get("get_scene")
            process_info_obj.save()
        elif attr_name == "test_report_process":
            process_info_obj.test_report_process = request.FILES.get("test_report_process")
            process_info_obj.save()
    except Exception:
        result["status"] = "ERROR"
        result["msg"] = "上传出错，请重试！"

    return HttpResponse(json.dumps(result))



class FishPoolView(View):
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
            fish_batch_num = str(now.year)+str(now.month)+str(now.day)+str(ran_num)
            return render(request, 'fishes/add_product_mobile.html', {'pool_id': pool_id, "fish_batch_num": fish_batch_num})

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

@csrf_exempt
def AddProductView(request):
    """添加产品信息(入料)"""
    result = {"status": False, "message": '添加数据失败，请重试！'}
    fish_pool = FishPool.objects.filter(id=int(request.POST.get("val-poolID"))).first()
    data = {
        "pool_num_id": fish_pool.id,
        "fish_batch": request.POST.get("val-batchNum"),
        "name": request.POST.get("val-typename"),
        "specification": request.POST.get("val-specification"),
        "number": int(request.POST.get("val-fishnum")),
        "total_mass": float(request.POST.get("val-totalmass")),
        "stock_scene": request.FILES.get("pack_environment"),
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

                process_info = ProcessInfo.objects.create(fish_info_id=fish_info.id)

                # 领料成功后，默认向产品信息表添加领料成功的产品信息
                # 生成产品批次号
                now = datetime.datetime.now()
                ran_num = random.randint(1000, 10000)
                product_num = str(now.year) + str(now.month) + str(now.day) + str(ran_num)

                product_info_data = {
                    "product_batch": product_num,
                    "fish_info_id": fish_info.id,
                    "process_info_id": process_info.id
                }
                ProductInfo.objects.create(**product_info_data)

        except Exception as e:
            return HttpResponse(json.dumps(result))

        result['status'] = True
        result['message'] = '领料成功，请及时处理！'

        return HttpResponse(json.dumps(result))

def UserInfoView(request):
    """用户信息查看"""

    # 如果请求中没有“offset”说明是请求用户信息查看页面
    # 否则，是请求用户信息
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


def UserDetailView(request, uid):
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


def DeleteUserView(request):
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



def FishPoolInfoView(request):
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


def GenerateQRCode(request, key, pid):
    """生成二维码(鱼池、产品)"""
    url = None
    file_name = None
    if key == "pool":
        url = "http://" + request.get_host() + reverse("fishes:fishpool")+"?pid="+pid
        file_name = "鱼池" + pid + "号的二维码" + ".png"
    elif key == "product":
        url = "http://" + request.get_host() + reverse("fishes:search_view") + "?pid=" + pid
        file_name = "产品" + ProductInfo.objects.filter(id=int(pid)).first().product_batch + "批次的二维码" + ".png"
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()
    response = HttpResponse(image_stream)
    response['Content-Type'] = 'application/image'
    response['Content-Disposition'] = "attachment; filename*=utf-8''{0}".format(escape_uri_path(file_name))
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


def DeleteFishPool(request):
    """删除鱼池"""
    pool_nums = request.POST.getlist('pool_nums')
    result = {'status': False, 'message': '删除失败，请重试！'}
    for pool_num in pool_nums:
        fish_pool = get_object_or_404(FishPool, num=int(pool_num))
        fish_pool.delete()
    result['status'] = True
    result['message'] = '删除成功！'
    return HttpResponse(json.dumps(result))


def GenerateProductQRCodeView(request):
    """生成产品二维码"""
    url = request.GET.get("input-link")
    if url == '':   # 没有输入新的链接，则使用默认的链接
        url = "http://" + request.get_host() + reverse("fishes:homepage")
    file_name = "通用产品二维码" + ".png"

    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()
    response = HttpResponse(image_stream)
    response['Content-Type'] = 'application/image'
    response['Content-Disposition'] = "attachment; filename*=utf-8''{0}".format(escape_uri_path(file_name))
    # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file)
    return response


def ThirdPartTestReportView(request):
    """第三方检测报告管理"""
    time.sleep(1)
    return render(request, "fishes/third_part_test_report.html")


def VarietyView(request):
    """石斑鱼品种管理"""
    if request.GET.get('offset') is None:
        return render(request, "fishes/variety.html")

    search = request.GET.get('search')
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    offset = request.GET.get('offset')
    limit = request.GET.get('limit')

    varieties = None
    if search is not None and search.strip():
        varieties = Variety.objects.filter(Q(name=search) | Q(description=search))
    else:
        varieties = Variety.objects.all()

    if sort is not None:
        if order == 'asc':
            varieties = varieties.order_by('-' + sort)
        else:
            varieties = varieties.order_by(sort)

    total = varieties.count()
    print("total", total)

    data = []
    for variety in varieties:
        temp = {
            'id': variety.id,
            'name': variety.name,
            'description': variety.description
        }
        data.append(temp)

    result = {'total': total, 'rows': data[0+int(offset):0+int(offset)+int(limit)]}
    return HttpResponse(json.dumps(result))


def AddVarietyView(request):
    """添加石斑鱼品种名称"""
    result = {"status": False, "message": "添加数据失败，请重试！"}
    variety = {
        "name": request.POST.get("val-variety-name"),
        "description": request.POST.get("description") if request.POST.get("description") else None,
    }

    variety_created = Variety.objects.create(**variety)
    if variety_created is not None:
        result['status'] = True
        result['message'] = '添加品种名称成功！'

    return HttpResponse(json.dumps(result))


def DelVarietyView(request):
    """删除石斑鱼品种名称"""
    result = {"status": False, "message": "删除数据失败，请重试！"}
    ids = request.POST.get("variety_ids")
    ids_list = None
    if ids:
        ids_list = ids.split(',')
    if ids_list:
        for vid in ids_list:
            variety = get_object_or_404(Variety, id=int(vid))
            variety.delete()
        result['status'] = True
        result['message'] = "删除数据成功！"

    return HttpResponse(json.dumps(result))


def FeedbackNOTReplyView(request):
    """未回复反馈"""
    return render(request, "fishes/feedback_not_reply.html")


def FeedbackReplyView(request):
    """已回复反馈"""
    return render(request, "fishes/feedback_reply.html")


def SysSetForHomepageView(request):
    """网站首页内容设置"""
    return render(request, "fishes/sysset_for_homepage.html")


def SysSetForSearchResultView(request):
    """搜索结果页面设置"""
    return render(request, "fishes/sysset_for_serach_result.html")


def GetFishNumView(request):
    """获取每个鱼池的石斑鱼数量和品种"""
    data = {
        "pool_num": None,
        "variety": None,
        "fish_num": None
    }

    pools_in_using = FishPool.objects.filter(in_using=True)

    if pools_in_using is None:
        return HttpResponse(json.dumps(data))
    pool_num = []
    variety = []
    fish_num = []
    for pool in pools_in_using:
        fishes = pool.fishinfo.all()
        for fish in fishes:
            if fish.is_stocking:
                pool_num.append("鱼池 "+str(pool.num)+" 号")
                variety.append(fish.variety.name if fish.variety.name else "-")
                fish_num.append(fish.number)

    data['pool_num'] = pool_num
    data['variety'] = variety
    data['fish_num'] = fish_num
    return HttpResponse(json.dumps(data))


def GetVarietyNumView(request):
    """获取品种——鱼数量"""
    data = {
        "variety": None,
        "seriesData": None
    }

    varieties = Variety.objects.all()
    variety_list = []
    seriesData_list = []
    for variety in varieties:
        variety_list.append(variety.name)
        fishinfos = variety.fishinfo_variety.all()
        fish_num = 0
        for fishinfo in fishinfos:
            fish_num += fishinfo.number
        seriesData_list.append({"value": fish_num, "name": variety.name})

    data['variety'] = variety_list
    data['seriesData'] = seriesData_list

    return HttpResponse(json.dumps(data))


def GetProcessNumView(request):
    """获取生产数据进行统计"""
    result = {}
    data = {}
    processinfos = ProcessInfo.objects.all()
    for processinfo in processinfos:
        process_date = processinfo.process_date.strftime("%Y-%m-%d")
        fish_nums = processinfo.fish_info.number
        if process_date in data.keys():
            data[process_date] += fish_nums
        else:
            data[process_date] = fish_nums

    sorted(data)
    # result['date'] = list(data.keys())
    # result['data'] = list(data.values())
    # print(result)
    date_list = []
    data_list = []
    for key in sorted(data.keys()):
        date_list.append(key)
        data_list.append(data.get(key))

    result['date'] = date_list
    result['data'] = data_list

    today = datetime.datetime.today()
    start_date = today - timedelta(days=14)
    end_date = today + timedelta(days=14)

    result['start'] = start_date.strftime('%Y-%m-%d')
    result['end'] = end_date.strftime('%Y-%m-%d')

    return HttpResponse(json.dumps(result))


