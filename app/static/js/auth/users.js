layui.use(['element', 'layer', 'util', 'form', 'layedit', 'laypage'], function () {
    var $ = layui.jquery;
    var element = layui.element();
    var layer = layui.layer;
    var util = layui.util;
    var form = layui.form();
    var layedit = layui.layedit;
    var laypage = layui.laypage;

    // 表单提交
    form.on('submit(addUser)', function(data) {
        // layer.msg(JSON.stringify(data.field));
        $.ajax({
            type: 'POST',
            url: '/users',
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
                    function () {
                        location.href="/users";
                    });
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

    // 添加主机弹出层
    $('#add-user-btn').on('click', function () {
        layer.open({
            type: 1,
            title: '添加用户',
            skin: 'layui-layer-molv',
            content: $('#add-user-ctx'),
            area: ['600px', '480px'],
            // area: 'auto',
            // maxWidth: '900px',
            closeBtn: 1,
            resize: true
            // shadeClose: true,
        });
    });
});