
var form_validation = function() {
    var e = function() {
            jQuery(".form-adduser").validate({
                ignore: [],
                errorClass: "invalid-feedback animated fadeInDown",
                errorElement: "div",
                errorPlacement: function(e, a) {
                    jQuery(a).parents(".form-group > div").append(e)
                },
                highlight: function(e) {
                    jQuery(e).closest(".form-group").removeClass("is-invalid").addClass("is-invalid")
                },
                success: function(e) {
                    jQuery(e).closest(".form-group").removeClass("is-invalid"), jQuery(e).remove()
                },
                rules: {
                    //TODO: 这里后面可以写成远程验证,查找JQuery validate的remote资料
                    "val-employeeID": {
                        required: !0,
                        minlength: 11,
                        digits: !0
                    },
                    "val-username": {
                        required: !0,
                        minlength: 3
                    },
                    "val-password": {
                        required: !0,
                        minlength: 5
                    },
                    "val-phonenum": {
                        required: !0,
                        phoneNum: !0
                    },
                },
                messages: {
                    "val-employeeID": {
                        required: "员工号不能为空",
                        minlength: "员工号长度必须大于11位",
                        digits: "员工号必须全部为数字"
                    },
                    "val-username": {
                        required: "用户名不能为空",
                        minlength: "用户名最小长度大于3个字符"
                    },
                    "val-password": {
                        required: "密码不能为空",
                        minlength: "密码长度必须大于5个字符"
                    },
                    "val-phonenum": {
                        required: '手机号不能为空',
                        phoneNum: '手机号格式不正确'
                    },
                }
            })
        };
    var a = function () {
        $("#val-employeeID").bind('input porpertychange', function () {
            $("#val-username").val($("#val-employeeID").val())
        });
        $.validator.addMethod("phoneNum", function (value, element) {
            var reg = /^((1[3-8][0-9])+\d{8})$/;
            return this.optional(element) || (reg.test(value));
        }, "手机格式不正确");
    };
    return {
        init: function() {
            e(), a(), jQuery(".js-select2").on("change", function() {
                jQuery(this).valid()
            })
        }
    }
}();
jQuery(function() {
    form_validation.init()
});

/* 鱼池添加表单验证 */
var addFishPoolFormInit = function () {
    $.validator.addMethod('num_required', function (value, element) {
        var reg = /^\d+$/;
        console.log(value);
        return this.optional(element) || (reg.test(value));
        }, "请选择一个鱼池编号");
    var e = function () {
        $(".form-addfishpool").validate({
            ignore: [],
            errorClass: "invalid-feedback animated fadeInDown",
            errorElement: "div",
            errorPlacement: function (e, a) {
                jQuery(a).parents(".form-group > div").append(e)
            },
            highlight: function (e) {
                jQuery(e).closest(".form-group").removeClass("is-invalid").addClass("is-invalid")
            },
            success: function (e) {
                jQuery(e).closest(".form-group").removeClass("is-invalid"), jQuery(e).remove()
            },
            rules: {
                "val-num": {
                    required: !0,
                    num_required: !0
                },
                "val-radius": {
                    required: !0,
                    number: !0,
                    min: 0
                },
                "val-depth": {
                    required: !0,
                    number: !0,
                    min: 0
                },
                "val-ph": {
                    required: !0,
                    number: !0,
                    min: 0
                },
                "val-temperature": {
                    required: !0,
                    number: !0,
                    min: 0
                },
            },
            messages: {
                "val-num": {
                    required: "鱼池编号不能为空",
                    num_required: "请选择一个鱼池编号"
                },
                "val-radius": {
                    required: "鱼池半径不能为空",
                    number: "半径必须为整数或小数",
                    min: "半径值必须大于0"
                },
                "val-depth": {
                    required: "鱼池深度不能为空",
                    number: "深度值必须为整数或小数",
                    min: "深度值必须大于0"
                },
                "val-ph": {
                    required: "鱼池PH值不能为空",
                    number: "鱼池PH值必须为整数或小数",
                    min: "鱼池PH值必须大于0"
                },
                "val-temperature": {
                    required: "鱼池温度不能为空",
                    number: "鱼池温度值必须为整数或小数",
                    min: "鱼池温度必须大于0"
                }
            }
        })
    };
    return {
        init: function() {
            e(), jQuery(".js-select2").on("change", function() {
                jQuery(this).valid()
            })
        }
    }
}();

$(function () {
    addFishPoolFormInit.init();
});


/* 入料添加表单验证 */
var addProductFormInit = function () {

    var e = function () {
        $(".form-addproduct").validate({
            ignore: [],
            errorClass: "invalid-feedback animated fadeInDown",
            errorElement: "div",
            errorPlacement: function (e, a) {
                jQuery(a).parents(".form-group > div").append(e)
            },
            highlight: function (e) {
                jQuery(e).closest(".form-group").removeClass("is-invalid").addClass("is-invalid")
            },
            success: function (e) {
                jQuery(e).closest(".form-group").removeClass("is-invalid"), jQuery(e).remove()
            },
            rules: {
                "val-specification": {
                    required: !0,
                },
                "val-fishnum": {
                    required: !0,
                    digits: !0,
                    min: 0
                },
                "val-totalmass": {
                    required: !0,
                    number: !0,
                    min: 0
                },
            },
            messages: {
                "val-specification": {
                    required: "鱼规格不能为空",
                },
                "val-fishnum": {
                    required: "鱼的数量不能为空",
                    digits: "鱼的数量必须为正整数",
                    min: "鱼的数量必须大于0"
                },
                "val-totalmass": {
                    required: "鱼的总重量不能为空",
                    number: "鱼的总重量必须为整数或小数",
                    min: "鱼的总重量必须大于0"
                },
            }
        })
    };
    return {
        init: function() {
            e(), jQuery(".js-select2").on("change", function() {
                jQuery(this).valid()
            })
        }
    }
}();

$(function () {
    addProductFormInit.init();
});


/*
*
* 领料验证 form-process-product
* */

var processProductFormInit = function () {

    var e = function () {
        $(".form-process-product").validate({
            ignore: [],
            errorClass: "invalid-feedback animated fadeInDown",
            errorElement: "div",
            errorPlacement: function (e, a) {
                jQuery(a).parents(".form-group > div").append(e)
            },
            highlight: function (e) {
                jQuery(e).closest(".form-group").removeClass("is-invalid").addClass("is-invalid")
            },
            success: function (e) {
                jQuery(e).closest(".form-group").removeClass("is-invalid"), jQuery(e).remove()
            },
            rules: {
                "val-fishnum": {
                    required: !0,
                    digits: !0,
                    min: 0
                },
            },
            messages: {
                "val-fishnum": {
                    required: "鱼的数量不能为空",
                    digits: "鱼的数量必须为正整数",
                    min: "鱼的数量必须大于0的数字"
                },
            }
        })
    };
    return {
        init: function() {
            e(), jQuery(".js-select2").on("change", function() {
                jQuery(this).valid()
            })
        }
    }
}();

$(function () {
    processProductFormInit.init();
});


