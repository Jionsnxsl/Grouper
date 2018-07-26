$(function() {
    "use strict";
    $(function() {
            $(".preloader").fadeOut();
        }),

        jQuery(document).on("click", ".mega-dropdown", function(i) {
            i.stopPropagation();
        });


    var i = function() {
        (window.innerWidth > 0 ? window.innerWidth : this.screen.width) < 1170 ? ($("body").addClass("mini-sidebar"),
            $(".navbar-brand span").hide(), $(".scroll-sidebar, .slimScrollDiv").css("overflow-x", "visible").parent().css("overflow", "visible"),
            $(".sidebartoggler i").addClass("ti-menu")) : ($("body").removeClass("mini-sidebar"),
            $(".navbar-brand span").show());
        var i = (window.innerHeight > 0 ? window.innerHeight : this.screen.height) - 1;
        (i -= 70) < 1 && (i = 1), i > 70 && $(".page-wrapper").css("min-height", i + "px");
    };

/* 这段代码会把首页中的缩小左侧栏事件变为无效，请不要打开注释！
    $(window).ready(i), $(window).on("resize", i), $(".sidebartoggler").on("click", function() {
            $("body").hasClass("mini-sidebar") ? ($("body").trigger("resize"), $(".scroll-sidebar, .slimScrollDiv").css("overflow", "hidden").parent().css("overflow", "visible"),
                $("body").removeClass("mini-sidebar"), $(".navbar-brand span").show()) : ($("body").trigger("resize"),
                $(".scroll-sidebar, .slimScrollDiv").css("overflow-x", "visible").parent().css("overflow", "visible"),
                $("body").addClass("mini-sidebar"), $(".navbar-brand span").hide());
        }),
*/

/* 这段代码导致手机版的左侧栏事件无效
        $(".fix-header .header").stick_in_parent({}), $(".nav-toggler").click(function() {
            $("body").toggleClass("show-sidebar"), $(".nav-toggler i").toggleClass("mdi mdi-menu"),
                $(".nav-toggler i").addClass("mdi mdi-close");
        }),

*/
/* 这段代码导致搜索框出现后自动消失
        $(".search-box a, .search-box .app-search .srh-btn").on("click", function() {
            $(".app-search").slideToggle(200);
        }),
*/


        $(".floating-labels .form-control").on("focus blur", function(i) {
            $(this).parents(".form-group").toggleClass("focused", "focus" === i.type || this.value.length > 0);
        }).trigger("blur"), $(function() {
            for (var i = window.location, o = $("ul#sidebarnav a").filter(function() {
                    return this.href == i;
                }).addClass("active").parent().addClass("active");;) {
                if (!o.is("li")) break;
                o = o.parent().addClass("in").parent().addClass("active");
            }
        }),

        $(function() {
                function LeftSidebarMenu() {
                $("nav a[aria-expanded]").bind('click', function () {
                    $("nav a[aria-expanded]").attr('aria-expanded', false).removeClass('active').parent().removeClass('active')
                    $("nav a[aria-expanded]").next('ul').attr('aria-expanded', false).removeClass('in')
                    $("nav a[aria-expanded]").next('ul').children('li').removeClass('active').children('a').removeClass('active')
                   if($(this).siblings('ul').length == 0){
                       $(this).addClass("active").parent().addClass('active');
                   } else {
                       $(this).addClass('active').attr('aria-expanded', true).parent().addClass('active')
                       $(this).next('ul').attr('aria-expanded', true).addClass('in')
                   }
                });

                $("nav ul[aria-expanded] li a").bind('click', function () {
                    $(this).parent().removeClass('active').siblings().removeClass('active').children('a').removeClass('active')
                    $(this).addClass('active').parent().addClass('active')
                });

            };
            LeftSidebarMenu();
        }),

        $(".scroll-sidebar").slimScroll({
            position: "left",
            size: "5px",
            height: "100%",
            color: "#dcdcdc"
        }),

        $(".message-center").slimScroll({
            position: "right",
            size: "5px",
            color: "#dcdcdc"
        }),

        $(".aboutscroll").slimScroll({
            position: "right",
            size: "5px",
            height: "80",
            color: "#dcdcdc"
        }),

        $(".message-scroll").slimScroll({
            position: "right",
            size: "5px",
            height: "570",
            color: "#dcdcdc"
        }),

        $(".chat-box").slimScroll({
            position: "right",
            size: "5px",
            height: "470",
            color: "#dcdcdc"
        }),

        $(".slimscrollright").slimScroll({
            height: "100%",
            position: "right",
            size: "5px",
            color: "#dcdcdc"
        }),



        $("body").trigger("resize"), $(".list-task li label").click(function() {
            $(this).toggleClass("task-done");
        }),



        $("#to-recover").on("click", function() {
            $("#loginform").slideUp(), $("#recoverform").fadeIn();
        }),



        $('a[data-action="collapse"]').on("click", function(i) {
            i.preventDefault(), $(this).closest(".card").find('[data-action="collapse"] i').toggleClass("ti-minus ti-plus"),
                $(this).closest(".card").children(".card-body").collapse("toggle");
        }),



        $('a[data-action="expand"]').on("click", function(i) {
            i.preventDefault(), $(this).closest(".card").find('[data-action="expand"] i').toggleClass("mdi-arrow-expand mdi-arrow-compress"),
                $(this).closest(".card").toggleClass("card-fullscreen");
        }),



        $('a[data-action="close"]').on("click", function() {
            $(this).closest(".card").removeClass().slideUp("fast");
        });
});

/* 用户信息查看初始化(START) */
function userInfoInit() {
    var operateFormatter = function (value, row, index) {//赋予的参数
        //注意：这里的 row.id 是用户的ID
        //return "<button class='btn btn-info btn-sm' type='button'><a href="+"/fishes/admin/userdetail/"+parseInt(row.id)+" class='fa fa-paste'>详情</a></button>"
        return '<a class="btn btn-info" href=' + '/fishes/admin/userdetail/' + parseInt(row.id) + ' role="button">详细</a>'
    };

    const $table = $('#userinfo-table');
    const $remove = $('#delete-user');
    let selections = [];

    function initTable() {
        $table.bootstrapTable({
            height: getHeight(),
            url: "/fishes/admin/userinfo/"/*"{% url 'fishes:userinfo' %}"*/,
            columns: [{
                field: 'state',
                checkbox: true,
                align: 'center',
            }, {
                title: '用户名',
                field: 'username',
                align: 'center',
                sortable: true
            }, {
                field: 'employeeID',
                title: '员工号',
                sortable: true,
                editable: true,
                align: 'center'
            }, {
                field: 'is_staff',
                title: '是否为普通员工',
                align: 'center',
            }, {
                field: 'is_superuser',
                title: '是否为管理员',
                align: 'center',
            }, {
                field: 'operate',
                title: '操作',
                align: 'center',
                formatter: operateFormatter
            }]
        });
        // sometimes footer render error.
        setTimeout(() => {
            $table.bootstrapTable('resetView');
        }, 200);
        $table.on('check.bs.table uncheck.bs.table ' +
            'check-all.bs.table uncheck-all.bs.table', () => {
            $remove.prop('disabled', !$table.bootstrapTable('getSelections').length);

            // save your data, here just save the current page
            selections = getIdSelections();
            // push or splice the selections if you want to save all data selections
        });
        $remove.click(() => {
            // 删除用户
            const users = getIdSelections();
            var confirm = window.confirm('是否要删除 ' + users);
            if (confirm) {
                $(".preloader-submit-data").show();
                $.ajax({
                    url: "/fishes/admin/deleteuser"/*"{% url 'fishes:deleteuser' %}"*/,
                    type: "POST",
                    data: {'employeeIDs': users},
                    traditional: true,
                    dataType: "JSON",
                    success: function (data) {
                        $(".preloader-submit-data").hide();
                        if (data.status) {
                            alert(data.message);
                            location.reload();
                        } else {
                            alert(data.message);
                            location.reload();
                        }
                    }
                });
            } else {
                //$remove.prop('disabled', !$table.bootstrapTable('getSelections').length);
            }
        });
        $(window).resize(() => {
            $table.bootstrapTable('resetView', {
                height: getHeight()
            });
        });
    }

    function getIdSelections() {
        return $.map($table.bootstrapTable('getSelections'), ({employeeID}) => employeeID);
    }

    function getHeight() {
        return $(window).height() - $('h1').outerHeight(true);
    }

    initTable();
}
/* 用户信息查看初始化(END) */

/* 用户信息添加初始化(START) */
function addUser() {
    $("#add-user-submit").click(function () {
        if ($(".form-adduser").valid()) { // 已经在validate-init.js中注册了验证函数
            $(".preloader-submit-data").show();
            $.ajax({
                url: "/fishes/admin/adduser/"/*"{% url 'fishes:adduser' %}"*/,
                type: "POST",
                data: $(".form-adduser").serialize(),
                dataType: "JSON",
                success: function (data) {
                    $(".preloader-submit-data").hide();
                    if (data.status) {
                        alert(data.message);
                        location.reload();
                    } else {
                        alert(data.message);
                        location.reload();
                    }
                }
            });
        } else {
            console.log('无效');
        }
    });
}
/*  用户信息添加初始化(END)*/

/* 鱼池信息查看初始化(START) */
function fishInfoInit() {
    var operateFormatter = function (value, row, index) {//赋予的参数
        //注意：这里的 row.id 是用户的ID
        return '<a class="btn btn-info" href=' + '/fishes/admin/generateqrcode/' +'pool-'+ parseInt(row.id) + ' role="button">鱼池二维码</a>'
        // return "<button class='btn btn-info btn-sm' type='button'><a href="+"/fishes/admin/userdetail/"+parseInt(row.id)+" class='fa fa-paste'>详情</a></button>"
    };

    var in_using_formater = function (value, row, index) {
        if(value){
            return '是'
        }else {
            return '否'
        }
    };

    const $table = $('#fishpool-table');
    const $remove = $('#delete-pool');
    let selections = [];

    function initTable() {
        $table.bootstrapTable({
            height: getHeight(),
            url: "/fishes/admin/fishpoolinfo/"/*"{% url 'fishes:fishpoolinfo' %}"*/,
            columns: [{
                field: 'state',
                checkbox: true,
                align: 'center',
            }, {
                title: '鱼池编号',
                field: 'num',
                align: 'center',
                sortable: true
            }, {
                field: 'radius',
                title: '鱼池半径',
                align: 'center'
            }, {
                field: 'depth',
                title: '鱼池深度',
                align: 'center',
            }, {
                field: 'PH',
                title: 'PH值',
                align: 'center',
            }, {
                field: 'temperature',
                title: '水温',
                align: 'center',
            }, {
                field: 'in_using',
                title: '是否正在使用中',
                align: 'center',
                formatter: in_using_formater
            }, {
                field: 'operate',
                title: '操作',
                align: 'center',
                formatter: operateFormatter
            }]
        });
        // sometimes footer render error.
        setTimeout(() => {
            $table.bootstrapTable('resetView');
        }, 200);
        $table.on('check.bs.table uncheck.bs.table ' +
            'check-all.bs.table uncheck-all.bs.table', () => {
            $remove.prop('disabled', !$table.bootstrapTable('getSelections').length);
            // save your data, here just save the current page
            selections = getIdSelections();
            // push or splice the selections if you want to save all data selections
        });
        $remove.click(() => {
            // 删除鱼池
            const pools = getIdSelections();
            var confirm = window.confirm('是否要删除 ' + pools);
            if (confirm) {
                $(".preloader-submit-data").show();
                $.ajax({
                    url: "/fishes/admin/deletefishpool/"/*"{% url 'fishes:deletefishpool' %}"*/,
                    type: "POST",
                    data: {'pool_nums': pools},
                    traditional: true,
                    dataType: "JSON",
                    success: function (data) {
                        $(".preloader-submit-data").hide();
                        if (data.status) {
                            alert(data.message);
                            location.reload();
                        } else {
                            alert(data.message);
                            location.reload();
                        }
                    }
                });
            } else {
                //$remove.prop('disabled', !$table.bootstrapTable('getSelections').length);
            }
        });
        $(window).resize(() => {
            $table.bootstrapTable('resetView', {
                height: getHeight()
            });
        });
    }

    function getIdSelections() {
        return $.map($table.bootstrapTable('getSelections'), ({num}) => num);
    }

    function getHeight() {
        return $(window).height() - $('h1').outerHeight(true);
    }

    $(() => {
        initTable();
    });
}
/* 鱼池信息查看初始化(END) */

/* 鱼池信息添加初始化(START) */
function addFishPool() {
    $("#add-fishpool-submit").click(function () {
        if ($(".form-addfishpool").valid()) { // 已经在validate-init.js中注册了验证函数
            $(".preloader-submit-data").show();
            $.ajax({
                url: "/fishes/admin/addfishpool/"/*"{% url 'fishes:adduser' %}"*/,
                type: "POST",
                data: $(".form-addfishpool").serialize(),
                dataType: "JSON",
                success: function (data) {
                    $(".preloader-submit-data").hide();
                    if (data.status) {
                        alert(data.message);
                        location.reload();
                    } else {
                        alert(data.message);
                        location.reload();
                    }
                }
            });
        } else {
            console.log('无效');
        }
    });
}
/*  鱼池信息添加初始化(END)*/

/* 入料初始化(START) */
$.extend({
    addProduct: function () {
        $("#add-product-submit").click(function () {
            if ($(".form-addproduct").valid()) { // 已经在validate-init.js中注册了验证函数
                $(".preloader-submit-data").show();
                var form_data = new FormData($(".form-addproduct")[0]);
                $.ajax({
                    url: "/fishes/admin/m/addproduct/"/*"{% url 'fishes:adduser' %}"*/,
                    type: "POST",
                    data: form_data,    //$(".form-addproduct").serialize(),
                    dataType: "JSON",
                    processData:false,
                    contentType:false,
                    success: function (data) {
                        $(".preloader-submit-data").hide();
                        if (data.status) {
                            // 成功添加---->跳转到后台主页
                            alert(data.message);
                            //location.reload();
                            location.href = "/fishes/admin";
                        } else {
                            // 添加失败 ---> 刷新当前页面
                            alert(data.message);
                            location.reload();
                        }
                    },
                    error: function(xhr, type, errorThrown) {
                        alert('网络异常，请稍后再试！');
                    }
                });
            } else {
                console.log('无效');
            }
        });
    }
});
/*  入料初始化(END)*/


/* 转移鱼初始化(START) */
$.extend({
    transProduct: function () {
        $("#add-trans-submit").click(function () {
            //if ($(".form-transproduct").valid())  //这个表单不在进行验证，都是系统提供选择
                $(".preloader-submit-data").show();
                $.ajax({
                    url: "/fishes/admin/m/transproduct/"/*"{% url 'fishes:adduser' %}"*/,
                    type: "POST",
                    data: $(".form-transproduct").serialize(),
                    dataType: "JSON",
                    success: function (data) {
                        $(".preloader-submit-data").hide();
                        if (data.status) {
                            // 转移成功 --》 跳转到后台主页
                            alert(data.message);
                            location.href = "/fishes/admin";
                            //location.reload();
                        } else {
                            // 否则刷新当前页面
                            alert(data.message);
                            location.reload();
                        }
                    }
                });
        });
    }
});
/*  转移鱼初始化(END)*/

/* 领料提交事件(START) */
$.extend({
    processProduct: function () {
        $("#process-product").click(function () {
            //if ($(".form-transproduct").valid())  //这个表单不在进行验证，都是系统提供选择
                $(".preloader-submit-data").show();
                $.ajax({
                    url: "/fishes/admin/m/processproduct/"/*"{% url 'fishes:adduser' %}"*/,
                    type: "POST",
                    data: $("#form-process-product").serialize(),
                    dataType: "JSON",
                    success: function (data) {
                        $(".preloader-submit-data").hide();
                        if (data.status) {
                            // 领料成功---》跳转到后台主页
                            alert(data.message);
                            location.href = '/fishes/admin/';
                        } else {
                            alert(data.message);
                            location.reload();
                        }
                    }
                });
        });
    }
});
/*  领料提交事件(END)*/

/* 产品信息查看初始化(START) */
function productInfoInit() {
    var operateFormatter = function (value, row, index) {//赋予的参数
        //注意：这里的 row.id 是产品信息的ID
        //console.log(row);
        //console.log(row.id);
        //return "<button class='btn btn-info btn-sm' type='button'><a href="+"/fishes/admin/userdetail/"+parseInt(row.id)+" class='fa fa-paste'>详情</a></button>"
        return '<a class="btn btn-info" href=' + '/fishes/admin/productdetail/?pid=' + parseInt(row.id) + ' role="button">详细</a>'
    };

    const $table = $('#productinfo-table');
    // const $remove = $('#delete-user'); // 产品查看不提供快速删除按钮
    let selections = [];

    function initTable() {
        $table.bootstrapTable({
            height: getHeight(),
            url: "/fishes/admin/productinfo/"/*"{% url 'fishes:userinfo' %}"*/,
            columns: [{
                field: 'product_batch',
                title: '产品批次',
                align: 'center',
                sortable: true
            }, {
                field: 'fish_batch',
                title: '鱼批次',
                sortable: true,
                align: 'center'
            }, {
                field: 'product_date',
                title: '产品生成时间',
                align: 'center',
            },  {
                field: 'operate',
                title: '操作',
                align: 'center',
                formatter: operateFormatter
            }]
        });
        // sometimes footer render error.
        setTimeout(() => {
            $table.bootstrapTable('resetView');
        }, 200);
        $table.on('check.bs.table uncheck.bs.table ' +
            'check-all.bs.table uncheck-all.bs.table', () => {
            $remove.prop('disabled', !$table.bootstrapTable('getSelections').length);

            // save your data, here just save the current page
            selections = getIdSelections();
            // push or splice the selections if you want to save all data selections
        });
        $(window).resize(() => {
            $table.bootstrapTable('resetView', {
                height: getHeight()
            });
        });
    }

    function getIdSelections() {
        return $.map($table.bootstrapTable('getSelections'), ({employeeID}) => employeeID);
    }

    function getHeight() {
        return $(window).height() - $('h1').outerHeight(true);
    }

    initTable();
}
/* 产品信息查看初始化(END) */

/* 产品详细信息中的上传插件初始化(START) */
function initFileinput(ctrname, uploadurl, previewurl, pid, attr_name) {
            $("#" + ctrname).fileinput({
                language: 'zh', //设置语言
                theme: 'fa',
                showUpload: true,
                dropZoneEnabled: false,
                browseClass: "btn btn-primary", //按钮样式
                allowedFileExtensions: ['jpg', 'png'],  //接收的文件后缀
                uploadUrl: uploadurl, //上传的地址
                enctype:'multipart/form-data',
                previewFileType: "image",
                browseClass: "btn btn-success",
                //browseLabel: "Pick Image",
                browseIcon: "<i class=\"fa fa-picture-o\"></i> ",
                removeClass: "btn btn-danger",
                //removeLabel: "Delete",
                removeIcon: "<i class=\"fa fa-trash\"></i> ",
                uploadClass: "btn btn-info",
                //uploadLabel: "Upload",
                uploadIcon: "<i class=\"fa fa-upload\"></i> ",
                minFileCount: 1,
                minFileSize: 1,
                layoutTemplates: {
                    // actionDelete:'', //去除上传预览的缩略图中的删除图标
                    //actionUpload: '',//去除上传预览缩略图中的上传图片；
                    //actionZoom: ''   //去除上传预览缩略图中的查看详情预览的缩略图标
                },
                uploadExtraData: {  //为上传的图片添加额外信息
                    pid: pid,
                    attr_name: attr_name,
                },
                deleteExtraData:{  //为删除添加额外信息
                    pid: pid,
                    attr_name: attr_name,
                },
                overwriteInitial: true,
                initialPreviewAsData: true,
                initialPreview: [
                    previewurl, //用来请求预览图片的URL
                ],
                initialPreviewConfig: [
                    // url ： 用来删除的URL，去除的话删除按钮无效
                    {caption: "nature-1.jpg", size: 329892, width: "120px", url: "?delete", key: 1},
                ]
            });

            // 上传错误
            $('#' + ctrname).on('fileerror', function(event, data, msg) {
                console.log("ERROR");
            });

            // 上传成功
            $("#" + ctrname).on("fileuploaded", function (event, data, previewId, index) {
                console.log("OK");
            });
        }
/* 产品详细信息中的上传插件初始化(END) */
