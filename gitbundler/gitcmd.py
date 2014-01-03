#! /usr/bin/env python
#coding=utf-8

import os, sys
from subprocess import Popen, PIPE

class GitCmd(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.branch = "master"
        
    def _exec(self, cmd, console=True):
        cmd = 'git %s' % str(cmd)
        if console:
            cmdline = cmd
            width = 74
            if len(cmdline) > width:
                print "git> %s" % cmdline[0:width]
                cmdline = cmdline[width:]
                while len(cmdline) > width-2:
                    print " . >   %s" % cmdline[0:width-2]
                    cmdline = cmdline[width-2:]
                print " . >   %s" % cmdline
            else:
                print "git> %s" % cmdline
                
        #in_, out_, err_ = os.popen3(cmd, 't', cwd=self.path)
        
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, cwd=self.path)
        out_, err_ = p.stdout, p.stderr
        p.wait()
        return out_, err_
    
    def execute(self, cmd):
        stdout, errout = self._exec(cmd)
        errorstr = errout.read().strip()
        print errorstr
        return stdout.read().strip()
    
    def existed_branch(self, match_branch):
        stdout, errout = self._exec('branch', console=False)
        errorstr = errout.read().strip()
        
        branch_list = stdout.read().strip().split("\n")
        
        for branch in branch_list:
            if branch.startswith("* "):
                branch = branch.replace("* ", "")
            branch = branch.strip()
            if match_branch == branch:
                return True
            
        return False
        
    
    def get_branch(self):
        stdout, errout = self._exec('branch')
        errorstr = errout.read().strip()
        
        branch_list = stdout.read().strip()
        print branch_list
        branch_list = branch_list.split("\n")
        
        for branch in branch_list:
            if branch.startswith("* "):
                current_branch = branch.replace("* ", "")
                print "  Current  :: %s" % current_branch
                self.branch = current_branch
                self.current_branch = current_branch
                return current_branch
        
        print "  Current  :: master"
        return "master"
    
    def get_filelist(self, commit):
        stdout, errout = self._exec('diff-tree -r -c --no-commit-id --diff-filter=AMR --name-only %s' % commit)
        filelist = stdout.read().splitlines()
        
        if filelist:
            print " Files in commit %s:" % commit
            for f in filelist:
                print " * %s" % f
            print ""
        else:
            print "[ERROR] There are no files in this commit %s" % commit
        return filelist
    
    def get_rev_parse(self, commit):
        stdout, errout = self._exec('rev-parse --verify -q %s' % commit)
        rev = stdout.read().splitlines()
        if rev:
            print " Revision %s\n" % rev
            return rev[0]
        else:
            print "[ERROR] Needed a single commit revision"
            return None
    
    def archive(self, commit, output):
        rev = self.get_rev_parse(commit)
        if rev:
            if not output:
                output = "update-%s.zip" % rev[0:8]
            files = self.get_filelist(rev)
            if files:
                stdout, errout = self._exec('archive --format zip -9 -o %s %s %s' % (output, rev, ' '.join(files)))
                errorstr = errout.read().strip()
                print errorstr
                return stdout.read().strip()
    
    def set_force_branch(self, branch):
        if branch and self.branch != branch:
            print "  Reset current  :: %s" % branch
            self.branch = branch
    
    def checkout(self, branch):
        stdout, errout = self._exec('checkout %s' % branch)
        errorstr = errout.read().strip()
        print errorstr
        return stdout.read().strip()
    
    def pull(self):
        stdout, errout = self._exec('pull -v')
        errorstr = errout.read().strip()
        print errorstr
        return stdout.read().strip()
    
    def pull_bundle(self, bundle):
        if self.existed_branch(self.branch):
            self.checkout(self.branch)
            stdout, errout = self._exec('pull %s %s' % (bundle, self.branch))
        else:
            stdout, errout = self._exec('fetch %s %s:%s' % (bundle, self.branch, self.branch))
            self.checkout(self.branch)
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
        
