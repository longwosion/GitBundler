#! /usr/bin/env python
#coding=utf-8
import os
from gitcmd import GitCmd
from config import GitBundlerConfig

class GitBundlerServer(object):
    
    def __init__(self):
        config = GitBundlerConfig()
        self.url = config.get('server.upload.url', verbose=False)
        self.user = config.get('server.upload.user', verbose=False)
        self.password = config.get('server.upload.password', verbose=False)
            
    def pushbundle(self, bundlename, range=None):
        config = GitBundlerConfig()
        repo, filename, options, branch = config.get_serverbundle(bundlename)
        if repo and filename and options and branch:
            if range:
                options = range
            self.push(repo, filename, options, branch)
            
    def pushdir(self, path, range=None):
        config = GitBundlerConfig()
        repo, filename, options, branch = config.get_serverbundle_match(path)
        if repo and filename and options and branch:
            if range:
                options = range
            self.push(repo, filename, options, branch)
            
    def upload(self, file):
        from gitbundler.poster.encode import multipart_encode
        from gitbundler.poster.streaminghttp import register_openers
        
        import urllib2
        
        register_openers()
        
        if os.path.exists(file):
            print "  Uploading File:: %s" % file
            print "  Server:: %s" % self.url
            file = open(file, "rb")
            params = {'fileName': file}
            datagen, headers = multipart_encode(params)
            headers['gitbundler-user'] = self.user
            headers['gitbundler-password'] = self.password
            request = urllib2.Request(self.url, datagen, headers)
            result = urllib2.urlopen(request)
            print "  Upload:: %s" % result.read()
            file.close()
        else:
            print "error: cannot found upload file: %s." % file
        
    
    def push(self, repo, filename, options, branch):
        from gitbundler.poster.encode import multipart_encode
        from gitbundler.poster.streaminghttp import register_openers

        import urllib2

        register_openers()

        repo = os.path.abspath(repo)
        if not os.path.exists(repo):
            print "error: repo folder %s doesn't existed" %repo
            return
            
        print "Bundle> \n  File  :: %s, git: %s, %s" % (filename, repo, options)
    
        git = GitCmd(filename, repo, branch)
        print git.pull()
        print git.bundle_create(filename, options)
       
        if os.path.exists(os.path.join(repo, filename)):
            print "  Info  :: %s" % git.ls_remote(filename)
            print "  Server:: %s" % self.url
            file = open(os.path.join(repo, filename), "rb")
            params = {'fileName': file}
            datagen, headers = multipart_encode(params)
            headers['gitbundler-user'] = self.user
            headers['gitbundler-password'] = self.password
            request = urllib2.Request(self.url, datagen, headers)
            result = urllib2.urlopen(request)
            print "  Upload:: %s" % result.read()
            file.close()
            os.unlink(os.path.relpath(os.path.join(repo, filename)))
        else:
            print "error: generate git bundle fails."


class GitBundlerClient(object):
    
    def __init__(self):
        config = GitBundlerConfig()
        self.url = config.get('client.download.url', verbose=False)
        self.user = config.get('client.download.user', verbose=False)
        self.password = config.get('client.download.password', verbose=False)
        
    def pullbundle(self, bundlename):
        config = GitBundlerConfig()
        repo, filename, branch = config.get_clientbundle(bundlename)
        if repo and filename and branch:
            self.pull(repo, filename, branch)
            
    def pulldir(self, path):
        config = GitBundlerConfig()
        repo, filename, branch = config.get_clientbundle_match(path)
        if repo and filename and branch:
            self.pull(repo, filename, branch)
            
    def download(self, filename):
        import os
        import urllib2
        
        fileurl = '%s%s' % (self.url, filename)
        print "  Downloading File:: %s" % file
        print "  Server:: %s" % self.url
        headers = {}
        headers['gitbundler-user'] = self.user
        headers['gitbundler-password'] = self.password
        
        request = urllib2.Request(fileurl, None, headers)
        server = urllib2.urlopen(request)
        bundle = open(filename, 'wb')
        bundle.write(server.read())
        bundle.close()
        server.close()
        
        if os.path.exists(filename):
            print "  Download %s successfully"  % filename
        else:
            print "error: download file %s fails." % filename
        
    
    def pull(self, repo, filename, branch):
        import os
        import urllib2
        
        git = GitCmd(filename, repo, branch)
        fileurl = '%s%s' % (self.url, filename)
        print 'Downloading %s' % fileurl
        
        headers = {}
        headers['gitbundler-user'] = self.user
        headers['gitbundler-password'] = self.password
        
        request = urllib2.Request(fileurl, None, headers)
        server = urllib2.urlopen(request)
        bundle = open(os.path.join(repo, filename), 'wb')
        bundle.write(server.read())
        bundle.close()
        server.close()
        
        if os.path.exists(os.path.join(repo, filename)):
            print "  Info  :: %s" % git.ls_remote(filename)
            print "  Server:: %s" % self.url
            print git.pull_bundle(filename)
            #os.unlink(os.path.relpath(os.path.join(repo, filename)))
        else:
            print "error: git bundle download fails."
        
        

