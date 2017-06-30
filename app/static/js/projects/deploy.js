layui.use(['element', 'layer', 'util', 'form', 'layedit', 'laypage'], function () {
    var $ = layui.jquery;
    var element = layui.element();
    var layer = layui.layer;
    var util = layui.util;
    var form = layui.form();
    var layedit = layui.layedit;
    var laypage = layui.laypage;
 
    // 添加项目弹出层
    $('#deploy-info-btn').on('click', function () {
        layer.open({
            type: 1,
            title: '提测信息',
            skin: 'layui-layer-molv',
            content: $('#deploy-info-ctx'),
            area: ['460px', '320px'],
            // area: 'auto',
            // maxWidth: '900px',
            closeBtn: 1,
            resize: true
            // shadeClose: true,
        });
    });

    // 执行绑定
    form.on('submit(deployTest)', function(data) {
        if (data.field.environ == 2) {
            activate(5);
        } else {
            activate(2);
        }
        layer.closeAll();
        layer.load();
        // layer.msg(JSON.stringify(data.field));
        $.ajax({
            type: 'POST',
            url: '/projects/deploy',
            data: data.field,
            dataType: 'json',
            // contentType: false,
            processData: true,
            success: function (data, txtStatus, jqXHR) {
                layer.closeAll('loading');
                if (data.code === 200) {
                    layer.msg(data.msg, {
                        icon: 1,
                        time: 1600,
                        anim: 0,
                        shade: [0.6, '#c2c2c2']
                    },
                    // function () {
                    //     location.href="/projects/deploy";
                    // }
                    // activate(data.status)
                    activate(6),
                    );
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
    (function () {
        var $point_arr, $points, $progress, $trigger, activate, active, max, tracker, val;

        $trigger = $('.trigger').first();

        $points = $('.progress-points').first();

        $point_arr = $('[data-point]');

        $progress = $('.progress').first();

        val = parseInt($points.data('current')) - 1;

        max = $point_arr.length - 1;

        tracker = active = 0;

        activate = function(index) {
            if (index !== active) {
                active = index;
                $point_arr.removeClass('completed active');
                $point_arr.slice(0, index).addClass('completed');
                $point_arr.eq(active).addClass('active');
                return $progress.css('width', (index / max * 100) + "%");
            }
        };
        window.activate = activate;

        // $points.on('click', 'li', function(event) {
        //     var _index;
        //     _index = $point_arr.index(this);
        //     tracker = _index === 0 ? 1 : _index === val ? 0 : tracker;
        //     return activate(_index);
        // });

        // $trigger.on('click', function() {
        //     return activate(tracker++ % 2 === 0 ? 0 : val);
        // });

        setTimeout((function() {
            return activate(val);
        }), 1000);
    }).call(this);
});