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

实际执行的操作：
* 读取当前分支。比如是<master>
* git pull
* git bundle create <filename> --since=<days> <master>

```
gitb lpull <remote> <branch>
gitb lpull
gitb lpull local
gitb lpull local req
```

实际执行的操作：
* git checkout local
* git pull local req

<remote>缺省是local,  <branch>缺省是当前分支

## Client
```
gitb pull
gitb pull -b uliweb
gitb pull --branch req (第一次使用，本地没有req分支)
```

实际执行的操作：
* 读取当前分支。比如是req
* 如果req分支不存在，执行 git pull ctasks2days req:req
* 如果req分支存在，执行 
    * git checkout req
    * git pull ctasks2days req

## Other
```
gitb upload file.name.zip
gitb download file.name.zip
```

