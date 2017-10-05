#!/bin/env python

from bottle import default_app, get, post, template, request, static_file, redirect, abort
import os
from subprocess import call
import argparse
import tempfile
import sys
import logging

log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)

# need to parse args right away because decorators depend on args
prefix = None
s3_bucket = None
parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, help="port to listen on")
parser.add_argument("--s3_bucket", help="S3 bucket to sync with")
parser.add_argument("--prefix", help="Prefix to also serve webpage at, i.e. www.example.com and www.example.com/prefix/")
args = parser.parse_args()
if not args.port:
    args.port = 6969
if args.s3_bucket:
    import boto3
    s3_bucket = args.s3_bucket
if args.prefix:
    if not args.prefix.startswith('/'):
        args.prefix = '/' + args.prefix
    if args.prefix.endswith('/'):
        args.prefix = args.prefix[:-1]
    prefix = args.prefix
else:
    prefix = '/poboys'

platforms = ['noarch', 'linux-64', 'win-64', 'osx-64']


def ensure_pkgs_dir_exists():
    try: 
        os.makedirs('pkgs')
    except OSError:
        if not os.path.isdir('pkgs'):
            raise

    return 'pkgs'


def ensure_platform_dir_exists(platform):
    pkgs_dir = ensure_pkgs_dir_exists()
    platform_dir = os.path.join(pkgs_dir, platform)

    try: 
        if platform not in platforms:
            abort(404, "Invalid platform %s" % platform)
        os.makedirs(platform_dir)
    except OSError:
        if not os.path.isdir(platform_dir):
            raise

    return platform_dir


def reindex_platform_dir(platform_dir):
    savedir = os.getcwd()
    os.chdir(platform_dir)
    call(["conda", "index"])
    os.chdir(savedir)
    return ['repodata.json', 'repodata.json.bz2', '.index.json']


@get('/')
@get(prefix + '/')
def index():
    return template('index', prefix=prefix, platforms=platforms)


@post('/upload')
@post(prefix + '/upload')
def do_upload():
    platform = request.forms.get('platform')
    fileupload = request.files.get('fileupload')
    filename = fileupload.filename

    platform_dir = ensure_platform_dir_exists(platform)

    fileupload.save(platform_dir, overwrite=False) 
    index_filenames = reindex_platform_dir(platform_dir)

    # upload to S3 if requested
    if s3_bucket:
        try:
            s3 = boto3.resource('s3')
            with open(os.path.join(platform_dir, filename), 'rb') as f:
                s3.Object(s3_bucket, os.path.join(platform, filename)).put(Body=f)
            for index_filename in index_filenames:
                with open(os.path.join(platform_dir, index_filename), 'rb') as f:
                    s3.Object(s3_bucket, os.path.join(platform, index_filename)).put(Body=f)
        except Exception as e:
            # something went wrong.  Undo everything and bail
            os.remove(os.path.join(platform_dir, filename))
            reindex_platform_dir(platform_dir)
            abort(503, "Failed to upload to S3 %s with exception %s" % (s3_bucket, str(e)))

    redirect(prefix + '/pkgs/' + platform)


@get('/pkgs')
@get(prefix + '/pkgs')
def get_pkgs():
    pkgs_dir = ensure_pkgs_dir_exists()
    filelist = sorted([ f for f in os.listdir(pkgs_dir) ])
    return template('filelist_to_links', header='Current Platforms', prefix=prefix, parenturl='/pkgs', filelist=filelist, allow_delete=False)


@get('/pkgs/<platform>')
@get(prefix + '/pkgs/<platform>')
def get_platform(platform):
    if not platform in platforms:
        return "Unknown platform " + platform

    platform_dir = ensure_platform_dir_exists(platform)

    filelist = sorted([ f for f in os.listdir(platform_dir) ])
    return template('filelist_to_links', header='Packages', prefix=prefix, parenturl='/pkgs/'+platform, filelist=filelist, allow_delete=True)


@get('/pkgs/<platform>/<filename>')
@get(prefix + '/pkgs/<platform>/<filename>')
def get_file(platform, filename):
    if not platform in platforms:
        return "Unknown platform " + platform

    platform_dir = ensure_platform_dir_exists(platform)

    return static_file(filename, root=platform_dir, download=filename)


@post('/delete/pkgs/<platform>/<filename>')
@post(prefix + '/delete/pkgs/<platform>/<filename>')
def del_file(platform, filename):
    if not platform in platforms:
        return "Unknown platform " + platform

    platform_dir = ensure_platform_dir_exists(platform)
    tempdir = tempfile.gettempdir()

    try:
        # move to a tempdir (in case we need to undo this)
        os.rename(os.path.join(platform_dir, filename), os.path.join(tempdir, filename))
    except OSError:
        pass

    index_filenames = reindex_platform_dir(platform_dir)

    # delete from S3 if requested
    if s3_bucket:
        try:
            s3 = boto3.resource('s3')
            s3.Object(s3_bucket, os.path.join(platform, filename)).delete()
            for index_filename in index_filenames:
                with open(os.path.join(platform_dir, index_filename), 'rb') as f:
                    s3.Object(s3_bucket, os.path.join(platform, index_filename)).put(Body=f)
        except Exception as e:
            # something went wrong.  Undo everything and bail
            os.rename(os.path.join(tempdir, filename), os.path.join(platform_dir, filename))
            reindex_platform_dir(platform_dir) 
            abort(503, "Failed to delete from S3 bucket %s with exception %s" % (s3_bucket, str(e)))

    # commit the delete
    os.remove(os.path.join(tempdir, filename))

    redirect(prefix + '/pkgs/' + platform)


if __name__ == '__main__':
    for platform in platforms:
        ensure_platform_dir_exists(platform)
        os.chdir('pkgs/'+platform)
        call(["conda", "index"])
        os.chdir('../../')

    app = default_app()

    log.info("Serving on port %d" % args.port)
    app.run(host='0.0.0.0', port=args.port, debug=True)
