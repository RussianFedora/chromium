# NEVER EVER EVER turn this on in official builds
%global freeworld 0

# gn is the new new new buildtool. *sigh*
%global use_gn 0

# Leave this alone, please.
%global target out/Release

# %%{nil} for Stable; -beta for Beta; -dev for Devel
# dash in -beta and -dev is intentional !
%global chromium_channel %{nil}
%global chromium_browser_channel chromium-browser%{chromium_channel}
%global chromium_path %{_libdir}/chromium-browser%{chromium_channel}
%global crd_path %{_libdir}/chrome-remote-desktop
%global tests 0

# We don't want any libs in these directories to generate Provides
# Requires is trickier. 
%global __provides_exclude_from %{chromium_path}/.*\\.so|%{chromium_path}/lib/.*\\.so
%global privlibs libaccessibility|libaura_extra|libaura|libbase_i18n|libbase|libblink_common|libblink_platform|libblink_web|libboringssl|libbrowser_ui_views|libcaptive_portal|libcapture|libcc_blink|libcc_ipc|libcc_proto|libcc|libcc_surfaces|libchromium_sqlite3|libcloud_policy_proto_generated_compile|libcloud_policy_proto|libcompositor|libcontent|libcrcrypto|libdbus|libdevice_battery|libdevice_bluetooth|libdevice_core|libdevice_event_log_component|libdevice_gamepad|libdevice_power_save_blocker|libdevice_vibration|libdisplay_compositor|libdisplay|libdisplay_types|libdisplay_util|libdomain_reliability|libEGL|libevents_base|libevents_devices|libevents_devices_x11|libevents_ipc|libevents_ozone_layout|libevents_platform|libevents|libevents_x|libffmpeg|libgcm_driver_common|libgcm|libgesture_detection|libgfx_geometry|libgfx_ipc_geometry|libgfx_ipc_skia|libgfx_ipc|libgfx_range|libgfx|libgfx_vector_icons|libgfx_x11|libgin|libgles2_c_lib|libgles2_implementation|libgles2_utils|libGLESv2|libgl_init|libgl_wrapper|libgpu|libgtk2ui|libicui18n|libicuuc|libipc_mojo|libipc|libkeyboard|libkeyboard_with_content|libkeycodes_x11|libkeyed_service_content|libkeyed_service_core|libmedia_blink|libmedia_gpu|libmedia|libmessage_center|libmidi|libmodules|libmojo_common_lib|libmojo_geometry_lib|libmojo_public_system|libmojo_system_impl|libnative_theme|libnet|libnet_with_v8|libonc_component|libplatform_handle|libpolicy_component|libppapi_host|libppapi_proxy|libppapi_shared|libprefs|libprinting|libprotobuf_lite|libproxy_config|libsandbox_services|libscheduler|libseccomp_bpf_helpers|libseccomp_bpf|libsessions_content|libshared_memory_support|libshell_dialogs|libskia|libsnapshot|libsql|libstorage_common|libstorage|libsuid_sandbox_client|libsurface|libsync_core|libsync_proto|libtracing|libtranslator|libui_base_ime|libui_base|libui_base_x|libui_data_pack|libui_touch_selection|liburl_ipc|liburl_lib|liburl_matcher|libuser_prefs|libv8|libviews|libwallpaper|libwebcore_shared|libwebdata_common|libweb_dialogs|libwebview|libwm|libwtf|libx11_events_platform
%global __requires_exclude ^(%{privlibs})\\.so

# Try to not use the Xvfb as it is slow..
%global tests_force_display 0
# If we build with shared on, then chrome-remote-desktop depends on chromium libs.
# If we build with shared off, then users cannot swap out libffmpeg (and i686 gets a lot harder to build)
%global shared 1
# We should not need to turn this on. The app in the webstore _should_ work.
%global build_remoting_app 0

# AddressSanitizer mode
# https://www.chromium.org/developers/testing/addresssanitizer
%global asan 0

# Only flip this on if stuff is really broken re: nacl.
# chromium-native_client doesn't build on Fedora 23 because
# clang is too old and buggy.
%if 0%{?fedora} <= 23
%global killnacl 1
%else
%global killnacl 0
%endif

%if 0%{?killnacl}
 %global nacl 0
 %global nonacl 1
%else
# TODO: Try arm (nacl disabled)
%if 0%{?fedora}
 %ifarch i686
 %global nacl 0
 %global nonacl 1
 %else
 %global nacl 1
 %global nonacl 0
 %endif
%endif
%endif

%if 0
# Chromium's fork of ICU is now something we can't unbundle.
# This is left here to ease the change if that ever switches.
BuildRequires:  libicu-devel >= 5.4
%global bundleicu 0
%else
%global bundleicu 1
%endif

%global bundlere2 1

# Chromium breaks on wayland, hidpi, and colors with gtk3 enabled.
%global gtk3 0

%if 0%{?rhel} == 7
%global bundleopus 1
%global bundlelibusbx 1
%global bundleharfbuzz 1
%else
%global bundleharfbuzz 0
%global bundleopus 0
%global bundlelibusbx 0
%endif

### Google API keys (see http://www.chromium.org/developers/how-tos/api-keys)
### Note: These are for Fedora use ONLY.
### For your own distribution, please get your own set of keys.
### http://lists.debian.org/debian-legal/2013/11/msg00006.html
%global api_key AIzaSyDUIXvzVrt5OkVsgXhQ6NFfvWlA44by-aw
%global default_client_id 449907151817.apps.googleusercontent.com
%global default_client_secret miEreAep8nuvTdvLums6qyLK
%global chromoting_client_id 449907151817-8vnlfih032ni8c4jjps9int9t86k546t.apps.googleusercontent.com 

Name:		chromium%{chromium_channel}
Version:	53.0.2785.143
Release:	1%{?dist}
Summary:	A WebKit (Blink) powered web browser
Url:		http://www.chromium.org/Home
License:	BSD and LGPLv2+ and ASL 2.0 and IJG and MIT and GPLv2+ and ISC and OpenSSL and (MPLv1.1 or GPLv2 or LGPLv2)

### Chromium Fedora Patches ###
Patch0:		chromium-46.0.2490.71-gcc5.patch
Patch1:		chromium-45.0.2454.101-linux-path-max.patch
Patch2:		chromium-50.0.2661.86-addrfix.patch
# Google patched their bundled copy of icu 54 to include API functionality that wasn't added until 55.
# :P
Patch3:		chromium-52.0.2723.2-system-icu-54-does-not-have-detectHostTimeZone.patch
Patch4:		chromium-46.0.2490.71-notest.patch
# In file included from ../linux/directory.c:21:
# In file included from ../../../../native_client/src/nonsfi/linux/abi_conversion.h:20:
# ../../../../native_client/src/nonsfi/linux/linux_syscall_structs.h:44:13: error: GNU-style inline assembly is disabled
#     __asm__ __volatile__("mov %%gs, %0" : "=r"(gs));
#             ^
# 1 error generated.
Patch6:		chromium-47.0.2526.80-pnacl-fgnu-inline-asm.patch
# Ignore broken nacl open fd counter
Patch7:		chromium-47.0.2526.80-nacl-ignore-broken-fd-counter.patch
# Use libusb_interrupt_event_handler from current libusbx (1.0.21-0.1.git448584a)
Patch9:		chromium-48.0.2564.116-libusb_interrupt_event_handler.patch
# Fix re2 unbundle gyp
Patch10:	chromium-50.0.2661.94-unbundle-re2-fix.patch
# Ignore deprecations in cups 2.2
# https://bugs.chromium.org/p/chromium/issues/detail?id=622493
Patch12:	chromium-52.0.2743.82-cups22.patch
# Add ICU Text Codec aliases (from openSUSE via Russian Fedora)
Patch14:	chromium-52.0.2743.82-more-codec-aliases.patch
# Use PIE in the Linux sandbox (from openSUSE via Russian Fedora)
Patch15:	chromium-52.0.2743.82-sandbox-pie.patch
# Enable ARM CPU detection for webrtc (from archlinux via Russian Fedora)
Patch16:	chromium-52.0.2743.82-arm-webrtc.patch
# Do not force -m32 in icu compile on ARM (from archlinux via Russian Fedora)
Patch17:	chromium-52.0.2743.82-arm-icu-fix.patch
# Use /etc/chromium for master_prefs
Patch18:	chromium-52.0.2743.82-master-prefs-path.patch
# Disable MADV_FREE (if set by glibc)
# https://bugzilla.redhat.com/show_bug.cgi?id=1361157
Patch19:	chromium-52.0.2743.116-unset-madv_free.patch
# Use gn system files
Patch20:	chromium-53.0.2785.92-gn-system.patch
# Fix last commit position issue
# https://groups.google.com/a/chromium.org/forum/#!topic/gn-dev/7nlJv486bD4
Patch21:	chromium-53.0.2785.92-last-commit-position.patch
# Fix issue where timespec is not defined when sys/stat.h is included.
Patch22:	chromium-53.0.2785.92-boringssl-time-fix.patch
# Fix gn build on Linux
# https://crrev.com/415208
Patch23:	chromium-53.0.2785.101-crrev-415028.patch

### Chromium Tests Patches ###
Patch100:	chromium-46.0.2490.86-use_system_opus.patch
Patch101:	chromium-52.0.2723.2-use_system_harfbuzz.patch
Patch102:	chromium-52.0.2723.2-sync_link_zlib.patch

# Use chromium-latest.py to generate clean tarball from released build tarballs, found here:
# http://build.chromium.org/buildbot/official/
# For Chromium Fedora use chromium-latest.py --stable --ffmpegclean --ffmpegarm
# If you want to include the ffmpeg arm sources append the --ffmpegarm switch
# https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%%{version}.tar.xz
%if %{freeworld}
Source0:	https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
%else
Source0:	chromium-%{version}-clean.tar.xz
%endif
%if 0%{tests}
Source1:	https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}-testdata.tar.xz
%endif
# https://chromium.googlesource.com/chromium/tools/depot_tools.git/+archive/7e7a454f9afdddacf63e10be48f0eab603be654e.tar.gz
Source2:	depot_tools.git-master.tar.gz
Source3:	chromium-browser.sh
Source4:	%{chromium_browser_channel}.desktop
# Also, only used if you want to reproduce the clean tarball.
Source5:	clean_ffmpeg.sh
Source6:	chromium-latest.py
Source7:	get_free_ffmpeg_source_files.py
# Get the names of all tests (gtests) for Linux
# Usage: get_linux_tests_name.py chromium-%%{version} --spec
Source8:	get_linux_tests_names.py
# GNOME stuff
Source9:	chromium-browser.xml
Source10:	https://dl.google.com/dl/edgedl/chrome/policy/policy_templates.zip
Source11:	chrome-remote-desktop.service
Source12:	chromium-browser.appdata.xml
Source13:	master_preferences

# We can assume gcc and binutils.
BuildRequires:	gcc-c++

BuildRequires:	alsa-lib-devel
BuildRequires:	atk-devel
BuildRequires:	bison
BuildRequires:	cups-devel
BuildRequires:	dbus-devel
BuildRequires:	desktop-file-utils
BuildRequires:	expat-devel
BuildRequires:	flex
BuildRequires:	fontconfig-devel
BuildRequires:	GConf2-devel
BuildRequires:	glib2-devel
BuildRequires:	gnome-keyring-devel
BuildRequires:	gtk2-devel
BuildRequires:	glibc-devel
BuildRequires:	gperf
BuildRequires:	libatomic
BuildRequires:	libcap-devel
BuildRequires:	libdrm-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libudev-devel
BuildRequires:	libusb-devel
BuildRequires:	libXdamage-devel
BuildRequires:	libXScrnSaver-devel
BuildRequires:	libXtst-devel
BuildRequires:	nss-devel
BuildRequires:	pciutils-devel
BuildRequires:	pulseaudio-libs-devel
%if 0%{?tests}
BuildRequires:	pam-devel
# Tests needs X
BuildRequires:	Xvfb
BuildRequires:	liberation-sans-fonts
# For sandbox initialization
BuildRequires:	sudo
%endif

# for /usr/bin/appstream-util
BuildRequires: libappstream-glib

# Fedora turns on NaCl
# NaCl needs these
BuildRequires:	libstdc++-devel, openssl-devel
%if 0%{?nacl}
BuildRequires:	nacl-gcc, nacl-binutils, nacl-newlib
BuildRequires:	nacl-arm-gcc, nacl-arm-binutils, nacl-arm-newlib
# pNaCl needs this monster
# It's possible that someday this dep will stabilize, but 
# right now, it needs to be updated everytime chromium bumps
# a major version.
BuildRequires:	chromium-native_client >= 52.0.2743.82
%ifarch x86_64
# Really, this is what we want:
# BuildRequires:  glibc-devel(x86-32) libgcc(x86-32)
# But, koji only offers glibc32. Maybe that's enough.
# This BR will pull in either glibc.i686 or glibc32.
BuildRequires:	/lib/libc.so.6 /usr/lib/libc.so
%endif
%endif
# Fedora tries to use system libs whenever it can.
BuildRequires:	bzip2-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	elfutils-libelf-devel
BuildRequires:	flac-devel
BuildRequires:	hwdata
BuildRequires:	kernel-headers
BuildRequires:	libevent-devel
BuildRequires:	libffi-devel
%if 0%{?bundleicu}
# If this is true, we're using the bundled icu.
# We'd like to use the system icu every time, but we cannot always do that.
%else
# Not newer than 54 (at least not right now)
BuildRequires:	libicu-devel = 54.1
%endif
BuildRequires:	libjpeg-devel
# BuildRequires:	libpng-devel
%if 0
# see https://code.google.com/p/chromium/issues/detail?id=501318
BuildRequires:	libsrtp-devel >= 1.4.4
%endif
BuildRequires:	libudev-devel
%if %{bundlelibusbx}
# Do nothing
%else
Requires:	libusbx >= 1.0.21-0.1.git448584a
BuildRequires:	libusbx-devel >= 1.0.21-0.1.git448584a
%endif
# We don't use libvpx anymore because Chromium loves to
# use bleeding edge revisions here that break other things
# ... so we just use the bundled libvpx.
# Same is true for libwebp.
BuildRequires:	libxslt-devel
# Same here, it seems.
# BuildRequires:	libyuv-devel
%if %{bundleopus}
# Do nothing
%else
BuildRequires:	opus-devel
%endif
BuildRequires:	perl(Switch)
%if 0%{gtk3}
BuildRequires:	pkgconfig(gtk+-3.0)
%endif
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	python-beautifulsoup4
BuildRequires:	python-BeautifulSoup
BuildRequires:	python-html5lib
BuildRequires:	python-jinja2
BuildRequires:	python-markupsafe
BuildRequires:	python-ply
BuildRequires:	python-simplejson
%if 0%{?bundlere2}
# Using bundled bits, do nothing.
%else
Requires:	re2 >= 20160401
BuildRequires:	re2-devel >= 20160401
%endif
BuildRequires:	speech-dispatcher-devel
BuildRequires:	yasm
BuildRequires:	pkgconfig(gnome-keyring-1)
# remote desktop needs this
BuildRequires:	pam-devel
BuildRequires:	systemd
%if 0%{?asan}
BuildRequires:	clang, compiler-rt
%endif

# We pick up an automatic requires on the library, but we need the version check
# because the nss shared library is unversioned.
# This is to prevent someone from hitting http://code.google.com/p/chromium/issues/detail?id=26448
Requires:	nss%{_isa} >= 3.12.3
Requires:	nss-mdns%{_isa}

# GTK modules it expects to find for some reason.
Requires:	libcanberra-gtk2%{_isa}

%if 0%{?fedora}
# This enables support for u2f tokens
Requires:	u2f-hidraw-policy
%endif

# Once upon a time, we tried to split these out... but that's not worth the effort anymore.
Provides:	chromium-ffmpegsumo = %{version}-%{release}
Obsoletes:	chromium-ffmpegsumo <= 35.0.1916.114
# This is a lie. v8 has its own version... but I'm being lazy and not using it here.
# Barring Google getting much faster on the v8 side (or much slower on the Chromium side)
# the true v8 version will be much smaller than the Chromium version that it came from.
Provides:	chromium-v8 = %{version}-%{release}
Obsoletes:	chromium-v8 <= 3.25.28.18
# This is a lie. webrtc never had any real version. 0.2 is greater than 0.1
Provides:	webrtc = 0.2
Obsoletes:	webrtc <= 0.1
%if 0%{?shared}
Requires:       chromium-libs%{_isa} = %{version}-%{release}
# This is broken out so it can be replaced.
Requires:	chromium-libs-media%{_isa} = %{version}-%{release}
# Nothing to do here. chromium-libs is real.
%else
Provides:	chromium-libs = %{version}-%{release}
Obsoletes:	chromium-libs <= %{version}-%{release}
%endif

ExclusiveArch:	x86_64 i686

# Bundled bits (I'm sure I've missed some)
Provides: bundled(angle) = 2422
Provides: bundled(bintrees) = 1.0.1
# This is a fork of openssl.
Provides: bundled(boringssl)
Provides: bundled(brotli)
Provides: bundled(bspatch)
Provides: bundled(cacheinvalidation) = 20150720
Provides: bundled(cardboard) = 0.5.4
Provides: bundled(colorama) = 799604a104
Provides: bundled(crashpad)
Provides: bundled(dmg_fp)
Provides: bundled(expat) = 2.1.0
Provides: bundled(fdmlibm) = 5.3
# Don't get too excited. MPEG and other legally problematic stuff is stripped out.
Provides: bundled(ffmpeg) = 2.6
Provides: bundled(fips181) = 2.2.3
Provides: bundled(fontconfig) = 2.11.0
Provides: bundled(gperftools) = svn144
Provides: bundled(gtk3) = 3.1.4
%if 0%{?bundleharfbuzz}
Provides: bundled(harfbuzz) = 1.2.7
%endif
Provides: bundled(hunspell) = 1.3.2
Provides: bundled(iccjpeg)
%if 0%{?bundleicu}
Provides: bundled(icu) = 54.1
%endif
Provides: bundled(kitchensink) = 1
Provides: bundled(leveldb) = r80
Provides: bundled(libaddressinput) = 0
Provides: bundled(libjingle) = 9564
Provides: bundled(libphonenumber) = svn584
Provides: bundled(libpng) = 1.6.22
Provides: bundled(libsrtp) = 1.5.2
%if %{bundlelibusbx}
Provides: bundled(libusbx) = 1.0.17
%endif
Provides: bundled(libvpx) = 1.4.0
Provides: bundled(libwebp) = 0.4.3
Provides: bundled(libXNVCtrl) = 302.17
Provides: bundled(libyuv) = 1444
Provides: bundled(lzma) = 9.20
Provides: bundled(libudis86) = 1.7.1
Provides: bundled(mesa) = 9.0.3
Provides: bundled(NSBezierPath) = 1.0
Provides: bundled(mozc)
Provides: bundled(mt19937ar) = 2002.1.26
%if %{bundleopus}
Provides: bundled(opus) = 1.1.2
%endif
Provides: bundled(ots) = 767d6040439e6ebcdb867271fcb686bd3f8ac739
Provides: bundled(protobuf) = r476
Provides: bundled(qcms) = 4
%if 0%{?bundlere2}
Provides: bundled(re2)
%endif
Provides: bundled(sfntly) = svn111
Provides: bundled(skia)
Provides: bundled(SMHasher) = 0
Provides: bundled(snappy) = r80
Provides: bundled(speech-dispatcher) = 0.7.1
Provides: bundled(sqlite) = 3.8.7.4
Provides: bundled(superfasthash) = 0
Provides: bundled(talloc) = 2.0.1
Provides: bundled(usrsctp) = 0
Provides: bundled(v8) = 4.5.103.35
Provides: bundled(webrtc) = 90usrsctp
Provides: bundled(woff2) = 445f541996fe8376f3976d35692fd2b9a6eedf2d
Provides: bundled(xdg-mime)
Provides: bundled(xdg-user-dirs)
Provides: bundled(x86inc) = 0
Provides: bundled(zlib) = 1.2.5

# For selinux scriptlet
Requires(post): /usr/sbin/semanage
Requires(post): /usr/sbin/restorecon

%description
Chromium is an open-source web browser, powered by WebKit (Blink).

%if 0%{?shared}
%package libs
Summary: Shared libraries used by chromium (and chrome-remote-desktop)
Requires: chromium-libs-media%{_isa} = %{version}

%description libs
Shared libraries used by chromium (and chrome-remote-desktop).

%if %{freeworld}
%package libs-media-freeworld
Summary: Chromium media libraries built with all possible codecs
Provides: chromium-libs-media = %{version}-%{release}
Provides: chromium-libs-media%{_isa} = %{version}-%{release}

%description libs-media-freeworld
Chromium media libraries built with all possible codecs. Chromium is an
open-source web browser, powered by WebKit (Blink). This package replaces
the default chromium-libs-media package, which is limited in what it
can include.
%else
%package libs-media
Summary: Shared libraries used by the chromium media subsystem
Requires: chromium-libs%{_isa} = %{version}

%description libs-media
Shared libraries used by the chromium media subsystem.
%endif
%endif

%package -n chrome-remote-desktop
Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: xorg-x11-server-Xvfb
%if 0%{?shared}
Requires: chromium-libs%{_isa} = %{version}-%{release}
%endif
Summary: Remote desktop support for google-chrome & chromium

%description -n chrome-remote-desktop
Remote desktop support for google-chrome & chromium.

%package -n chromedriver
Summary:	WebDriver for Google Chrome/Chromium
%if 0%{?shared}
Requires:       chromium-libs%{_isa} = %{version}-%{release}
%endif
# From Russian Fedora (minus the epoch)
Provides:	chromedriver-stable = %{version}-%{release}
Conflicts:	chromedriver-testing
Conflicts:	chromedriver-unstable

%description -n chromedriver
WebDriver is an open source tool for automated testing of webapps across many
browsers. It provides capabilities for navigating to web pages, user input,
JavaScript execution, and more. ChromeDriver is a standalone server which
implements WebDriver's wire protocol for Chromium. It is being developed by
members of the Chromium and WebDriver teams.

%prep
%setup -q -T -c -n %{name}-policies -a 10
%setup -q -T -c -n depot_tools -a 2
%if 0%{tests}
%setup -q -n chromium-%{version} -b 1
%else
%setup -q -n chromium-%{version}
%endif

### Chromium Fedora Patches ###
%patch0 -p1 -b .gcc5
%patch1 -p1 -b .pathmax
%patch2 -p1 -b .addrfix
%patch3 -p1 -b .system-icu
%patch4 -p1 -b .notest
%patch6 -p1 -b .gnu-inline
%patch7 -p1 -b .ignore-fd-count
%patch9 -p1 -b .modern-libusbx
%patch10 -p1 -b .unbundle-fix
%patch12 -p1 -b .cups22
%patch14 -p1 -b .morealiases
%patch15 -p1 -b .sandboxpie
%patch16 -p1 -b .armwebrtc
%patch17 -p1 -b .armfix
%patch18 -p1 -b .etc
%patch19 -p1 -b .madv_free
%patch20 -p1 -b .gnsystem
%patch21 -p1 -b .lastcommit
%patch22 -p1 -b .timefix
%patch23 -p1 -b .415208

### Chromium Tests Patches ###
%patch100 -p1 -b .use_system_opus
%patch101 -p1 -b .use_system_harfbuzz
%patch102 -p1 -b .sync_link_zlib

%if 0%{?asan}
export CC="clang"
export CXX="clang++"
%else
export CC="gcc"
export CXX="g++"
%endif
export AR="ar"
export RANLIB="ranlib"

%if 0%{?nacl}
# prep the nacl tree
mkdir -p out/Release/gen/sdk/linux_x86/nacl_x86_newlib
cp -a --no-preserve=context /usr/%{_arch}-nacl/* out/Release/gen/sdk/linux_x86/nacl_x86_newlib

mkdir -p out/Release/gen/sdk/linux_x86/nacl_arm_newlib
cp -a --no-preserve=context /usr/arm-nacl/* out/Release/gen/sdk/linux_x86/nacl_arm_newlib

# Not sure if we need this or not, but better safe than sorry.
pushd out/Release/gen/sdk/linux_x86
ln -s nacl_x86_newlib nacl_x86_newlib_raw
ln -s nacl_arm_newlib nacl_arm_newlib_raw
popd

mkdir -p out/Release/gen/sdk/linux_x86/nacl_x86_newlib/bin
pushd out/Release/gen/sdk/linux_x86/nacl_x86_newlib/bin
ln -s /usr/bin/x86_64-nacl-gcc gcc
ln -s /usr/bin/x86_64-nacl-gcc x86_64-nacl-gcc
ln -s /usr/bin/x86_64-nacl-g++ g++
ln -s /usr/bin/x86_64-nacl-g++ x86_64-nacl-g++
# ln -s /usr/bin/x86_64-nacl-ar ar
ln -s /usr/bin/x86_64-nacl-ar x86_64-nacl-ar
# ln -s /usr/bin/x86_64-nacl-as as
ln -s /usr/bin/x86_64-nacl-as x86_64-nacl-as
# ln -s /usr/bin/x86_64-nacl-ranlib ranlib
ln -s /usr/bin/x86_64-nacl-ranlib x86_64-nacl-ranlib
# Cleanups
rm addr2line
ln -s /usr/bin/x86_64-nacl-addr2line addr2line
rm c++filt
ln -s /usr/bin/x86_64-nacl-c++filt c++filt
rm gprof
ln -s /usr/bin/x86_64-nacl-gprof gprof
rm readelf
ln -s /usr/bin/x86_64-nacl-readelf readelf
rm size
ln -s /usr/bin/x86_64-nacl-size size
rm strings
ln -s /usr/bin/x86_64-nacl-strings strings
popd

mkdir -p out/Release/gen/sdk/linux_x86/nacl_arm_newlib/bin
pushd out/Release/gen/sdk/linux_x86/nacl_arm_newlib/bin
ln -s /usr/bin/arm-nacl-gcc gcc
ln -s /usr/bin/arm-nacl-gcc arm-nacl-gcc
ln -s /usr/bin/arm-nacl-g++ g++
ln -s /usr/bin/arm-nacl-g++ arm-nacl-g++
ln -s /usr/bin/arm-nacl-ar arm-nacl-ar
ln -s /usr/bin/arm-nacl-as arm-nacl-as
ln -s /usr/bin/arm-nacl-ranlib arm-nacl-ranlib
popd

touch out/Release/gen/sdk/linux_x86/nacl_x86_newlib/stamp.untar out/Release/gen/sdk/linux_x86/nacl_x86_newlib/stamp.prep
touch out/Release/gen/sdk/linux_x86/nacl_x86_newlib/nacl_x86_newlib.json
touch out/Release/gen/sdk/linux_x86/nacl_arm_newlib/stamp.untar out/Release/gen/sdk/linux_x86/nacl_arm_newlib/stamp.prep
touch out/Release/gen/sdk/linux_x86/nacl_arm_newlib/nacl_arm_newlib.json

pushd out/Release/gen/sdk/linux_x86/
mkdir -p pnacl_newlib pnacl_translator
# Might be able to do symlinks here, but eh.
cp -a --no-preserve=context /usr/pnacl_newlib/* pnacl_newlib/
cp -a --no-preserve=context /usr/pnacl_translator/* pnacl_translator/
for i in lib/libc.a lib/libc++.a lib/libg.a lib/libm.a; do
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/x86_64_bc-nacl/$i
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/i686_bc-nacl/$i
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/le32-nacl/$i
done

for i in lib/clang/3.7.0/lib/x86_64_bc-nacl/libpnaclmm.a lib/clang/3.7.0/lib/i686_bc-nacl/libpnaclmm.a; do
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/$i
done

for i in lib/clang/3.7.0/lib/le32-nacl/libpnaclmm.a lib/clang/3.7.0/lib/le32-nacl/libgcc.a; do
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/$i
done

popd

mkdir -p native_client/toolchain/.tars/linux_x86
touch native_client/toolchain/.tars/linux_x86/pnacl_translator.json

pushd native_client/toolchain
ln -s ../../out/Release/gen/sdk/linux_x86 linux_x86
popd
%endif

CHROMIUM_BROWSER_GN_DEFINES=""
%ifarch x86_64
CHROMIUM_BROWSER_GN_DEFINES+=' system_libdir="lib64"'
%endif
CHROMIUM_BROWSER_GN_DEFINES+=' google_api_key="%{api_key}" google_default_client_id="%{default_client_id}" google_default_client_secret="%{default_client_secret}"'
CHROMIUM_BROWSER_GN_DEFINES+=' is_clang=false use_sysroot=false use_gio=true use_pulseaudio=true icu_use_data_file_flag=true'
%if 0%{?nonacl}
CHROMIUM_BROWSER_GN_DEFINES+=' enable_nacl=false'
%endif
%if %{freeworld}
CHROMIUM_BROWSER_GN_DEFINES+=' ffmpeg_branding="ChromeOS" proprietary_codecs=true'
%else
CHROMIUM_BROWSER_GN_DEFINES+=' ffmpeg_branding="Chromium" proprietary_codecs=false'
%endif
%if 0%{?shared}
CHROMIUM_BROWSER_GN_DEFINES+=' is_component_ffmpeg=true is_component_build=true'
%else
CHROMIUM_BROWSER_GN_DEFINES+=' is_component_ffmpeg=false is_component_build=false'
%endif
CHROMIUM_BROWSER_GN_DEFINES+=' remove_webcore_debug_symbols=true enable_hangout_services_extension=true'
CHROMIUM_BROWSER_GN_DEFINES+=' enable_hotwording=false use_aura=true enable_hidpi=true'
CHROMIUM_BROWSER_GN_DEFINES+=' enable_webrtc=true enable_widevine=true'
%if 0%{gtk3}
CHROMIUM_BROWSER_GN_DEFINES+=' use_gtk3=true'
%else
CHROMIUM_BROWSER_GN_DEFINES+=' use_gtk3=false'
%endif
CHROMIUM_BROWSER_GN_DEFINES+=' extra_cflags="-fno-delete-null-pointer-checks" treat_warnings_as_errors=false'
export CHROMIUM_BROWSER_GN_DEFINES

export CHROMIUM_BROWSER_GYP_DEFINES="\
%ifarch x86_64
	-Dtarget_arch=x64 \
	-Dsystem_libdir=lib64 \
%endif
	-Dgoogle_api_key="%{api_key}" \
	-Dgoogle_default_client_id="%{default_client_id}" \
	-Dgoogle_default_client_secret="%{default_client_secret}" \
%if 0%{?asan}
	-Dasan=1 \
	-Dclang=1 \
	-Dhost_clang=1 \
	-Dclang_dynlib_flags="" \
	-Dclang_plugin_args="" \
	-Dclang_chrome_plugins_flags="" \
%else
	-Dclang=0 \
        -Dhost_clang=0 \
%endif
	-Ddisable_glibc=1 \
	-Dlinux_fpic=1 \
	-Ddisable_sse2=1 \
%if 0%{?nonacl}
	-Ddisable_nacl=1 \
%else
	-Ddisable_newlib_untar=1 \
	-Ddisable_pnacl_untar=1 \
	-Dpnacl_newlib_toolchain=out/Release/gen/sdk/linux_x86/pnacl_newlib/ \
	-Dpnacl_translator_dir=/usr/pnacl_translator \
%endif
	\
	-Duse_gconf=0 \
	-Duse_gio=1 \
	-Duse_gnome_keyring=1 \
	-Duse_pulseaudio=1 \
	-Duse_system_bzip2=1 \
	-Duse_system_flac=1 \
%if 0%{?bundleharfbuzz}
	-Duse_system_harfbuzz=0 \
%else
	-Duse_system_harfbuzz=1 \
%endif
%if 0%{?bundleicu}
	-Duse_system_icu=0 \
%else
	-Duse_system_icu=1 \
%endif
	-Dicu_use_data_file_flag=1 \
	-Duse_system_libevent=1 \
	-Duse_system_libjpeg=1 \
	-Duse_system_libpng=1 \
%if %{bundlelibusbx}
	-Duse_system_libusb=0 \
%else
	-Duse_system_libusb=1 \
%endif
	-Duse_system_libxml=1 \
	-Duse_system_libxslt=1 \
%if %{bundleopus}
	-Duse_system_opus=0 \
%else
	-Duse_system_opus=1 \
%endif
	-Duse_system_protobuf=0 \
%if 0%{?bundlere2}
%else
	-Duse_system_re2=1 \
%endif
	-Duse_system_libsrtp=0 \
	-Duse_system_xdg_utils=1 \
	-Duse_system_yasm=1 \
	-Duse_system_zlib=0 \
	\
	-Dlinux_link_libspeechd=1 \
	-Dlinux_link_gnome_keyring=1 \
	-Dlinux_link_gsettings=1 \
	-Dlinux_link_libpci=1 \
	-Dlinux_link_libgps=0 \
	-Dlinux_sandbox_path=%{chromium_path}/chrome-sandbox \
	-Dlinux_sandbox_chrome_path=%{chromium_path}/chromium-browser \
	-Dlinux_strip_binary=1 \
	-Dlinux_use_bundled_binutils=0 \
	-Dlinux_use_bundled_gold=0 \
	-Dlinux_use_gold_binary=0 \
	-Dlinux_use_gold_flags=0 \
	-Dlinux_use_libgps=0 \
	\
	-Dusb_ids_path=/usr/share/hwdata/usb.ids \
%if 0%{?fedora}
	-Dlibspeechd_h_prefix=speech-dispatcher/ \
%endif
	\
%if %{freeworld}
        -Dffmpeg_branding=ChromeOS \
        -Dproprietary_codecs=1 \
%else
	-Dffmpeg_branding=Chromium \
	-Dproprietary_codecs=0 \
%endif
%if 0%{?shared}
	-Dbuild_ffmpegsumo=1 \
	-Dffmpeg_component=shared_library \
%else
	-Dffmpeg_component=static_library \
%endif
	\
	-Dno_strict_aliasing=1 \
	-Dv8_no_strict_aliasing=1 \
	\
	-Dremove_webcore_debug_symbols=1 \
	-Dlogging_like_official_build=1 \
	-Denable_hotwording=0 \
	-Duse_aura=1 \
	-Denable_hidpi=1 \
	-Denable_touch_ui=1 \
	-Denable_pepper_cdms=1 \
	-Denable_webrtc=1 \
	-Denable_widevine=1 \
%if 0%{gtk3}
	-Duse_gtk3=1 \
%else
	-Dtoolkit_uses_gtk=0 \
%endif
%if 0
	-Dbuildtype=Official \
%endif
	\
%if 0%{?shared}
	-Dcomponent=shared_library \
%endif
	-Duse_sysroot=0 \
	-Drelease_extra_cflags="-fno-delete-null-pointer-checks" \
	-Dwerror= -Dsysroot="

# Remove most of the bundled libraries. Libraries specified below (taken from
# Gentoo's Chromium ebuild) are the libraries that needs to be preserved.
build/linux/unbundle/remove_bundled_libraries.py \
%if 0%{?asan}
	'buildtools/third_party/libc++' \
	'buildtools/third_party/libc++abi' \
%endif
	'third_party/ffmpeg' \
	'third_party/adobe' \
	'third_party/flac' \
	'third_party/harfbuzz-ng' \
	'third_party/icu' \
	'base/third_party/libevent' \
	'third_party/libjpeg_turbo' \
	'third_party/libpng' \
	'third_party/libsrtp' \
	'third_party/libwebp' \
	'third_party/libxml' \
	'third_party/libxslt' \
%if %{freeworld}
	'third_party/openh264' \
%endif
%if 0%{?bundlere2}
	'third_party/re2' \
%endif
	'third_party/snappy' \
	'third_party/speech-dispatcher' \
	'third_party/usb_ids' \
	'third_party/woff2' \
	'third_party/xdg-utils' \
	'third_party/yasm' \
	'third_party/zlib' \
	'base/third_party/dmg_fp' \
	'base/third_party/dynamic_annotations' \
	'base/third_party/icu' \
	'base/third_party/nspr' \
	'base/third_party/superfasthash' \
	'base/third_party/symbolize' \
	'base/third_party/valgrind' \
	'base/third_party/xdg_mime' \
	'base/third_party/xdg_user_dirs' \
	'breakpad/src/third_party/curl' \
	'chrome/third_party/mozilla_security_manager' \
	'courgette/third_party' \
	'native_client/src/third_party/dlmalloc' \
	'native_client/src/third_party/valgrind' \
	'net/third_party/mozilla_security_manager' \
	'net/third_party/nss' \
	'third_party/WebKit' \
	'third_party/analytics' \
	'third_party/angle' \
	'third_party/angle/src/common/third_party/numerics' \
	'third_party/angle/src/third_party/compiler' \
	'third_party/angle/src/third_party/libXNVCtrl' \
	'third_party/angle/src/third_party/murmurhash' \
	'third_party/angle/src/third_party/trace_event' \
	'third_party/boringssl' \
	'third_party/brotli' \
	'third_party/cacheinvalidation' \
	'third_party/catapult' \
	'third_party/catapult/tracing/third_party/components/polymer' \
	'third_party/catapult/tracing/third_party/d3' \
	'third_party/catapult/tracing/third_party/gl-matrix' \
	'third_party/catapult/tracing/third_party/jszip' \
	'third_party/catapult/tracing/third_party/mannwhitneyu' \
	'third_party/catapult/third_party/py_vulcanize' \
	'third_party/catapult/third_party/py_vulcanize/third_party/rcssmin' \
	'third_party/catapult/third_party/py_vulcanize/third_party/rjsmin' \
	'third_party/cld_2' \
	'third_party/cros_system_api' \
	'third_party/cython/python_flags.py' \
	'third_party/devscripts' \
	'third_party/dom_distiller_js' \
	'third_party/dom_distiller_js/dist/proto_gen/third_party/dom_distiller_js' \
	'third_party/fips181' \
	'third_party/flot' \
	'third_party/google_input_tools' \
	'third_party/google_input_tools/third_party/closure_library' \
	'third_party/google_input_tools/third_party/closure_library/third_party/closure' \
	'third_party/hunspell' \
	'third_party/iccjpeg' \
	'third_party/jstemplate' \
	'third_party/khronos' \
	'third_party/leveldatabase' \
	'third_party/libXNVCtrl' \
	'third_party/libaddressinput' \
	'third_party/libjingle' \
	'third_party/libphonenumber' \
	'third_party/libsecret' \
	'third_party/libudev' \
	'third_party/libusb' \
	'third_party/libvpx' \
	'third_party/libvpx/source/libvpx/third_party/x86inc' \
	'third_party/libxml/chromium' \
	'third_party/libwebm' \
	'third_party/libyuv' \
	'third_party/lss' \
	'third_party/lzma_sdk' \
	'third_party/mesa' \
	'third_party/modp_b64' \
	'third_party/mt19937ar' \
	'third_party/openmax_dl' \
	'third_party/opus' \
	'third_party/ots' \
	'third_party/pdfium' \
	'third_party/pdfium/third_party/agg23' \
	'third_party/pdfium/third_party/base' \
	'third_party/pdfium/third_party/bigint' \
	'third_party/pdfium/third_party/freetype' \
	'third_party/pdfium/third_party/lcms2-2.6' \
	'third_party/pdfium/third_party/libjpeg' \
	'third_party/pdfium/third_party/libopenjpeg20' \
	'third_party/pdfium/third_party/zlib_v128' \
	'third_party/polymer' \
	'third_party/protobuf' \
	'third_party/protobuf/third_party/six' \
	'third_party/ply' \
	'third_party/qcms' \
	'third_party/sfntly' \
	'third_party/skia' \
	'third_party/smhasher' \
	'third_party/sqlite' \
	'third_party/tcmalloc' \
	'third_party/usrsctp' \
	'third_party/web-animations-js' \
	'third_party/webdriver' \
	'third_party/webrtc' \
	'third_party/widevine' \
	'third_party/x86inc' \
	'third_party/zlib/google' \
	'url/third_party/mozilla' \
	'v8/src/third_party/fdlibm' \
	'v8/src/third_party/valgrind' \
	--do-remove

# Look, I don't know. This package is spit and chewing gum. Sorry.
rm -rf third_party/jinja2
ln -s %{python_sitelib}/jinja2 third_party/jinja2
rm -rf third_party/markupsafe
ln -s %{python_sitearch}/markupsafe third_party/markupsafe
# We should look on removing other python packages as well i.e. ply

# Fix hardcoded path in remoting code
sed -i 's|/opt/google/chrome-remote-desktop|%{crd_path}|g' remoting/host/setup/daemon_controller_delegate_linux.cc

export PATH=$PATH:%{_builddir}/depot_tools

%if %{use_gn}
build/linux/unbundle/replace_gn_files.py --system-libraries \
	flac \
%if 0%{?bundleharfbuzz}
%else
	harfbuzz-ng \
%endif
%if 0%{?bundleicu}
%else
	icu \
%endif
	libevent \
	libjpeg \
%if %{bundlelibusbx}
%else
	libusb \
%endif
	libxml \
	libxslt \
%if %{bundleopus}
%else
	opus \
%endif
%if 0%{?bundlere2}
%else
	re2 \
%endif
	yasm

tools/gn/bootstrap/bootstrap.py -v --gn-gen-args "$CHROMIUM_BROWSER_GN_DEFINES"
%{target}/gn gen --args="$CHROMIUM_BROWSER_GN_DEFINES" %{target}
%else
# Update gyp files according to our configuration
# If you will change something in the configuration please update it
# for build/gyp_chromium as well (and vice versa).
build/linux/unbundle/replace_gyp_files.py $CHROMIUM_BROWSER_GYP_DEFINES

build/gyp_chromium \
	--depth . \
%if 0%{?asan}
	-Drelease_extra_cflags="-O1 -fno-inline-functions -fno-inline" \
%endif
	$CHROMIUM_BROWSER_GYP_DEFINES
%endif

%if %{bundlelibusbx}
# no hackity hack hack
%else
# hackity hack hack
rm -rf third_party/libusb/src/libusb/libusb.h
%endif

# make up a version for widevine
sed '14i#define WIDEVINE_CDM_VERSION_STRING "Something fresh"' -i "third_party/widevine/cdm/stub/widevine_cdm_version.h"

# Hard code extra version
FILE=chrome/common/channel_info_posix.cc
sed -i.orig -e 's/getenv("CHROME_VERSION_EXTRA")/"Fedora Project"/' $FILE

%build

%if %{?tests}
# Tests targets taken from testing/buildbot/chromium.linux.json and obtained with
# get_linux_tests_name.py PATH_TO_UNPACKED_CHROMIUM_SOURCES --spec
# You can also check if you have to update the tests in SPEC file by running
# get_linux_tests_name.py PATH_TO_UNPACKED_CHROMIUM_SOURCES --check PATH_TO_SPEC_FILE
export CHROMIUM_BROWSER_UNIT_TESTS="\
	accessibility_unittests \
	app_list_unittests \
	app_shell_unittests \
	aura_unittests \
	base_unittests \
	browser_tests \
	cacheinvalidation_unittests \
	cast_unittests \
	cc_unittests \
	chromedriver_unittests \
	components_browsertests \
	components_unittests \
	compositor_unittests \
	content_browsertests \
	content_unittests \
	crypto_unittests \
	dbus_unittests \
	device_unittests \
	display_unittests \
	events_unittests \
	extensions_browsertests \
	extensions_unittests \
	gcm_unit_tests \
	gfx_unittests \
	gl_unittests \
	gn_unittests \
	google_apis_unittests \
	gpu_unittests \
	interactive_ui_tests \
	ipc_mojo_unittests \
	ipc_tests \
	jingle_unittests \
	media_unittests \
	midi_unittests \
	mojo_common_unittests \
	mojo_public_bindings_unittests \
	mojo_public_environment_unittests \
	mojo_public_system_unittests \
	mojo_public_utility_unittests \
	mojo_system_unittests \
%if 0%{?nacl}
	nacl_loader_unittests \
%endif
	net_unittests \
	ppapi_unittests \
	printing_unittests \
	remoting_unittests \
	sandbox_linux_unittests \
	skia_unittests \
	sql_unittests \
	sync_integration_tests \
	sync_unit_tests \
	ui_base_unittests \
	ui_touch_selection_unittests \
	unit_tests \
	url_unittests \
	views_unittests \
	wm_unittests \
	"
%else
export CHROMIUM_BROWSER_UNIT_TESTS=
%endif


%global target out/Release

../depot_tools/ninja -C %{target} -vvv chrome chrome_sandbox chromedriver widevinecdmadapter clearkeycdm policy_templates $CHROMIUM_BROWSER_UNIT_TESTS

# remote client
pushd remoting
../../depot_tools/ninja -C ../%{target} -vvv remoting_me2me_host remoting_start_host remoting_it2me_native_messaging_host remoting_me2me_native_messaging_host remoting_native_messaging_manifests remoting_resources
%if 0%{?build_remoting_app}
%if 0%{?nacl}
GOOGLE_CLIENT_ID_REMOTING_IDENTITY_API=%{chromoting_client_id} ../../depot_tools/ninja -vv -C ../out/Release/ remoting_webapp
%endif
%endif
popd


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{chromium_path}
cp -a %{SOURCE3} %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
export BUILD_TARGET=`cat /etc/redhat-release`
export CHROMIUM_PATH=%{chromium_path}
export CHROMIUM_BROWSER_CHANNEL=%{chromium_browser_channel}
sed -i "s|@@BUILD_TARGET@@|$BUILD_TARGET|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
sed -i "s|@@CHROMIUM_PATH@@|$CHROMIUM_PATH|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
sed -i "s|@@CHROMIUM_BROWSER_CHANNEL@@|$CHROMIUM_BROWSER_CHANNEL|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
%if "%{chromium_channel}" == "%%{nil}"
sed -i "s|@@EXTRA_FLAGS@@||g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
%else
# Enable debug outputs for beta and dev channels
export EXTRA_FLAGS="--enable-logging=stderr --v=2"
sed -i "s|@@EXTRA_FLAGS@@|$EXTRA_FLAGS|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
%endif

ln -s %{chromium_path}/%{chromium_browser_channel}.sh %{buildroot}%{_bindir}/%{chromium_browser_channel}
mkdir -p %{buildroot}%{_mandir}/man1/

pushd %{target}
cp -a *.pak locales resources icudtl.dat %{buildroot}%{chromium_path}
%if 0%{?nacl}
cp -a nacl_helper* *.nexe pnacl tls_edit %{buildroot}%{chromium_path}
chmod -x %{buildroot}%{chromium_path}/nacl_helper_bootstrap* *.nexe
%endif
cp -a protoc pseudo_locales pyproto %{buildroot}%{chromium_path}
cp -a chrome %{buildroot}%{chromium_path}/%{chromium_browser_channel}
cp -a chrome_sandbox %{buildroot}%{chromium_path}/chrome-sandbox
cp -a chrome.1 %{buildroot}%{_mandir}/man1/%{chromium_browser_channel}.1
# V8 initial snapshots
# https://code.google.com/p/chromium/issues/detail?id=421063
cp -a natives_blob.bin %{buildroot}%{chromium_path}
cp -a snapshot_blob.bin %{buildroot}%{chromium_path}
%if 0%{?shared}
cp -a lib %{buildroot}%{chromium_path}
%endif
# clearkeycdm and widevine bits
# EXCEPT libwidevinecdm*.so*. At least libwidevinecdm.so is just an empty shim, 
# because the chromium sources don't have the prebuilt binary. 
# You'll have to get libwidevinecdm*.so*
# from Google Chrome and copy it in /usr/lib64/chromium-browser/
cp -a libclearkeycdm.so* %{buildroot}%{chromium_path}

# chromedriver
cp -a chromedriver %{buildroot}%{chromium_path}/chromedriver
ln -s %{chromium_path}/chromedriver %{buildroot}%{_bindir}/chromedriver

# Remote desktop bits
mkdir -p %{buildroot}%{crd_path}

%if 0%{?shared}
pushd %{buildroot}%{crd_path}
ln -s %{chromium_path}/lib lib
popd
%endif

# See remoting/host/installer/linux/Makefile for logic
cp -a native_messaging_host %{buildroot}%{crd_path}/native-messaging-host
cp -a remote_assistance_host %{buildroot}%{crd_path}/remote-assistance-host
cp -a remoting_locales %{buildroot}%{crd_path}/
cp -a remoting_me2me_host %{buildroot}%{crd_path}/chrome-remote-desktop-host
cp -a remoting_start_host %{buildroot}%{crd_path}/start-host

# chromium
mkdir -p %{buildroot}%{_sysconfdir}/chromium/native-messaging-hosts
# google-chrome
mkdir -p %{buildroot}%{_sysconfdir}/opt/chrome/
cp -a remoting/* %{buildroot}%{_sysconfdir}/chromium/native-messaging-hosts/
for i in %{buildroot}%{_sysconfdir}/chromium/native-messaging-hosts/*.json; do
	sed -i 's|/opt/google/chrome-remote-desktop|%{crd_path}|g' $i
done
pushd %{buildroot}%{_sysconfdir}/opt/chrome/
ln -s ../../chromium/native-messaging-hosts native-messaging-hosts
popd

mkdir -p %{buildroot}/var/lib/chrome-remote-desktop
touch %{buildroot}/var/lib/chrome-remote-desktop/hashes

mkdir -p %{buildroot}%{_sysconfdir}/pam.d/
pushd %{buildroot}%{_sysconfdir}/pam.d/
ln -s system-auth chrome-remote-desktop
popd

%if 0%{?build_remoting_app}
%if 0%{?nacl}
cp -a remoting_client_plugin_newlib.* %{buildroot}%{chromium_path}
%endif
%endif
popd

cp -a remoting/host/linux/linux_me2me_host.py %{buildroot}%{crd_path}/chrome-remote-desktop
cp -a remoting/host/installer/linux/is-remoting-session %{buildroot}%{crd_path}/

mkdir -p %{buildroot}%{_unitdir}
cp -a %{SOURCE11} %{buildroot}%{_unitdir}/
sed -i 's|@@CRD_PATH@@|%{crd_path}|g' %{buildroot}%{_unitdir}/chrome-remote-desktop.service

# Add directories for policy management
mkdir -p %{buildroot}%{_sysconfdir}/chromium/policies/managed
mkdir -p %{buildroot}%{_sysconfdir}/chromium/policies/recommended
cp -a ../%{name}-policies/common/html/en-US/*.html .

# linux json files no longer in .zip file
#cp -a ../%{name}-policies/linux/examples/*.json .
cp -a out/Release/gen/chrome/app/policy/linux/examples/chrome.json .

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
cp -a chrome/app/theme/chromium/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{chromium_browser_channel}.png

# Install the master_preferences file
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 %{SOURCE13} %{buildroot}%{_sysconfdir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/applications/
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE4}

install -D -m0644 %{SOURCE12} ${RPM_BUILD_ROOT}%{_datadir}/appdata/%{chromium_browser_channel}.appdata.xml
appstream-util validate-relax --nonet ${RPM_BUILD_ROOT}%{_datadir}/appdata/%{chromium_browser_channel}.appdata.xml

mkdir -p %{buildroot}%{_datadir}/gnome-control-center/default-apps/
cp -a %{SOURCE9} %{buildroot}%{_datadir}/gnome-control-center/default-apps/

mkdir -p %{buildroot}%{chromium_path}/PepperFlash

%check
%if 0%{tests}
%if 0%{?tests_force_display}
	export DISPLAY=:0
%else
	Xvfb :9 -screen 0 1024x768x24 &

	export XVFB_PID=$!
	export DISPLAY=:9
%endif
	export LC_ALL="en_US.utf8"

	sleep 5

	# Run tests and disable the failed ones
	pushd %{target}
	(
	cp -f chrome_sandbox chrome-sandbox
	echo "Test sandbox needs to be owned by root and have the suid set"
	if [ "$(id -u)" != "0" ]; then
		sudo chown root:root chrome-sandbox && sudo chmod 4755 chrome-sandbox
	else
		chown root:root chrome-sandbox && chmod 4755 chrome-sandbox
	fi

	# Example of failed or timed-out test annotation
	# ./browser_tests \
	#	--gtest_filter=-"\
	#		`#failed`\
	#		SandboxStatusUITest.testBPFSandboxEnabled:`#failed - not using BPF sandbox`\
	#		:\
	#		`#timed-out`\
	#		CalculatorBrowserTest.Model:\
	#		WebRtcBrowserTest.RunsAudioVideoWebRTCCallInTwoTabs\
	#	" \

	./accessibility_unittests && \
	./app_list_unittests && \
	./app_shell_unittests && \
	./aura_unittests && \
	./base_unittests \
		--gtest_filter=-"\
			`#failed`\
			ICUStringConversionsTest.ConvertToUtf8AndNormalize\
		" \
	&& \
	./browser_tests \
		--gtest_filter=-"\
			`#failed`\
			DevToolsSanityTest.TestNetworkRawHeadersText:\
			DevToolsSanityTest.TestNetworkSize:\
			DevToolsSanityTest.TestNetworkSyncSize:\
			ExtensionWebstoreGetWebGLStatusTest.Allowed:\
			InlineLoginUISafeIframeBrowserTest.Basic:\
			InlineLoginUISafeIframeBrowserTest.ConfirmationRequiredForNonsecureSignin:\
			InlineLoginUISafeIframeBrowserTest.NoWebUIInIframe:\
			InlineLoginUISafeIframeBrowserTest.TopFrameNavigationDisallowed:\
			OutOfProcessPPAPITest.Graphics3D:\
			PolicyTest.Disable3DAPIs:\
			WebRtcWebcamBrowserTests/WebRtcWebcamBrowserTest.TestAcquiringAndReacquiringWebcam/0:\
			:\
			`#timed-out`\
			CalculatorBrowserTest.Model:\
			ImageFetcherImplBrowserTest.MultipleFetch:\
			ProfileManagerBrowserTest.DeletePasswords:\
			TabCaptureApiPixelTest.EndToEndThroughWebRTC:\
			WebRtcBrowserTest.RunsAudioVideoWebRTCCallInTwoTabs:\
			WebRtcSimulcastBrowserTest.TestVgaReturnsTwoSimulcastStreams\
		" \
	&& \
	./cacheinvalidation_unittests && \
	./cast_unittests && \
	./cc_unittests && \
	./chromedriver_unittests && \
	./components_unittests \
		--gtest_filter=-"\
			`#failed`\
			AutocompleteMatchTest.Duplicates:\
			BookmarkIndexTest.GetBookmarksMatchingWithURLs:\
			BookmarkIndexTest.MatchPositionsURLs:\
			InMemoryURLIndexTypesTest.StaticFunctions:\
			ScoredHistoryMatchTest.GetTopicalityScore:\
			ScoredHistoryMatchTest.Inlining:\
			ScoredHistoryMatchTest.ScoringTLD:\
			UrlFormatterTest.FormatUrlWithOffsets:\
			UrlFormatterTest.IDNToUnicodeFast:\
			UrlFormatterTest.IDNToUnicodeSlow\
		" \
	&& \
	./components_browsertests \
		--gtest_filter=-"\
			`#failed`\
			AutofillRiskFingerprintTest.GetFingerprint\
		" \
	&& \
	./compositor_unittests && \
	./content_browsertests \
		--gtest_filter=-"\
			`#failed`\
			BrowserGpuChannelHostFactoryTest.:\
			BrowserGpuChannelHostFactoryTest.AlreadyEstablished:\
			BrowserGpuChannelHostFactoryTest.Basic:\
			ImageTransportFactoryBrowserTest.TestLostContext:\
			ImageTransportFactoryTearDownBrowserTest.LoseOnTearDown:\
			RenderViewImplTest.GetCompositionCharacterBoundsTest:\
			SignalTest.BasicSignalQueryTest:\
			SignalTest.BasicSignalSyncPointTest:\
			SignalTest.InvalidSignalQueryUnboundTest:\
			SignalTest.InvalidSignalSyncPointTest:\
			SignalTest.SignalQueryUnboundTest:\
			WebRtcBrowserTest.*:\
			:\
			`#timed-out`\
			WebRtcAecDumpBrowserTest.CallWithAecDump:\
			WebRtcAecDumpBrowserTest.CallWithAecDumpEnabledThenDisabled\
		" \
	&& \
	./content_unittests && \
	./crypto_unittests && \
	./dbus_unittests \
		--gtest_filter=-"\
			`#crashed`\
			EndToEndAsyncTest.InvalidObjectPath:\
			EndToEndAsyncTest.InvalidServiceName:\
			EndToEndSyncTest.InvalidObjectPath:\
			EndToEndSyncTest.InvalidServiceName:\
			MessageTest.SetInvalidHeaders\
		" \
	&& \
	./device_unittests && \
	./display_unittests && \
	./events_unittests && \
	./extensions_browsertests && \
	./extensions_unittests && \
	./gcm_unit_tests && \
	./gfx_unittests \
		--gtest_filter=-"\
			`#failed - missing Microsoft TrueType fonts`\
			FontListTest.Fonts_GetHeight_GetBaseline:\
			FontRenderParamsTest.Default:\
			FontRenderParamsTest.MissingFamily:\
			FontRenderParamsTest.Size:\
			FontRenderParamsTest.Style:\
			FontRenderParamsTest.SubstituteFamily:\
			FontRenderParamsTest.UseBitmaps:\
			FontTest.GetActualFontNameForTesting:\
			FontTest.LoadArial:\
			FontTest.LoadArialBold:\
			PlatformFontLinuxTest.DefaultFont:\
			RenderTextTest.HarfBuzz_FontListFallback:\
			RenderTextTest.SetFontList:\
			RenderTextTest.StringSizeRespectsFontListMetrics\
			:\
			`#crashed`\
			FontRenderParamsTest.Default:\
			FontRenderParamsTest.ForceFullHintingWhenAntialiasingIsDisabled:\
			FontRenderParamsTest.MissingFamily:\
			FontRenderParamsTest.NoFontconfigMatch:\
			FontRenderParamsTest.OnlySetConfiguredValues:\
			FontRenderParamsTest.Scalable:\
			FontRenderParamsTest.Size:\
			FontRenderParamsTest.Style:\
			FontRenderParamsTest.SubstituteFamily:\
			FontRenderParamsTest.UseBitmaps:\
			PlatformFontLinuxTest.DefaultFont\
		" \
	&& \
	./gl_unittests && \
	./gn_unittests \
		--gtest_filter=-"\
			`#failed`\
			Format.004:\
			Format.007:\
			Format.012:\
			Format.013:\
			Format.014:\
			Format.015:\
			Format.017:\
			Format.019:\
			Format.020:\
			Format.021:\
			Format.023:\
			Format.031:\
			Format.033:\
			Format.038:\
			Format.043:\
			Format.046:\
			Format.048:\
			Format.056:\
			Format.057:\
			Format.062:\
			ParseTree.SortRangeExtraction:\
			Parser.CommentsAtEndOfBlock:\
			Parser.CommentsConnectedInList:\
			Parser.CommentsEndOfBlockSingleLine:\
			Parser.CommentsLineAttached:\
			Parser.CommentsSuffix:\
			Parser.CommentsSuffixDifferentLine:\
			Parser.CommentsSuffixMultiple\
		" \
	&& \
	./google_apis_unittests && \
	./gpu_unittests && \
	./interactive_ui_tests \
		--gtest_filter=-"\
			`#failed`\
			AshNativeCursorManagerTest.CursorChangeOnEnterNotify:\
			BookmarkBarViewTest5.DND:\
			OmniboxViewViewsTest.DeactivateTouchEditingOnExecuteCommand:\
			OmniboxViewViewsTest.SelectAllOnTap:\
			StartupBrowserCreatorTest.LastUsedProfileActivated:\
			X11TopmostWindowFinderTest.Basic:\
			X11TopmostWindowFinderTest.Menu:\
			:\
			`#timed-out`\
			BookmarkBarViewTest9.ScrollButtonScrolls:\
			DockedPanelBrowserTest.CloseSqueezedPanels:\
			DockedPanelBrowserTest.MinimizeSqueezedActive:\
			GlobalCommandsApiTest.GlobalCommand\
		" \
	&& \
	./ipc_mojo_unittests && \
	./ipc_tests && \
	./jingle_unittests && \
	./midi_unittests && \
	./media_unittests && \
	./mojo_common_unittests && \
	./mojo_public_bindings_unittests && \
	./mojo_public_environment_unittests && \
	./mojo_public_system_unittests && \
	./mojo_public_utility_unittests && \
	./mojo_system_unittests && \
%if 0%{?nacl}
	./nacl_loader_unittests && \
%endif
	./net_unittests \
		--gtest_filter=-"\
			`#failed`\
			CertVerifyProcTest.TestKnownRoot\
		" \
	&& \
	./ppapi_unittests && \
	./printing_unittests && \
	./remoting_unittests && \
	./sandbox_linux_unittests && \
	./skia_unittests && \
	./sql_unittests && \
	./ui_base_unittests && \
	./ui_touch_selection_unittests && \
	./sync_unit_tests && \
	./unit_tests \
		--gtest_filter=-"\
			`#failed - some need https://chromium.googlesource.com/chromium/deps/hunspell_dictionaries/+/master`\
			BookmarkProviderTest.StripHttpAndAdjustOffsets:\
			HQPOrderingTest.TEAMatch:\
			HistoryQuickProviderTest.ContentsClass:\
			LimitedInMemoryURLIndexTest.Initialization:\
			MultilingualSpellCheckTest.MultilingualSpellCheckParagraph:\
			MultilingualSpellCheckTest.MultilingualSpellCheckSuggestions:\
			MultilingualSpellCheckTest.MultilingualSpellCheckWord:\
			MultilingualSpellCheckTest.MultilingualSpellCheckWordEnglishSpanish:\
			SpellCheckTest.CreateTextCheckingResultsKeepsMarkers:\
			SpellCheckTest.DictionaryFiles:\
			SpellCheckTest.EnglishWords:\
			SpellCheckTest.GetAutoCorrectionWord_EN_US:\
			SpellCheckTest.LogicalSuggestions:\
			SpellCheckTest.MisspelledWords:\
			SpellCheckTest.NoSuggest:\
			SpellCheckTest.SpellCheckParagraphLongSentenceMultipleMisspellings:\
			SpellCheckTest.SpellCheckParagraphMultipleMisspellings:\
			SpellCheckTest.SpellCheckParagraphSingleMisspellings:\
			SpellCheckTest.SpellCheckStrings_EN_US:\
			SpellCheckTest.SpellCheckSuggestions_EN_US:\
			SpellCheckTest.SpellingEngine_CheckSpelling:\
			SpellcheckWordIteratorTest.FindSkippableWordsKhmer:\
			:\
			`#crashed`\
			ListChangesTaskTest.UnderTrackedFolder:\
			ListChangesTaskTest.UnrelatedChange:\
			SpellCheckTest.RequestSpellCheckWithMisspellings:\
			SpellCheckTest.RequestSpellCheckWithMultipleRequests:\
			SpellCheckTest.RequestSpellCheckWithSingleMisspelling\
		" \
	&& \
	./url_unittests && \
	./views_unittests \
		--gtest_filter=-"\
			`#failed`\
			DesktopWindowTreeHostX11HighDPITest.LocatedEventDispatchWithCapture:\
			LabelTest.FontPropertySymbol:\
			WidgetTest.WindowMouseModalityTest\
		" \
	&& \
	./wm_unittests \
	)
	popd

	if [ -n "$XVFB_PID" ]; then
		kill $XVFB_PID
		unset XVFB_PID
		unset DISPLAY
	fi
%endif

%post
# Set SELinux labels - semanage itself will adjust the lib directory naming
# But only do it when selinux is enabled, otherwise, it gets noisy.
if selinuxenabled; then
	semanage fcontext -a -t bin_t /usr/lib/%{chromium_browser_channel}
	semanage fcontext -a -t bin_t /usr/lib/%{chromium_browser_channel}/%{chromium_browser_channel}.sh
	semanage fcontext -a -t chrome_sandbox_exec_t /usr/lib/chrome-sandbox
	restorecon -R -v %{chromium_path}/%{chromium_browser_channel}
fi

touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
	touch --no-create %{_datadir}/icons/hicolor &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%pre -n chrome-remote-desktop
getent group chrome-remote-desktop >/dev/null || groupadd -r chrome-remote-desktop

%post -n chrome-remote-desktop
%systemd_post chrome-remote-desktop.service

%preun -n chrome-remote-desktop
%systemd_preun chrome-remote-desktop.service

%postun -n chrome-remote-desktop
%systemd_postun_with_restart chrome-remote-desktop.service

%files
%doc AUTHORS
%license LICENSE
%config %{_sysconfdir}/%{name}/
%{_bindir}/%{chromium_browser_channel}
%dir %{chromium_path}
%{chromium_path}/*.bin
%{chromium_path}/*.pak
%{chromium_path}/icudtl.dat
%{chromium_path}/%{chromium_browser_channel}
%{chromium_path}/%{chromium_browser_channel}.sh
%if 0%{?nacl}
%{chromium_path}/nacl_helper*
%{chromium_path}/*.nexe
%{chromium_path}/pnacl/
%{chromium_path}/tls_edit
%endif
%dir %{chromium_path}/PepperFlash/
%{chromium_path}/protoc
# %%{chromium_path}/remoting_locales/
%{chromium_path}/pseudo_locales/
# %%{chromium_path}/plugins/
%{chromium_path}/pyproto/
%attr(4755, root, root) %{chromium_path}/chrome-sandbox
%dir %{chromium_path}/locales/
%lang(am) %{chromium_path}/locales/am.pak
%lang(ar) %{chromium_path}/locales/ar.pak
%lang(bg) %{chromium_path}/locales/bg.pak
%lang(bn) %{chromium_path}/locales/bn.pak
%lang(ca) %{chromium_path}/locales/ca.pak
%lang(cs) %{chromium_path}/locales/cs.pak
%lang(da) %{chromium_path}/locales/da.pak
%lang(de) %{chromium_path}/locales/de.pak
%lang(el) %{chromium_path}/locales/el.pak
%lang(en_GB) %{chromium_path}/locales/en-GB.pak
%lang(en_US) %{chromium_path}/locales/en-US.pak
%lang(es) %{chromium_path}/locales/es.pak
%lang(es) %{chromium_path}/locales/es-419.pak
%lang(et) %{chromium_path}/locales/et.pak
%lang(fa) %{chromium_path}/locales/fa.pak
%lang(fi) %{chromium_path}/locales/fi.pak
%lang(fil) %{chromium_path}/locales/fil.pak
%lang(fr) %{chromium_path}/locales/fr.pak
%lang(gu) %{chromium_path}/locales/gu.pak
%lang(he) %{chromium_path}/locales/he.pak
%lang(hi) %{chromium_path}/locales/hi.pak
%lang(hr) %{chromium_path}/locales/hr.pak
%lang(hu) %{chromium_path}/locales/hu.pak
%lang(id) %{chromium_path}/locales/id.pak
%lang(it) %{chromium_path}/locales/it.pak
%lang(ja) %{chromium_path}/locales/ja.pak
%lang(kn) %{chromium_path}/locales/kn.pak
%lang(ko) %{chromium_path}/locales/ko.pak
%lang(lt) %{chromium_path}/locales/lt.pak
%lang(lv) %{chromium_path}/locales/lv.pak
%lang(ml) %{chromium_path}/locales/ml.pak
%lang(mr) %{chromium_path}/locales/mr.pak
%lang(ms) %{chromium_path}/locales/ms.pak
%lang(nb) %{chromium_path}/locales/nb.pak
%lang(nl) %{chromium_path}/locales/nl.pak
%lang(pl) %{chromium_path}/locales/pl.pak
%lang(pt_BR) %{chromium_path}/locales/pt-BR.pak
%lang(pt_PT) %{chromium_path}/locales/pt-PT.pak
%lang(ro) %{chromium_path}/locales/ro.pak
%lang(ru) %{chromium_path}/locales/ru.pak
%lang(sk) %{chromium_path}/locales/sk.pak
%lang(sl) %{chromium_path}/locales/sl.pak
%lang(sr) %{chromium_path}/locales/sr.pak
%lang(sv) %{chromium_path}/locales/sv.pak
%lang(sw) %{chromium_path}/locales/sw.pak
%lang(ta) %{chromium_path}/locales/ta.pak
%lang(te) %{chromium_path}/locales/te.pak
%lang(th) %{chromium_path}/locales/th.pak
%lang(tr) %{chromium_path}/locales/tr.pak
%lang(uk) %{chromium_path}/locales/uk.pak
%lang(vi) %{chromium_path}/locales/vi.pak
%lang(zh_CN) %{chromium_path}/locales/zh-CN.pak
%lang(zh_TW) %{chromium_path}/locales/zh-TW.pak
%{chromium_path}/resources/
%{_mandir}/man1/%{chromium_browser_channel}.*
%{_datadir}/icons/hicolor/256x256/apps/%{chromium_browser_channel}.png
%{_datadir}/applications/*.desktop
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/gnome-control-center/default-apps/chromium-browser.xml

%doc chrome_policy_list.html *.json

%if 0%{?shared}
%files libs
%exclude %{chromium_path}/lib/libffmpeg.so*
%exclude %{chromium_path}/lib/libmedia.so*
%{chromium_path}/lib/
%{chromium_path}/libclearkeycdm.so*

%if %{freeworld}
%files libs-media-freeworld
%else
%files libs-media
%endif
%{chromium_path}/lib/libffmpeg.so*
%{chromium_path}/lib/libmedia.so*
%endif

%files -n chrome-remote-desktop
%{crd_path}/chrome-remote-desktop
%{crd_path}/chrome-remote-desktop-host
%{crd_path}/is-remoting-session
%if 0%{?shared}
%{crd_path}/lib
%endif
%{crd_path}/native-messaging-host
%{crd_path}/remote-assistance-host
%{_sysconfdir}/pam.d/chrome-remote-desktop
%{_sysconfdir}/chromium/native-messaging-hosts/
%{_sysconfdir}/opt/chrome/
%{crd_path}/remoting_locales/
%{crd_path}/start-host
%{_unitdir}/chrome-remote-desktop.service
/var/lib/chrome-remote-desktop/
%if 0%{?build_remoting_app}
%if 0%{?nacl}
%{chromium_path}/remoting_client_plugin_newlib.*
%endif
%endif

%files -n chromedriver
%doc AUTHORS
%license LICENSE
%{_bindir}/chromedriver
%{chromium_path}/chromedriver

%changelog
* Fri Sep 30 2016 Tom Callaway <spot@fedoraproject.org> 53.0.2785.143-1
- 53.0.2785.143

* Tue Sep 20 2016 Tom Callaway <spot@fedoraproject.org> 53.0.2785.116-1
- 53.0.2785.116

* Wed Sep 14 2016 Tom Callaway <spot@fedoraproject.org> 53.0.2785.113-1
- 53.0.2785.113

* Thu Sep  8 2016 Tom Callaway <spot@fedoraproject.org> 53.0.2785.101-1
- 53.0.2785.101
- happy star trek day. live long and prosper.

* Wed Sep  7 2016 Tom Callaway <spot@fedoraproject.org> 53.0.2785.92-1
- add basic framework for gn tooling (disabled because it doesn't work yet)
- update to 53.0.2785.92
- fix HOME environment issue in chrome-remote-desktop service file

* Mon Aug 29 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.116-11
- conditionalize Requires: u2f-hidraw-policy so that it is only used on Fedora
- use bundled harfbuzz on EL7

* Thu Aug 18 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.116-10
- disable gtk3 because it breaks lots of things
- re-enable hidpi setting

* Tue Aug 16 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.116-9
- filter out Requires/Provides for chromium-only libs and plugins

* Tue Aug 16 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.116-8
- fix path on Requires(post) line for semanage

* Mon Aug 15 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.116-7
- add Requires(post) items for selinux scriptlets

* Mon Aug 15 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.116-6
- disable the "hidpi" setting
- unset MADV_FREE if set (should get F25+ working again)

* Fri Aug 12 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.116-5
- do not package libwidevinecdm*.so, they are just empty shells
  instead, to enable widevine, get these files from Google Chrome

* Fri Aug 12 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.116-4
- add "freeworld" conditional for testing netflix/widevine

* Fri Aug 12 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.116-3
- move PepperFlash directory out of the nacl conditional (thanks to churchyard)
- fix widevine (thanks to David Vásquez and UnitedRPMS)

* Wed Aug 10 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.116-2
- include clearkeycdm and widevinecdm files in libs-media

* Mon Aug  8 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.116-1
- update to 52.0.2743.116

* Thu Aug  4 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.82-13
- change libs split to "libs-media", as that actually works.
- add PepperFlash directory (nothing in it though, sorry)

* Wed Aug  3 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.82-12
- split out libs package beyond ffmpeg, into libs and libs-content
- fix libusbx conditional for el7 to not nuke libusb headers
- disable speech-dispatcher header prefix setting if not fedora (el7)

* Wed Aug  3 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.82-11
- split out chromium-libs-ffmpeg so it can be easily replaced
- conditionalize opus and libusbx for el7

* Wed Aug  3 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.82-10
- Add ICU Text Codec aliases (from openSUSE via Russian Fedora)
- Use PIE in the Linux sandbox (from openSUSE via Russian Fedora)
- Enable ARM CPU detection for webrtc (from archlinux via Russian Fedora)
- Do not force -m32 in icu compile on ARM (from archlinux via Russian Fedora)
- Enable gtk3 support (via conditional)
- Enable fpic on linux
- Enable hidpi
- Force aura on
- Enable touch_ui
- Add chromedriver subpackage (from Russian Fedora)
- Set default master_preferences location to /etc/chromium
- Add master_preferences file as config file
- Improve chromium-browser.desktop (from Russian Fedora)

* Thu Jul 28 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.82-9
- fix conditional to disable verbose logging output unless beta/dev

* Thu Jul 28 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.82-8
- disable nacl/pnacl for Fedora 23 (and older)

* Thu Jul 28 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.82-7
- fix post scriptlet so that selinux stuff only happens when selinux is enabled

* Thu Jul 28 2016 Richard Hughes <richard@hughsie.com> 52.0.2743.82-6
- Add an AppData file so that Chromium appears in the software center

* Wed Jul 27 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.82-5
- enable nacl/pnacl (chromium-native_client has landed in Fedora)
- fix chromium-browser.sh to report Fedora build target properly

* Wed Jul 27 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.82-4
- compile with -fno-delete-null-pointer-checks (fixes v8 crashes, nacl/pnacl)
- turn nacl/pnacl off until chromium-native_client lands in Fedora

* Tue Jul 26 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.82-3
- turn nacl back on for x86_64

* Thu Jul 21 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.82-2
- fix cups 2.2 support
- try to enable widevine compatibility (you still need to get the binary .so files from chrome)

* Thu Jul 21 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.82-1
- update to 52.0.2743.82
- handle locales properly
- cleanup spec

* Tue Jul 19 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.75-1
- update to 52.0.2743.75

* Wed Jul 6 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2743.60-1
- bump to 52.0.2743.60, disable nacl for now

* Mon May 9 2016 Tom Callaway <spot@fedoraproject.org> 52.0.2723.2-1
- force to dev to see if it works better on F24+

* Wed May 4 2016 Tom Callaway <spot@fedoraproject.org> 50.0.2661.94-6
- apply upstream fix for https://bugs.chromium.org/p/chromium/issues/detail?id=604534

* Tue May 3 2016 Tom Callaway <spot@fedoraproject.org> 50.0.2661.94-5
- use bundled re2 (conditionalize it)

* Tue May 3 2016 Tom Callaway <spot@fedoraproject.org> 50.0.2661.94-4
- disable asan (it never quite built)
- do not preserve re2 bundled tree, causes header/library mismatch

* Mon May 2 2016 Tom Callaway <spot@fedoraproject.org> 50.0.2661.94-3
- enable AddressSanize (ASan) for debugging

* Sat Apr 30 2016 Tom Callaway <spot@fedoraproject.org> 50.0.2661.94-2
- use bundled icu always. *sigh*

* Fri Apr 29 2016 Tom Callaway <spot@fedoraproject.org> 50.0.2661.94-1
- update to 50.0.2661.94

* Wed Apr 27 2016 Tom Callaway <spot@fedoraproject.org> 50.0.2661.86-1
- update to 50.0.2661.86

* Thu Mar 17 2016 Tom Callaway <spot@fedoraproject.org> 49.0.2623.87-4
- protect third_party/woff2

* Thu Mar 17 2016 Tom Callaway <spot@fedoraproject.org> 49.0.2623.87-3
- add BuildRequires: libffi-devel

* Thu Mar 17 2016 Tom Callaway <spot@fedoraproject.org> 49.0.2623.87-2
- explicitly disable sysroot

* Thu Mar 17 2016 Tom Callaway <spot@fedoraproject.org> 49.0.2623.87-1
- update to 49.0.2623.87

* Mon Feb 29 2016 Tom Callaway <spot@fedoraproject.org> 48.0.2564.116-3
- Happy Leap Day!
- add Requires: u2f-hidraw-policy for u2f token support
- add Requires: xorg-x11-server-Xvfb for chrome-remote-desktop

* Fri Feb 26 2016 Tom Callaway <spot@fedoraproject.org> 48.0.2564.116-2
- fix icu BR

* Wed Feb 24 2016 Tom Callaway <spot@fedoraproject.org> 48.0.2564.116-1
- Update to 48.0.2564.116
- conditionalize icu properly
- fix libusbx handling (bz1270324)

* Wed Feb 17 2016 Tom Callaway <spot@fedoraproject.org> 48.0.2564.103-2
- fixes for gcc6

* Mon Feb  8 2016 Tom Callaway <spot@fedoraproject.org> 48.0.2564.103-1
- update to 48.0.2564.103
- use bundled libsrtp (because upstream has coded themselves into an ugly corner)

* Fri Jan 22 2016 Tom Callaway <spot@fedoraproject.org> 48.0.2564.82-1
- update to 48.0.2564.82

* Fri Jan 15 2016 Tom Callaway <spot@fedoraproject.org> 47.0.2526.111-1
- update to 47.0.2526.111

* Thu Jan 07 2016 Tomas Popela <tpopela@redhat.com> 47.0.2526.106-2
- compare hashes when downloading the tarballs
- Google started to include the Debian sysroots in tarballs - remove them while
  processing the tarball
- add a way to not use the system display server for tests instead of Xvfb
- update the depot_tools checkout to get some GN fixes
- use the remove_bundled_libraries script
- update the clean_ffmpeg script to print errors when some files that we are
  processing are missing
- update the clean_ffmpeg script to operate on tarball's toplevel folder
- don't show comments as removed tests in get_linux_tests_names script
- rework the process_ffmpeg_gyp script (also rename it to
  get_free_ffmpeg_source_files) to use the GN files insted of GYP (but we still
  didn't switched to GN build)

* Wed Dec 16 2015 Tom Callaway <spot@fedoraproject.org> 47.0.2526.106-1
- update to 47.0.2526.106

* Tue Dec 15 2015 Tom Callaway <spot@fedoraproject.org> 47.0.2526.80-4
- entirely patch out the broken fd counter from the nacl loader code
  killing it with fire would be better, but then chromium is on fire
  and that somehow makes it worse.

* Mon Dec 14 2015 Tom Callaway <spot@fedoraproject.org> 47.0.2526.80-3
- revert nacl fd patch (now we see 6 fds! 6 LIGHTS!)

* Fri Dec 11 2015 Tom Callaway <spot@fedoraproject.org> 47.0.2526.80-2
- build everything shared, but when we do shared builds, make -libs subpackage
- make chrome-remote-desktop dep on -libs subpackage in shared builds

* Wed Dec  9 2015 Tom Callaway <spot@fedoraproject.org> 47.0.2526.80-1
- update to 47.0.2526.80
- only build ffmpeg shared, not any other libs
  this is because if we build the other libs shared, then our
  chrome-remote-desktop build deps on those libs and we do not want that

* Tue Dec  8 2015 Tom Callaway <spot@fedoraproject.org> 47.0.2526.73-2
- The nacl loader claims it sees 7 fds open ALL THE TIME, and fails
  So, we tell it that it is supposed to see 7.
  I suspect building with shared objects is causing this disconnect.

* Wed Dec  2 2015 Tom Callaway <spot@fedoraproject.org> 47.0.2526.73-1
- update to 47.0.2526.73
- rework chrome-remote-desktop subpackage to work for google-chrome and chromium

* Wed Dec  2 2015 Tomas Popela <tpopela@redhat.com> 47.0.2526.69-1
- Update to 47.0.2526.69

* Tue Dec  1 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.86-4
- still more remote desktop changes

* Mon Nov 30 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.86-3
- lots of remote desktop cleanups

* Thu Nov 12 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.86-2
- re-enable Requires/BuildRequires for libusbx
- add remote-desktop subpackage

* Wed Nov 11 2015 Tomas Popela <tpopela@redhat.com> 46.0.2490.86-1
- update to 46.0.2490.86
- clean the SPEC file
- add support for policies: https://www.chromium.org/administrators/linux-quick-start
- replace exec_mem_t SELinux label with bin_t - see rhbz#1281437
- refresh scripts that are used for processing the original tarball

* Fri Oct 30 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.80-5
- tls_edit is a nacl thing. who knew?

* Thu Oct 29 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.80-4
- more nacl fixups for i686 case

* Thu Oct 29 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.80-3
- conditionalize nacl/nonacl, disable nacl on i686, build for i686

* Mon Oct 26 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.80-2
- conditionalize shared bits (enable by default)

* Fri Oct 23 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.80-1
- update to 46.0.2490.80

* Thu Oct 15 2015 Tom Callaway <spot@fedoraproject.org> 46.0.2490.71-1
- update to 46.0.2490.71

* Thu Oct 15 2015 Tom Callaway <spot@fedoraproject.org> 45.0.2454.101-2
- fix icu handling for f21 and older

* Mon Oct  5 2015 Tom Callaway <spot@fedoraproject.org> 45.0.2454.101-1
- update to 45.0.2454.101

* Thu Jun 11 2015 Tom Callaway <spot@fedoraproject.org> 43.0.2357.124-1
- update to 43.0.2357.124

* Tue Jun  2 2015 Tom Callaway <spot@fedoraproject.org> 43.0.2357.81-1
- update to 43.0.2357.81

* Thu Feb 26 2015 Tom Callaway <spot@fedoraproject.org> 40.0.2214.115-1
- update to 40.0.2214.115

* Thu Feb 19 2015 Tom Callaway <spot@fedoraproject.org> 40.0.2214.111-1
- update to 40.0.2214.111

* Mon Feb  2 2015 Tom Callaway <spot@fedoraproject.org> 40.0.2214.94-1
- update to 40.0.2214.94

* Tue Jan 27 2015 Tom Callaway <spot@fedoraproject.org> 40.0.2214.93-1
- update to 40.0.2214.93

* Sat Jan 24 2015 Tom Callaway <spot@fedoraproject.org> 40.0.2214.91-1
- update to 40.0.2214.91

* Wed Jan 21 2015 Tom Callaway <spot@fedoraproject.org> 39.0.2171.95-3
- use bundled icu on Fedora < 21, we need 5.2

* Tue Jan  6 2015 Tom Callaway <spot@fedoraproject.org> 39.0.2171.95-2
- rebase off Tomas's spec file for Fedora

* Fri Dec 12 2014 Tomas Popela <tpopela@redhat.com> 39.0.2171.95-1
- Update to 39.0.2171.95
- Resolves: rhbz#1173448

* Wed Nov 26 2014 Tomas Popela <tpopela@redhat.com> 39.0.2171.71-1
- Update to 39.0.2171.71
- Resolves: rhbz#1168128

* Wed Nov 19 2014 Tomas Popela <tpopela@redhat.com> 39.0.2171.65-2
- Revert the chrome-sandbox rename to chrome_sandbox
- Resolves: rhbz#1165653

* Wed Nov 19 2014 Tomas Popela <tpopela@redhat.com> 39.0.2171.65-1
- Update to 39.0.2171.65
- Use Red Hat Developer Toolset for compilation
- Set additional SELinux labels
- Add more unit tests
- Resolves: rhbz#1165653

* Fri Nov 14 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.122-1
- Update to 38.0.2125.122
- Resolves: rhbz#1164116

* Wed Oct 29 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.111-1
- Update to 38.0.2125.111
- Resolves: rhbz#1158347

* Fri Oct 24 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.104-2
- Fix the situation when the return key (and keys from numpad) does not work
  in HTML elements with input
- Resolves: rhbz#1153988
- Dynamically determine the presence of the PepperFlash plugin
- Resolves: rhbz#1154118

* Thu Oct 16 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.104-1
- Update to 38.0.2125.104
- Resolves: rhbz#1153012

* Thu Oct 09 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.101-2
- The boringssl is used for tests, without the possibility of using
  the system openssl instead. Remove the openssl and boringssl sources
  when not building the tests.
- Resolves: rhbz#1004948

* Wed Oct 08 2014 Tomas Popela <tpopela@redhat.com> 38.0.2125.101-1
- Update to 38.0.2125.101
- System openssl is used for tests, otherwise the bundled boringssl is used
- Don't build with clang
- Resolves: rhbz#1004948

* Wed Sep 10 2014 Tomas Popela <tpopela@redhat.com> 37.0.2062.120-1
- Update to 37.0.2062.120
- Resolves: rhbz#1004948

* Wed Aug 27 2014 Tomas Popela <tpopela@redhat.com> 37.0.2062.94-1
- Update to 37.0.2062.94
- Include the pdf viewer library

* Wed Aug 13 2014 Tomas Popela <tpopela@redhat.com> 36.0.1985.143-1
- Update to 36.0.1985.143
- Use system openssl instead of bundled one
- Resolves: rhbz#1004948

* Thu Jul 17 2014 Tomas Popela <tpopela@redhat.com> 36.0.1985.125-1
- Update to 36.0.1985.125
- Add libexif as BR
- Resolves: rhbz#1004948

* Wed Jun 11 2014 Tomas Popela <tpopela@redhat.com> 35.0.1916.153-1
- Update to 35.0.1916.153
- Resolves: rhbz#1004948

* Wed May 21 2014 Tomas Popela <tpopela@redhat.com> 35.0.1916.114-1
- Update to 35.0.1916.114
- Bundle python-argparse
- Resolves: rhbz#1004948

* Wed May 14 2014 Tomas Popela <tpopela@redhat.com> 34.0.1847.137-1
- Update to 34.0.1847.137
- Resolves: rhbz#1004948

* Mon May 5 2014 Tomas Popela <tpopela@redhat.com> 34.0.1847.132-1
- Update to 34.0.1847.132
- Bundle depot_tools and switch from make to ninja
- Remove PepperFlash
- Resolves: rhbz#1004948

* Mon Feb 3 2014 Tomas Popela <tpopela@redhat.com> 32.0.1700.102-1
- Update to 32.0.1700.102

* Thu Jan 16 2014 Tomas Popela <tpopela@redhat.com> 32.0.1700.77-1
- Update to 32.0.1700.77
- Properly kill Xvfb when tests fails
- Add libdrm as BR
- Add libcap as BR

* Tue Jan 7 2014 Tomas Popela <tpopela@redhat.com> 31.0.1650.67-2
- Minor changes in spec files and scripts
- Add Xvfb as BR for tests
- Add policycoreutils-python as Requires
- Compile unittests and run them in chech phase, but turn them off by default
  as many of them are failing in Brew

* Thu Dec 5 2013 Tomas Popela <tpopela@redhat.com> 31.0.1650.67-1
- Update to 31.0.1650.63

* Thu Nov 21 2013 Tomas Popela <tpopela@redhat.com> 31.0.1650.57-1
- Update to 31.0.1650.57

* Wed Nov 13 2013 Tomas Popela <tpopela@redhat.com> 31.0.1650.48-1
- Update to 31.0.1650.48
- Minimal supported RHEL6 version is now RHEL 6.5 due to GTK+

* Fri Oct 25 2013 Tomas Popela <tpopela@redhat.com> 30.0.1599.114-1
- Update to 30.0.1599.114
- Hide the infobar with warning that this version of OS is not supported
- Polished the chromium-latest.py

* Thu Oct 17 2013 Tomas Popela <tpopela@redhat.com> 30.0.1599.101-1
- Update to 30.0.1599.101
- Minor changes in scripts

* Wed Oct 2 2013 Tomas Popela <tpopela@redhat.com> 30.0.1599.66-1
- Update to 30.0.1599.66
- Automated the script for cleaning the proprietary sources from ffmpeg.

* Thu Sep 19 2013 Tomas Popela <tpopela@redhat.com> 29.0.1547.76-1
- Update to 29.0.1547.76
- Added script for removing the proprietary sources from ffmpeg. This script is called during cleaning phase of ./chromium-latest --rhel

* Mon Sep 16 2013 Tomas Popela <tpopela@redhat.com> 29.0.1547.65-2
- Compile with Dproprietary_codecs=0 and Dffmpeg_branding=Chromium to disable proprietary codecs (i.e. MP3)

* Mon Sep 9 2013 Tomas Popela <tpopela@redhat.com> 29.0.1547.65-1
- Initial version based on Tom Callaway's <spot@fedoraproject.org> work

