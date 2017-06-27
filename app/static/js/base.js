layui.use(['element', 'layer', 'util', 'form', 'layedit'], function () {
    var $ = layui.jquery;
    var element = layui.element();
    var layer = layui.layer;
    var util = layui.util;
    var form = layui.form();
    var layedit = layui.layedit;
    // 返回顶部按钮
    util.fixbar({
        bar1: '&#xe60f;',
        bgcolor: '#393D49'
    });
    // 表单提交
    form.on('submit(resetPassword)', function(data) {
        // layer.msg(JSON.stringify(data.field));
        $.ajax({
            type: 'POST',
            url: '/reset',
            data: data.field,
            dataType: 'json',
            processData: true,
            success: function (data, txtStatus, jqXHR) {
                if (data.code === 200) {
                    layer.msg(data.msg, {
                        icon: 1,
                        time: 2000,
                        anim: 0,
                        shade: [0.6, '#c2c2c2']
                    },
                    layer.closeAll());
                    // function () {
                    //     location.reload();
                    // });
                } else {
                    layer.msg(data.msg, {
                        icon: 2,
                        time: 2000,
                        anim: 6,
                        shade: [0.6, '#c2c2c2']
                    });
                }
            }
        });
        return false;
    });
    // 列表全部选择
    form.on('checkbox(chk-all)', function (data) {
        if (this.checked) {
            $('input[name="items[]"]').each(function () {
                this.checked = true;
            }) 
        } else {
            $('input[name="items[]"]').each(function (index, element) {
                element.checked = false;
            }) 
        }
        form.render();
    });
    // 确认密码验证
    form.verify({
        sameas: function (value) {
            if ($('#new_pwd').val() !== value) {
                return '确认密码不匹配';
            }
        }
    });
    // 富文本
    layedit.build('demo', {
        height: 360,
        uploadImage: {
            url: '',
            type: 'post'
        }
    });
    // 重置密码弹出层
    $('#reset-password').on('click', function () {
        layer.open({
            type: 1,
            title: '修改密码',
            skin: 'layui-layer-molv',
            content: $('#reset-pass-ctx'),
            area: ['450px', '300px'],
            closeBtn: 1,
            // shadeClose: true,
        });
    });
});