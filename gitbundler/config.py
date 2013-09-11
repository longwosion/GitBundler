#! /usr/bin/env python
#coding=utf-8

from ConfigParser import ConfigParser
import os

path = os.path.dirname(__file__)
DEFAULT_CONFIG_FILE = os.path.join(path, 'gitbundler.ini')
DEFATUL_SECTION = 'global'

class GitBundlerConfig(object):
    
    def __init__(self):
        self.reload()
        
    def import_file(self, config_file):
        self.config = ConfigParser()
        if os.path.exists(config_file):
            self.config.read(config_file)
            self.save()
            print "import %s successfully." % config_file
            self.list_all()
        else:
            print "error: import file %s doesn't exist." % config_file
            
    def export_file(self, export_file):
        self.reload()
        configfile = open(export_file, 'wb')
        self.config.write(configfile)
        
    def reload(self):
        self.config = ConfigParser()
        if os.path.exists(DEFAULT_CONFIG_FILE):
            self.config.read(DEFAULT_CONFIG_FILE)
        
    def save(self):
        configfile = open(DEFAULT_CONFIG_FILE, 'wb')
        self.config.write(configfile)
        
    def __items(self, show_section=True):
        config = self.config
        for section in config.sections():
            for key, value in config.items(section):
                if show_section:
                    yield section, key, value
                else:
                    yield "%s.%s" %(section, key), value
                
    def __print_one_item(self, section, key, value, indent=""):
        if section:
            print "%s%s.%s=%s" % (indent, section, key, value)
        else:
            print "%s%s=%s" % (indent, key, value)

    def __parse_section(self, key):
        if key.find(".") != -1:
            section = key.split(".")[0]
            key = ".".join(key.split(".")[1:])
        else:
            section = DEFATUL_SECTION
        return section, key
                
    def list_all(self):
        config = self.config
        mapping = {}
        for section in config.sections():
            print "[%s]" % section
            for key, value in config.items(section):
                split_data = key.split(".")
                if split_data[0] == "bundles":
                    mapping_key = "%s.%s" % (section, ".".join(split_data[:2]))
                    if not mapping.has_key(mapping_key):
                        print ""
                        print "  # %s" % split_data[1]
                        mapping[mapping_key] = True
                    self.__print_one_item(None, key, value, indent="  ")
                else:
                    self.__print_one_item(section, key, value, indent="  ")
            print ""

    def add(self, key, value):
        section, key = self.__parse_section(key)
        
        if not self.config.has_section(section):
            self.config.add_section(section)
            
        self.config.set(section, key, value)
        self.save()
        
    def get(self, key, verbose=True):
        section, key = self.__parse_section(key)
        if self.config.has_option(section, key):
            if verbose:
                self.__print_one_item(section, key, self.config.get(section, key))
            return self.config.get(section, key)
        return None
            
    def unset(self, key):
        section, key = self.__parse_section(key)
        if self.config.has_option(section, key):
            self.config.remove_option(section, key)
        
    def remove_section(self, match_key):
        for key, value in self.__items(show_section=False):
            if key.startswith(match_key):
                section, key = self.__parse_section(key)
                self.config.remove_option(section, key)
        self.save()
        
    def get_serverbundle(self, bundle):
        repo = self.get('server.bundles.%s.repo' % bundle, verbose=False)
        filename = self.get('server.bundles.%s.filename' % bundle, verbose=False)
        options = self.get('server.bundles.%s.options' % bundle, verbose=False)
        branch = self.get('server.bundles.%s.branch' % bundle, verbose=False)
        if not (repo and filename and options and branch):
            print "error: can not find server bundle with name %s" % bundle
        
        return (repo, filename, options, branch)
    
    def get_serverbundle_match(self, path):
        for key, value in self.__items(show_section=False):
            if key.startswith('server.bundles') and key.endswith('.repo'):
                value = self.get(key, verbose=False)
                if os.path.abspath(path).upper() == os.path.abspath(value).upper():
                    bundle = key.split(".")[2]
                    return self.get_serverbundle(bundle)
        print "error: can not find server bundle match current path %s" % path                
        return (None, None, None, None)
        
    def get_clientbundle(self, bundle):
        repo = self.get('client.bundles.%s.repo' % bundle, verbose=False)
        filename = self.get('client.bundles.%s.filename' % bundle, verbose=False)
        branch = self.get('client.bundles.%s.branch' % bundle, verbose=False)
        if not (repo and filename and branch):
            print "error: can not find client bundle with name %s" % bundle
        
        return (repo, filename, branch)
    
    def get_clientbundle_match(self, path):
        for key, value in self.__items(show_section=False):
            if key.startswith('client.bundles') and key.endswith('.repo'):
                value = self.get(key, verbose=False)
                if os.path.abspath(path).upper() == os.path.abspath(value).upper():
                    bundle = key.split(".")[2]
                    return self.get_clientbundle(bundle)
        print "error: can not find client bundle match current path %s" % path                
        return (None, None, None)
