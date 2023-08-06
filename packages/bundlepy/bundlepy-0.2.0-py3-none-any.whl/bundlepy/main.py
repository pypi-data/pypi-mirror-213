#!/usr/bin/env python3
import glob
import multiprocessing
import os
import shutil
import sys

from contextlib import contextmanager

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from bundlepy.bundler_arguments import BundlerArguments
from bundlepy.remote_bundler import RemoteBundler
from bundlepy.bundler import Bundler
from bundlepy.venv_manager import VenvManager

def _build_remotes(args, remote_bundler):
    if args.all_targets:
        remote_bundler.bundle_app("windows")
        remote_bundler.bundle_app("linux")
        remote_bundler.bundle_app("osx")
        return
    if args.windows:
        remote_bundler.bundle_app("windows")
    if args.linux:
        remote_bundler.bundle_app("linux")
    if args.osx:
        remote_bundler.bundle_app("osx")

def is_remote(args) -> bool:
    return any([args.windows, args.osx, args.all_targets, args.linux])

def main():
    bundler_arg_parser = BundlerArguments()
    bundler_arg_parser.parse_arguments()
    packages = []
    transitive_imports = []
    if bundler_arg_parser.parsed_args.packages_file: 
        with open(bundler_arg_parser.parsed_args.packages_file, "r") as bund:
            packages = [package.strip() for package in bund.readlines()]
    elif bundler_arg_parser.parsed_args.packages:
        packages = bundler_arg_parser.parsed_args.packages
    
    if bundler_arg_parser.parsed_args.transitive_imports_file:
        with open(bundler_arg_parser.parsed_args.transitive_imports_file, "r") as imports:
            transitive_imports = [transitive_import.strip() for transitive_import in imports.readlines()]

    if not is_remote(bundler_arg_parser.parsed_args):
        bundler = Bundler(os.path.join(os.getcwd(), bundler_arg_parser.parsed_args.app),
                                packages, transitive_imports)
        bundler.bundle_app()
    else:
        remote_bundler = RemoteBundler(bundler_arg_parser.parsed_args.project_dir, packages, transitive_imports,
                                       bundler_arg_parser.parsed_args.app,
                                       bundler_arg_parser.parsed_args.cluster_conf_file)
        args = bundler_arg_parser.parsed_args
        _build_remotes(args, remote_bundler)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    sys.exit(main())
