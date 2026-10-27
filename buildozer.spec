[app]
title = 今天吃什么
package.name = fooddraw
package.domain = org.fooddraw

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,otf,ttf
source.exclude_dirs = .venv,bin,__pycache__,.git

version = 0.1

requirements = python3,kivy==2.3.1

orientation = portrait
fullscreen = 0

android.permissions =
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.debug_artifact = apk