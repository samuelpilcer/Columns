$(function(){

  $(document).scroll(function(){
      var top=$(this).scrollTop();
      if(top<180){
        var dif=1-top/180;
        $(".navbar-image").css({opacity:dif});
        $(".navbar-image").show();
        $(".navbar-material-blog .navbar-wrapper").css({'padding-top': '180px'});
        $(".navbar-material-blog").removeClass("navbar-fixed-top");
        $(".navbar-material-blog").addClass("navbar-absolute-top");
      }
      else {
        $(".navbar-image").css({opacity:0});
        $(".navbar-image").hide();
        $(".navbar-material-blog .navbar-wrapper").css({'padding-top': 0});
        $(".navbar-material-blog").removeClass("navbar-absolute-top");
        $(".navbar-material-blog").addClass("navbar-fixed-top");
      }
  });

  $("a[href*=#]").click(function(e) {
    e.preventDefault();
  });  
  
});