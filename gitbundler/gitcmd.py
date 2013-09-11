#! /usr/bin/env python
#coding=utf-8

import os, sys
from subprocess import Popen, PIPE

class GitCmd(object):
    def __init__(self, name, path, branch):
        self.name = name
        self.path = path
        self.branch = branch
        
    def _exec(self, cmd):
        cmd = 'git %s' % str(cmd)
        print "gitcmd> %s" % cmd
        #in_, out_, err_ = os.popen3(cmd, 't', cwd=self.path)
        
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, cwd=self.path)
        out_, err_ = p.stdout, p.stderr
        p.wait()
        return out_, err_
    
    def pull(self):
        stdout, errout = self._exec('pull')
        errorstr = errout.read().strip()
        print errorstr
        return stdout.read().strip()
    
    def pull_bundle(self, bundle):
        stdout, errout = self._exec('pull %s %s' % (bundle, self.branch))
        errorstr = errout.read().strip()
        print errorstr
        return stdout.read().strip()
    
    def get_head(self):
        stdout, errout = self._exec('rev-parse "%s"' % self.branch)
        return stdout.read().strip()

    def rev(self, commit='HEAD'):
        if commit == 'HEAD':
            return self.get_head()
        stdout, errout = self._exec('rev-parse "%s"' % commit)
        return stdout.read().strip()
    
    def bundle_create(self, bundle_file, option):
        stdout, errout = self._exec('bundle create %s --since=%s %s' %(bundle_file, option, self.branch))
        errorstr = errout.read().strip()
        print errorstr
        return stdout.read().strip()
    
    def ls_remote(self, bundle_file):
        stdout, errout = self._exec('ls-remote %s' % bundle_file)
        return stdout.read().strip()
        
