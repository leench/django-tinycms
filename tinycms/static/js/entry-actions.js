(function($){
	// tipWrap: 	提示消息的容器
	// maxNumber: 	最大输入字符
	$.fn.artTxtCount = function(tipWrap, maxNumber){
		var countClass = 'js_txtCount',		// 定义内部容器的CSS类名
			fullClass = 'js_txtFull',		// 定义超出字符的CSS类名
			disabledClass = 'disabled';		// 定义不可用提交按钮CSS类名

		// 统计字数
		var count = function(){
			var btn = $(this).closest('form').find(':submit'),
				val = $(this).val().length,

				// 是否禁用提交按钮
				disabled = {
					on: function(){
						btn.removeAttr('disabled').removeClass(disabledClass);
					},
					off: function(){
						btn.attr('disabled', 'disabled').addClass(disabledClass);
					}
				};

			//if (val == 0) disabled.off();
			if(val <= maxNumber){
				//if (val > 0) disabled.on();
				tipWrap.html('<span class="' + countClass + '"> <strong>' + val + ' \u4E2A\u5B57');
			}else{
				//disabled.off();
				tipWrap.html('<span class="' + countClass + ' ' + fullClass + '"> <strong>' + val + ' \u4E2A\u5B57');
			};
		};
		$(this).bind('keyup change', count);

		return this;
	};
})(jQuery);

$(document).ready(function() {
    if ( $('input#id_jump').is(':checked') ) {
        $("div.field-jump_to_url").show();
    } else {
        $("div.field-jump_to_url").hide();
    }
    $('input#id_jump').bind("change", function() {
        if ( $('input#id_jump').is(':checked') ) {
            $("div.field-jump_to_url").show('fast');
        } else {
            $("div.field-jump_to_url").hide('fast');
        }
    });
	$('#id_title').after('<span id="title_tips" class="tips"><span class="js_txtCount"> <strong>1 个字</strong></span>');
	$('#id_alternate_title').after('<span id="shorttitle_tips" class="tips"></span>');
	$('#id_description').after('<span id="description_tips" class="tips"></span>');
	$('#id_video_tip').after('<span id="video_tips" class="tips"></span>');

	$('#id_title').artTxtCount($('#title_tips'), 30);
	$('#id_alternate_title').artTxtCount($('#shorttitle_tips'), 15);
	$('#id_description').artTxtCount($('#description_tips'), 36);
	$('#id_video_tip').artTxtCount($('#video_tips'), 12);

	//
	$('form#article_form').submit(function(e){
		if ( $('select#id_category').val() == 1 ) {
			if ( confirm("栏目选择错误！是否继续？") ) {
				return;
			} else {
				return false;
			}
		}
	});
	$('form#video_form').submit(function(e){
		if ( $('select#id_category').val() == 1 ) {
			if ( confirm("栏目选择错误！是否继续？") ) {
				return;
			} else {
				return false;
			}
		}
	});
});

