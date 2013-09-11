#! /usr/bin/env python
#coding=utf-8

import os, sys
import re
import time
sys.path.insert(0, '.')
from commands import call, register_command, Command, get_answer, get_input
from optparse import make_option
import logging

__author__ = 'Eric SHI'
__author_email__ = 'longwosion@gmail.com'
__license__ = 'BSD'
__prog_name__ = 'gitb'
version = __version__ = '0.0.1'

class ConfigCommand(Command):
    name = 'config'
    has_options = True
    option_list = (
        make_option('-l', '--list', action="store_true", dest="list", help='list all'),
        make_option('--import', action="store", dest="configFile", help='clear & import config items from file'),
        make_option('--export', action="store", dest="exportFile", help='export config items to file'),
        make_option('--add', action="store_true", dest="add", help='adds a new config item: name value'),
        make_option('--get', action="store_true", dest="get", help='get value: name'),
        make_option('--unset', action="store_true", dest="unset", help='removes a config item: name'),
        make_option('--remove-section', action="store_true", dest="remove_section", help='remove a section: name'),
        
    )
    
    def handle(self, options, global_options, *args):
        from config import GitBundlerConfig
        config = GitBundlerConfig()
        
        if options.list:
            return config.list_all()
        elif options.add:
            if len(args) == 2:
                return config.add(args[0], args[1])
        elif options.get:
            if len(args) == 1:
                return config.get(args[0])
        elif options.unset:
            if len(args) == 1:
                return config.unset(args[0])
        elif options.remove_section and len(args) == 1:
            return config.remove_section(args[0])
        elif options.configFile:
            return config.import_file(options.configFile)
        elif options.exportFile:
            return config.export_file(options.exportFile)
            
        self.print_help(__prog_name__, self.name)
        
class PushCommand(Command):
    name = 'push'
    help = 'Create git bundle file and upload it to transfer server'
    has_options = True
    option_list = (
        make_option('-b', '--bundle', action="store", dest="bundle", help='server bundle name'),
        make_option('--range', action="store", dest="range", help="bundle range, such as 10days, 10.hours, 1.weeks"),
        make_option('--loop', action="store_true", dest="loop", help='upload bundle repeatly'),
    )
    
    def handle(self, options, global_options, *args):
        from config import GitBundlerConfig
        from server import GitBundlerServer
        config = GitBundlerConfig()
        
        while 1:
            run_flag = 0
            if options.bundle:
                server = GitBundlerServer()
                if server:
                    server.pushbundle(options.bundle, range=options.range)
                    run_flag = 1
            else:
                server = GitBundlerServer()
                if server:
                    path = os.getcwd()
                    server.pushdir(path, range=options.range)
                    run_flag = 1
            
            if run_flag == 0:
                return self.print_help(__prog_name__, self.name)
            else:
                if not options.loop:
                    return 
                else:
                    time.sleep(int(config.get('server.loop.interval', verbose=False) or 100))

class PullCommand(Command):
    name = 'pull'
    help = 'Download git bundle file from transfer server and merge to local work-tree'
    has_options = True
    option_list = (
        make_option('-b', '--bundle', action="store", dest="bundle", help='client bundle name'),
        make_option('--branch', action="store", dest="force_branch", help='force branch for creating local branch'),
    )
    
    def handle(self, options, global_options, *args):
        from config import GitBundlerConfig
        from server import GitBundlerClient
        config = GitBundlerConfig()
        
        client = GitBundlerClient()
        if client:
            if options.bundle:
                return client.pullbundle(options.bundle, force_branch=options.force_branch)
            else:
                path = os.getcwd()
                return client.pulldir(path, force_branch=options.force_branch)
            
        self.print_help(__prog_name__, self.name)
    
class UploadCommand(Command):
    name = 'upload'
    args = '<file1> <file2> ...'
    def handle(self, options, global_options, *args):
        from config import GitBundlerConfig
        from server import GitBundlerServer
        config = GitBundlerConfig()
        
        if len(args) >= 1:
            server = GitBundlerServer()
            if server:
                for filename in args:
                    server.upload(filename)
            return
                
        self.print_help(__prog_name__, self.name)
    
class DownloadCommand(Command):
    name = 'download'
    args = '<file1> <file2> ...'
    def handle(self, options, global_options, *args):
        from config import GitBundlerConfig
        from server import GitBundlerClient
        config = GitBundlerConfig()
        
        if len(args) >= 1:
            client = GitBundlerClient()
            if client:
                for filename in args:
                    client.download(filename)
            return 
        self.print_help(__prog_name__, self.name)
        
class LocalPullCommand(Command):
    name = 'lpull'
    args = '<remote> <remote_branch> ...'
    has_options = True
    option_list = (
        make_option('-b', '--bundle', action="store", dest="bundle", help='server bundle name'),
    )
    
    def handle(self, options, global_options, *args):
        from config import GitBundlerConfig
        from server import GitBundlerServer
        config = GitBundlerConfig()
        
        server = GitBundlerServer()
        path = path = os.getcwd()
        
        if server and server.guess_bundle(name=options.bundle, path=path):
            if len(args) == 2:
                server.lpush(args[0], branch=args[1])

            if len(args) == 1:
                server.lpush(args[0])
                
            if len(args) == 0:
                server.lpush('local')

register_command(ConfigCommand)
register_command(PushCommand)
register_command(PullCommand)    
register_command(UploadCommand)    
register_command(DownloadCommand)  
register_command(LocalPullCommand)  

def main():
    modules = []
    call(__prog_name__, __version__, modules)
    
if __name__ == '__main__':
    main()