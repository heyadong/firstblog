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
3.
使用flask-migrate
from flask_migrate import Migrate, MigrateCommands
migrate = Migrate(app,db)
manager.add_commands('db',MigrateCommands)

命令行输入
python manage.py db init 初始化迁移脚本
python manage.py db migrate -m "initial migration" 相当于db.crate_all()
使用db migrate 报如下错误：
alembic.util.exc.CommandError: Can't locate revision identified by '3901f09df9fb'
数据库更新的历史版本对不上。
删除数据库中的数据表 alembic_version，重新执行命令
python manage.py db upgrade 更新数据库保留数据库数据

4. 使用flask-sqlalchemy
join 关联查询
user = Users.query.join(
    Article,Artices.author_id == Users.id
).filter(Articles.id = qustion_id).first()

5. 消息闪现flask.flash：
.消息分类闪现，
后端：
flash('some messages','ok')
flash(’some other msgs, 'err')
前端渲染时:
{% for msg in get_flashes_messages(category_filter['ok'])  %} //只显示ok 的信息
{{ msg }}
{% endfor %}

6。使用钩子函数，
@before_request
@after_request
@