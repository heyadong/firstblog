# flask_learning
这是一个FLASK学习项目
用flask编写的简单的博客
2018/5/9 完成图片上传功能。包括非JPG图片上传验证提示
2018/5/11 图片列表的异步加载
使用Jquery  ajax
官方文档的例子：
jquery  example:
$.ajax({
  url: "/api/getWeather",
  data: {
    zipcode: 97201
  },
  success: function( result ) {
    $( "#weather-temp" ).html( "<strong>" + result + "</strong> degrees" );
  }
});
1,定义图片列表的url
@blog.route('/pics/')
def get_pics():
  # 查询图片：
  photos = Photos.query.all()
  # photo查询对象无法序列化所以将查询结转化成一个列表：
  pics_list = list()
  for photo in photos:
      pic = dict(id=photo.id, photo_name=photo.photo_name)
      photos.append(pic)
  return pics_list
2，前端获取数据
photos.html
<script>
$count = 0  //点击次数
$SCRIPT_ROOT = {{ request.script_root|tojson|safe }}
$(function(){
    $(#c1).bind('click',function(){
        count += 1                  //每点击一次计数+1
        $.getJSON($SCRIPT_ROOT+'/pics',
        {
          count：count

         }，
         function(data){
           $('table').append("<tr><td>"+
           data[i].id+
           "</td><td><img style=\"width: 90px;height: 70px\" class=\"img-rounded img-responsive\" src=\""
           +$SCRIPT_ROOT+'static/uploads/'+data[i].photo_name+"\"><td/><td></td></tr>")
           // table 标签下追加添加一行
         }

    )

   });
})

</script>
