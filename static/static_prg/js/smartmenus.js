// Скрипт для SmartMenus
// SmartMenus init sm-simple
$(function() {
  $('#main-menu-simple').smartmenus({
	mainMenuSubOffsetX: 10,
	mainMenuSubOffsetY: 0,
	subMenusSubOffsetX: 10,
	subMenusSubOffsetY: 0
	});
});

// SmartMenus init sm-blue
$(function() {
  $('#main-menu').smartmenus({
    subMenusSubOffsetX: 1,
    subMenusSubOffsetY: -8
  });
});

// Set proper max-height for sub menus in desktop view
$('#main-menu').bind('beforeshow.smapi', function(e, menu) {
  var $sub = $(menu),
    hasSubMenus = $sub.find('ul').length && !$sub.hasClass('mega-menu');
  // if the sub doesn't have any deeper sub menus, apply max-height
  if (!hasSubMenus) {
    var obj = $(this).data('smartmenus');
    if (obj.isCollapsible()) {
      $sub.css({
        'overflow-y': '',
        'max-height': ''
      });
    } else {
      var $a = $sub.dataSM('parent-a'),
        $li = $a.closest('li'),
        $ul = $li.parent(),
        level = $sub.dataSM('level'),
        $win = $(window),
        winH = $win.height(),
        winY = $win.scrollTop(),
        subY = winY;
      // if the parent menu is horizontal
      if ($ul.parent().is('[data-sm-horizontal-sub]') || level == 2 && !$ul.hasClass('sm-vertical')) {
        var itemY = $a.offset().top,
          itemH = obj.getHeight($a),
          subOffsetY = level == 2 ? obj.opts.mainMenuSubOffsetY : obj.opts.subMenusSubOffsetY,
          subY = itemY + itemH + subOffsetY;
      }
      $sub.css({
        'max-height': winH + winY - subY
      });
    }
  }
});

// Set overflow-y: auto for sub menus in desktop view
// this needs to be done on the 'show.smapi' event because the script resets overflow on menu show
$('#main-menu').bind('show.smapi', function(e, menu) {
  var $sub = $(menu),
    hasSubMenus = $sub.find('ul').length && !$sub.hasClass('mega-menu');
  // if the sub doesn't have any deeper sub menus, apply overflow-y: auto
  if (!hasSubMenus) {
    var obj = $(this).data('smartmenus');
    if (!obj.isCollapsible()) {
      // the timeout fixes an issue in jQuery 3
      // it may need to be adjusted if you use a longer "showDuration" than the default
      setTimeout(function() {
        $sub.css('overflow-y', 'auto');
      }, 1);
    }
  }
});