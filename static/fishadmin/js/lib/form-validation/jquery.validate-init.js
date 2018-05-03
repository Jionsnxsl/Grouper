
var form_validation = function() {
    var e = function() {
            jQuery(".form-valide").validate({
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