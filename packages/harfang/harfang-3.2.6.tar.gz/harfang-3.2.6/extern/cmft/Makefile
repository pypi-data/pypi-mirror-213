#
# Copyright 2014-2015 Dario Manesku. All rights reserved.
# License: http://www.opensource.org/licenses/BSD-2-Clause
#

VS2008_DEVENV_DIR=C:\Program Files (x86)\Microsoft Visual Studio 9.0\Common7\IDE
VS2010_DEVENV_DIR=C:\Program Files (x86)\Microsoft Visual Studio 11.0\Common7\IDE
VS2012_DEVENV_DIR=C:\Program Files (x86)\Microsoft Visual Studio 11.0\Common7\IDE

ifeq ($(OS),Windows_NT)
	OS=windows
else
	UNAME := $(shell uname -s)
	ifeq ($(UNAME),Darwin)
		OS=darwin
	endif
	ifeq ($(UNAME),Linux)
		OS=linux
	endif
endif

GENIE=./dependency/bx/tools/bin/$(OS)/genie

export CMFT_WIN_CLANG_DIR_=$(subst \,\\,$(subst /,\,$(WIN_CLANG_DIR)))
export CMFT_WIN_MINGW_DIR_=$(subst \,\\,$(subst /,\,$(WIN_MINGW_DIR)))

.PHONY: all
all:
	$(GENIE) --file=scripts/main.lua xcode4
	$(GENIE) --file=scripts/main.lua vs2008
	$(GENIE) --file=scripts/main.lua vs2010
	$(GENIE) --file=scripts/main.lua vs2012
	$(GENIE) --file=scripts/main.lua vs2013
	$(GENIE) --file=scripts/main.lua vs2015
	$(GENIE) --file=scripts/main.lua --gcc=mingw-gcc gmake
	$(GENIE) --file=scripts/main.lua --gcc=linux-gcc gmake
	$(GENIE) --file=scripts/main.lua --gcc=osx       gmake

.PHONY: clean-projects
clean-projects:
	@echo Removing _projects folder.
	-@rm -rf _projects

.PHONY: clean-build
clean-build:
	@echo Removing _build folder.
	-@rm -rf _build

.PHONY: clean
clean: clean-build clean-projects

_projects/xcode4:
	$(GENIE) --file=scripts/main.lua xcode4

_projects/vs2008:
	$(GENIE) --file=scripts/main.lua vs2008
vs2008-debug32:
	"$(subst /,\\,$(VS2008_DEVENV_DIR))\devenv" _projects/vs2008/cmft.sln /Build "Debug|Win32"
vs2008-release32:
	"$(subst /,\\,$(VS2008_DEVENV_DIR))\devenv" _projects/vs2008/cmft.sln /Build "Release|Win32"
vs2008-debug64:
	"$(subst /,\\,$(VS2008_DEVENV_DIR))\devenv" _projects/vs2008/cmft.sln /Build "Debug|x64"
vs2008-release64:
	"$(subst /,\\,$(VS2008_DEVENV_DIR))\devenv" _projects/vs2008/cmft.sln /Build "Release|x64"
vs2008: vs2008-debug32 vs2008-release32 vs2008-debug64 vs2008-release64

_projects/vs2010:
	$(GENIE) --file=scripts/main.lua vs2010
vs2010-debug32:
	"$(subst /,\\,$(VS2010_DEVENV_DIR))\devenv" _projects/vs2010/cmft.sln /Build "Debug|Win32"
vs2010-release32:
	"$(subst /,\\,$(VS2010_DEVENV_DIR))\devenv" _projects/vs2010/cmft.sln /Build "Release|Win32"
vs2010-debug64:
	"$(subst /,\\,$(VS2010_DEVENV_DIR))\devenv" _projects/vs2010/cmft.sln /Build "Debug|x64"
vs2010-release64:
	"$(subst /,\\,$(VS2010_DEVENV_DIR))\devenv" _projects/vs2010/cmft.sln /Build "Release|x64"

_projects/vs2012:
	$(GENIE) --file=scripts/main.lua vs2012
vs2012-debug32:
	"$(subst /,\\,$(VS2012_DEVENV_DIR))\devenv" _projects/vs2012/cmft.sln /Build "Debug|Win32"
vs2012-release32:
	"$(subst /,\\,$(VS2012_DEVENV_DIR))\devenv" _projects/vs2012/cmft.sln /Build "Release|Win32"
vs2012-debug64:
	"$(subst /,\\,$(VS2012_DEVENV_DIR))\devenv" _projects/vs2012/cmft.sln /Build "Debug|x64"
vs2012-release64:
	"$(subst /,\\,$(VS2012_DEVENV_DIR))\devenv" _projects/vs2012/cmft.sln /Build "Release|x64"

_projects/vs2013:
	$(GENIE) --file=scripts/main.lua vs2013
vs2013-debug32:
	"$(subst /,\\,$(VS2013_DEVENV_DIR))\devenv" _projects/vs2013/cmft.sln /Build "Debug|Win32"
vs2013-release32:
	"$(subst /,\\,$(VS2013_DEVENV_DIR))\devenv" _projects/vs2013/cmft.sln /Build "Release|Win32"
vs2013-debug64:
	"$(subst /,\\,$(VS2013_DEVENV_DIR))\devenv" _projects/vs2013/cmft.sln /Build "Debug|x64"
vs2013-release64:
	"$(subst /,\\,$(VS2013_DEVENV_DIR))\devenv" _projects/vs2013/cmft.sln /Build "Release|x64"

_projects/vs2015:
	$(GENIE) --file=scripts/main.lua vs2015
vs2015-debug32:
	"$(subst /,\\,$(VS2015_DEVENV_DIR))\devenv" _projects/vs2015/cmft.sln /Build "Debug|Win32"
vs2015-release32:
	"$(subst /,\\,$(VS2015_DEVENV_DIR))\devenv" _projects/vs2015/cmft.sln /Build "Release|Win32"
vs2015-debug64:
	"$(subst /,\\,$(VS2015_DEVENV_DIR))\devenv" _projects/vs2015/cmft.sln /Build "Debug|x64"
vs2015-release64:
	"$(subst /,\\,$(VS2015_DEVENV_DIR))\devenv" _projects/vs2015/cmft.sln /Build "Release|x64"

_projects/gmake-linux:
	$(GENIE) --file=scripts/main.lua --gcc=linux-gcc gmake
linux-debug32: _projects/gmake-linux
	make -R -C _projects/gmake-linux config=debug32
linux-release32: _projects/gmake-linux
	make -R -C _projects/gmake-linux config=release32
linux-debug64: _projects/gmake-linux
	make -R -C _projects/gmake-linux config=debug64
linux-release64: _projects/gmake-linux
	make -R -C _projects/gmake-linux config=release64
linux: linux-debug32 linux-release32 linux-debug64 linux-release64

_projects/gmake-osx:
	$(GENIE) --file=scripts/main.lua --gcc=osx gmake
osx-debug32: _projects/gmake-osx
	make -R -C _projects/gmake-osx config=debug32
osx-release32: _projects/gmake-osx
	make -R -C _projects/gmake-osx config=release32
osx-debug64: _projects/gmake-osx
	make -R -C _projects/gmake-osx config=debug64
osx-release64: _projects/gmake-osx
	make -R -C _projects/gmake-osx config=release64
osx: osx-debug32 osx-release32 osx-debug64 osx-release64

#_projects/gmake-linux-clang:
#	$(GENIE) --file=scripts/main.lua --clang=linux-clang gmake
#linux-clang-debug32: _projects/gmake-linux-clang
#	make -R -C _projects/gmake-linux-clang config=debug32
#linux-clang-release32: _projects/gmake-linux-clang
#	make -R -C _projects/gmake-linux-clang config=release32
#linux-clang-debug64: _projects/gmake-linux-clang
#	make -R -C _projects/gmake-linux-clang config=debug64
#linux-clang-release64: _projects/gmake-linux-clang
#	make -R -C _projects/gmake-linux-clang config=release64
#linux-clang: linux-debug32 linux-release32 linux-debug64 linux-release64

#_projects/gmake-win-clang:
#	$(GENIE) --file=scripts/main.lua --clang=win-clang gmake
#win-clang-debug32: _projects/gmake-win-clang
#	make -R -C _projects/gmake-win-clang config=debug32
#win-clang-release32: _projects/gmake-win-clang
#	make -R -C _projects/gmake-win-clang config=release32
#win-clang-debug64: _projects/gmake-win-clang
#	make -R -C _projects/gmake-win-clang config=debug64
#win-clang-release64: _projects/gmake-win-clang
#	make -R -C _projects/gmake-win-clang config=release64
#win-clang: win-debug32 win-release32 win-debug64 win-release64

_projects/gmake-mingw-gcc:
	$(GENIE) --file=scripts/main.lua --gcc=mingw-gcc gmake
mingw-gcc-debug32: _projects/gmake-mingw-gcc
	make -R -C _projects/gmake-mingw-gcc config=debug32
mingw-gcc-release32: _projects/gmake-mingw-gcc
	make -R -C _projects/gmake-mingw-gcc config=release32
mingw-gcc-debug64: _projects/gmake-mingw-gcc
	make -R -C _projects/gmake-mingw-gcc config=debug64
mingw-gcc-release64: _projects/gmake-mingw-gcc
	make -R -C _projects/gmake-mingw-gcc config=release64
mingw: mingw-gcc-debug32 mingw-gcc-release32 mingw-gcc-debug64 mingw-gcc-release64
