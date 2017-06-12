layui.use(['element', 'layer', 'util', 'form', 'layedit', 'laypage'], function () {
    var $ = layui.jquery;
    var element = layui.element();
    var layer = layui.layer;
    var util = layui.util;
    var form = layui.form();
    var layedit = layui.layedit;
    var laypage = layui.laypage;
 
    (function() {
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

        $points.on('click', 'li', function(event) {
            var _index;
            _index = $point_arr.index(this);
            tracker = _index === 0 ? 1 : _index === val ? 0 : tracker;
            return activate(_index);
        });

        $trigger.on('click', function() {
            return activate(tracker++ % 2 === 0 ? 0 : val);
        });

        setTimeout((function() {
            return activate(val);
        }), 1000);

    }).call(this);
});