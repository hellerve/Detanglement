(function() {
  $(document).ready(function() {
    $('.menu').click(function() {
      $('.clearfix').css('background-color', '#404040');
      $('nav.right').addClass('open');
      $('body').addClass('menu-open');
      return false;
    });
    return $(document).click(function() {
      $('.clearfix').css('background-color', 'rgba(70, 70, 70, 0.35)');
      $('body').removeClass('menu-open');
      return $('nav').removeClass('open');
    });
  });

}).call(this);

