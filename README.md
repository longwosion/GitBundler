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
* 读取当前分支。比如是[master]
* git pull
* git bundle create [filename] --since=[days] [master]

```
gitb lpull <remote> <branch>
gitb lpull
gitb lpull local
gitb lpull local req
```

实际执行的操作：
* git checkout req
* git pull local req

[remote]缺省是local,  [branch]缺省是当前分支

## Client
```
gitb pull
gitb pull -b uliweb
gitb pull --branch req (第一次使用，本地没有req分支)
```

实际执行的操作：
* 读取当前分支。比如是req
* 如果req分支不存在，执行 
    * git fetch ctasks2days req:req
    * git checkout req
* 如果req分支存在，执行 
    * git checkout req
    * git pull ctasks2days req
    
```
gitb archive HEAD
gitb archive -o archive.zip
```

实际执行的操作:
* 获取某个提交上的所有文件，打包形成zip文件。
* git diff-tree -r -c --no-commit-id --diff-filter=AMR --name-only [COMMIT_ID]
* git archive --format zip -9 -o update-20bf8aa5.zip 20bf8aa5 [file_list[


## Other
```
gitb upload file.name.zip
gitb download file.name.zip
```

