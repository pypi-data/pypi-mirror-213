#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os

os.system("rm -r ../windows_installer/emid")

ver_to_build = input("Version to build: ")
os.system("tar -xvf ../dist/emid-"+ver_to_build+".tar.gz --directory ../windows_installer/")
os.system("mv ../windows_installer/emid-"+ver_to_build+ " ../windows_installer/emid")

os.chdir("../windows_installer/emid")

os.system("wine cmd /c python setup_cx.py build")

os.system("rsync -r ./build/exe.win-amd64-3.11/lib/emid/doc/ ./build/exe.win-amd64-3.11/doc/")
#os.system("rsync -r ./build/exe.win-amd64-3.11/lib/emid/sounds/ ./build/exe.win-amd64-3.11/sounds/")


os.system("/usr/bin/bash ../../prep-release/win_launch_iss_compiler.sh")
