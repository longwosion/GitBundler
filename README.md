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
* ��ȡ��ǰ��֧��������[master]
* git pull
* git bundle create [filename] --since=[days] [master]

```
gitb lpull <remote> <branch>
gitb lpull
gitb lpull local
gitb lpull local req
```

ʵ��ִ�еĲ�����
* git checkout req
* git pull local req

[remote]ȱʡ��local,  [branch]ȱʡ�ǵ�ǰ��֧

## Client
```
gitb pull
gitb pull -b uliweb
gitb pull --branch req (��һ��ʹ�ã�����û��req��֧)
```

ʵ��ִ�еĲ�����
* ��ȡ��ǰ��֧��������req
* ���req��֧�����ڣ�ִ�� 
    * git fetch ctasks2days req:req
    * git checkout req
* ���req��֧���ڣ�ִ�� 
    * git checkout req
    * git pull ctasks2days req
    
```
gitb archive HEAD
gitb archive -o archive.zip
```

ʵ��ִ�еĲ���:
* ��ȡĳ���ύ�ϵ������ļ�������γ�zip�ļ���
* git diff-tree -r -c --no-commit-id --diff-filter=AMR --name-only [COMMIT_ID]
* git archive --format zip -9 -o update-20bf8aa5.zip 20bf8aa5 [file_list[


## Other
```
gitb upload file.name.zip
gitb download file.name.zip
```

