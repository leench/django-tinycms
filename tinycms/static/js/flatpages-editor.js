$(document).ready(function() {
	$('textarea#id_content').tinymce({
		// Location of TinyMCE script
		script_url : '/static/js/tiny_mce/tiny_mce.js',

		// General options
		theme : "advanced",
		//skin : "o2k7",
        //skin_variant : "silver",

		language : "cn", 

		width : 540,
		height: 280,

		plugins : "autolink,lists,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,advlist",

		/*
		plugins : "autolink,lists,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,advlist",
		*/

		// Theme options
		theme_advanced_buttons1 : "fontsizeselect,separator,bold,italic,underline,mediaupload,separator,forecolor,backcolor,separator,strikethrough,justifyleft,justifycenter,justifyright,justifyfull,bullist,numlist,undo,redo,link,unlink,code",
		//theme_advanced_buttons2 : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,|,insertdate,inserttime,|,cite,abbr,acronym,del,ins,attribs,|,nonbreaking,pagebreak",
		//theme_advanced_buttons3 : "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,media,|,fullscreen",

		/*
		theme_advanced_buttons1 : "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,styleselect,formatselect,fontselect,fontsizeselect",
		theme_advanced_buttons2 : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,|,insertdate,inserttime,preview,|,forecolor,backcolor",
		theme_advanced_buttons3 : "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,advhr,|,print,|,ltr,rtl,|,fullscreen",
		theme_advanced_buttons4 : "insertlayer,moveforward,movebackward,absolute,|,styleprops,|,cite,abbr,acronym,del,ins,attribs,|,visualchars,nonbreaking,template,pagebreak",
		*/
		theme_advanced_toolbar_location : "top",
		theme_advanced_toolbar_align : "left",
		theme_advanced_statusbar_location : "bottom",
		theme_advanced_resizing : true,

		theme_advanced_styles : "Header 1=header1;Header 2=header2;Header 3=header3;Table Row=tableRow1",
		theme_advanced_font_sizes: "10px,12px,13px,14px,16px,18px,20px",
		font_size_style_values : "10px,12px,13px,14px,16px,18px,20px",

		// Example content CSS (should be your site CSS)
		//content_css : "css/content.css",
		content_css : "/static/css/tinymce_content.css",

		// Drop lists for link/image/media/template dialogs
		template_external_list_url : "lists/template_list.js",
		external_link_list_url : "lists/link_list.js",
		external_image_list_url : "lists/image_list.js",
		media_external_list_url : "lists/media_list.js",

		setup : function(ed) {
			/*
			ed.onInit.add(function(ed) {
				ed.pasteAsPlainText = true;
			});
			*/
			// Add a custom button
			ed.addButton('mediaupload', {
				title : 'Í¼Æ¬ÉÏ´«',
				image : '/static/imgs/upload.gif',
				onclick : function() {
					$.colorbox({width:"640px", height:"80%", transition:"fade", href:"/media-upload/"});
					// Add you own code to execute something on click
					//ed.focus();
					//ed.selection.setContent('Hello world!');
				}
			});
		},

	});
});
