layui.use(['element', 'layer', 'util', 'form', 'layedit', 'laypage', 'upload'], function () {
    var $ = layui.jquery;
    var element = layui.element();
    var layer = layui.layer;
    var util = layui.util;
    var form = layui.form();
    var layedit = layui.layedit;
    var laypage = layui.laypage;

    // 文件上传
    layui.upload({
        url: '/projects/uploads',
        type: 'file',
        ext: 'yaml|yml|txt',
        success: function (res, input) {
            // console.log(res.filepath);
            $('#playbook').val(res.filepath);
        }
    });

    // 添加项目表单提交
    form.on('submit(addProject)', function(data) {
        // layer.msg(JSON.stringify(data.field));

        $.ajax({
            type: 'POST',
            url: '/projects/',
            data: data.field,
            dataType: 'json',
            // contentType: false,
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
                        location.href="/projects/";
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

    // 执行绑定
    form.on('submit(bindHost)', function(data) {
        layer.msg(JSON.stringify(data.field));
        $.ajax({
            type: 'POST',
            url: '/projects/bind',
            data: data.field,
            dataType: 'json',
            // contentType: false,
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
                        location.href="/projects/";
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
    // 添加项目弹出层
    $('#add-project-btn').on('click', function () {
        layer.open({
            type: 1,
            title: '添加项目',
            skin: 'layui-layer-molv',
            content: $('#add-project-ctx'),
            area: ['680px', '520px'],
            // area: 'auto',
            // maxWidth: '900px',
            closeBtn: 1,
            resize: true
            // shadeClose: true,
        });
    });

    // 修改项目
    $(document).on('click', '#update-project-btn', function () {
        layer.open({
            type: 1,
            title: '编辑项目',
            skin: 'layui-layer-molv',
            content: $('#add-project-ctx'),
            area: ['680px', '520px'],
            // area: 'auto',
            // maxWidth: '900px',
            closeBtn: 1,
            resize: true
            // shadeClose: true,
        });
        return false;
    });
    
    // 绑定主机
    $('table').on('click', '#bind-host-btn', function () {
        layer.open({
            type: 1,
            title: '绑定主机',
            skin: 'layui-layer-molv',
            content: $('#bind-host-ctx'),
            area: ['520px', '360px'],
            // area: 'auto',
            // maxWidth: '900px',
            closeBtn: 1,
            resize: true
            // shadeClose: true,
        });
        return false;
    });
});