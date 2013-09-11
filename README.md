GitBundler
==========

A command tool for accessing git in private network by 
transferring git bundle file in middle server

# Usage

## Server
```
gitb push
gitb push -b uliweb
gitb push --range 10days
```

ʵ��ִ�еĲ�����
* ��ȡ��ǰ��֧��������<master>
* git pull
* git bundle create <filename> --since=<days> <master>

```
gitb lpull <remote> <branch>
gitb lpull
gitb lpull local
gitb lpull local req
```

ʵ��ִ�еĲ�����
* git checkout local
* git pull local req

<remote>ȱʡ��local,  <branch>ȱʡ�ǵ�ǰ��֧

## Client
```
gitb pull
gitb pull -b uliweb
gitb pull --branch req (��һ��ʹ�ã�����û��req��֧)
```

ʵ��ִ�еĲ�����
* ��ȡ��ǰ��֧��������req
* ���req��֧�����ڣ�ִ�� git pull ctasks2days req:req
* ���req��֧���ڣ�ִ�� 
    * git checkout req
    * git pull ctasks2days req

## Other
```
gitb upload file.name.zip
gitb download file.name.zip
```

