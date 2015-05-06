#!/bin/env python

from bottle import get, post, run, template, request, static_file, redirect
import os
from subprocess import call
import argparse


platforms = ['noarch', 'linux-64', 'win-64', 'osx-64']


def ensure_pkgs_dir_exists():

    try: 
        os.makedirs('pkgs')
    except OSError:
        if not os.path.isdir('pkgs'):
            raise


def ensure_platform_dir_exists(platform):

    ensure_pkgs_dir_exists()

    try: 
        os.makedirs('pkgs/' + platform)
    except OSError:
        if not os.path.isdir('pkgs/' + platform):
            raise


@get('/')
def index():

    return template('index', platforms=platforms)


@post('/upload')
def do_upload():

    platform = request.forms.get('platform')
    filename = request.files.get('filename')

    ensure_platform_dir_exists(platform)

    filename.save('pkgs/'+platform, overwrite=True) 
    os.chdir('pkgs/'+platform)
    call(["conda", "index"])
    os.chdir('../../')
    redirect('/pkgs/'+platform)


@get('/pkgs')
def get_pkgs():

    ensure_pkgs_dir_exists()
    dirlist = [ f for f in os.listdir('pkgs') ]
    return template('dirlist_to_links', header='Current Platforms', parentdir='/pkgs', dirlist=dirlist, allow_delete=False)


@get('/pkgs/<platform>')
def get_platform(platform):

    if not platform in platforms:
        return "Unknown platform " + platform

    ensure_platform_dir_exists(platform)

    dirlist = [ f for f in os.listdir('pkgs/'+platform) ]
    return template('dirlist_to_links', header='Packages', parentdir='/pkgs/'+platform, dirlist=dirlist, allow_delete=True)


@get('/pkgs/<platform>/<filename>')
def get_file(platform, filename):

    if not platform in platforms:
        return "Unknown platform " + platform

    ensure_platform_dir_exists(platform)

    return static_file(filename, root='pkgs/'+platform, download=filename)


@post('/delete/pkgs/<platform>/<filename>')
def del_file(platform, filename):

    if not platform in platforms:
        return "Unknown platform " + platform

    ensure_platform_dir_exists(platform)

    try:
        os.remove('pkgs/'+platform+'/'+filename)
    except OSError:
        pass

    os.chdir('pkgs/'+platform)
    call(["conda", "index"])
    os.chdir('../../')
    redirect('/pkgs/'+platform)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, help="port to listen on")
    args = parser.parse_args()
    if not args.port:
        args.port = 6969
    

    for platform in platforms:
        ensure_platform_dir_exists(platform)
        os.chdir('pkgs/'+platform)
        call(["conda", "index"])
        os.chdir('../../')

    run(host='0.0.0.0', port=args.port, debug=True)
