### RSS Factory

***

demo:<https://weiborss.rhcloud.com>

RSS Factory 是用于生成 微博 RSS 的Web APP.  

demo服务搭建在OpenShift上，搭建步骤参考以下链接：  
1.搭建OpenShift Tornado DIY环境 
> <http://bozpy.sinaapp.com/blog/29>

2.在OpenShift上安装memcached 
> <http://www.blackglory.me/openshift-install-wordpress-memcached/>

```shell
# 启动memcached  
$OPENSHIFT_DATA_DIR/bin/memcached -l $OPENSHIFT_DIY_IP -p 15211 -d  
# 获取pid用于停止服务  
ps -ef|grep memcached
```
3.安装Python依赖库
```shell
pip install -r requirements.txt
```
4.git push RSS Factory的代码
