(function() {
  $(document).ready(function() {
    $('.menu').click(function() {
      $('nav.right').addClass('open');
      $('body').addClass('menu-open');
      return false;
    });
    return $(document).click(function() {
      $('body').removeClass('menu-open');
      return $('nav').removeClass('open');
    });
  });

}).call(this);

