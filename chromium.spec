#%define pnacl_version 11986
#%define newlib_version 11958
#%define glibc_version 11958

Summary:	A fast webkit-based web browser
Name:		chromium
Version:	34.0.1847.116
Release:	6%{?dist}
Epoch:		1

Group:		Applications/Internet
License:	BSD, LGPL
URL:		http://www.chromium.org/

Source0:	https://commondatastorage.googleapis.com/chromium-browser-official/%{name}-%{version}.tar.xz
#Source1:        http://gsdview.appspot.com/nativeclient-archive2/x86_toolchain/r%{glibc_version}/toolchain_linux_x86.tar.bz2
#Source2:        http://gsdview.appspot.com/nativeclient-archive2/toolchain/%{newlib_version}/naclsdk_linux_x86.tgz
#Source3:        http://gsdview.appspot.com/nativeclient-archive2/toolchain/%{pnacl_version}/naclsdk_pnacl_linux_x86.tgz
#Source4:        http://gsdview.appspot.com/nativeclient-archive2/toolchain/%{pnacl_version}/naclsdk_pnacl_translator.tgz

Source10:	chromium-wrapper
Source20:	chromium-browser.desktop
Source30:	master_preferences
Source31:	default_bookmarks.html
Source32:	chromium.default

Source997:	depot_tools.tar.xz
Source998:	gn-binaries.tar.xz

Provides:	chromium-stable
Conflicts:	chromium-testing
Conflicts:	chromium-unstable

Patch0:		chromium-30.0.1599.66-master-prefs-path.patch

# PATCH-FIX-OPENSUSE Disable the download of the NaCl tarballs
Patch12:         no-download-nacl.diff
# PATCH-FIX-OPENSUSE patches in system glew library
Patch13:	chromium-25.0.1364.172-system-glew.patch
# PATCH-FIX-OPENSUSE removes build part for courgette
Patch14:	chromium-25.0.1364.172-no-courgette.patch
# PATCH-FIX-OPENSUSE Compile the sandbox with -fPIE settings
Patch15:	chromium-25.0.1364.172-sandbox-pie.patch

# Fix https://codereview.chromium.org/142853004/
Patch30:	issue142853004_80001_90001.diff

BuildRequires:	alsa-lib-devel
BuildRequires:	atk-devel
BuildRequires:	bison
BuildRequires:	bzip2-devel
BuildRequires:	cups-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	elfutils-devel
BuildRequires:	expat-devel
BuildRequires:	flac-devel
BuildRequires:	flex
BuildRequires:	glib2-devel
BuildRequires:	gyp
%if 0%{?fedora} >= 20
BuildRequires:	ninja-build
%endif
BuildRequires:	gperf
BuildRequires:	gtk2-devel
BuildRequires:	libXScrnSaver-devel
BuildRequires:	libXt-devel
BuildRequires:	libXtst-devel
BuildRequires:	libevent-devel
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libpng-devel
BuildRequires:	libudev-devel
BuildRequires:	libvpx-devel
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	mesa-libGL-devel
BuildRequires:	mesa-libGLU-devel
BuildRequires:	nspr-devel
BuildRequires:	nss-devel
BuildRequires:	openssl-devel
BuildRequires:	perl(Switch)
BuildRequires:	perl(Digest::MD5)
%if 0%{?fedora} >= 19
BuildRequires:	perl-Text-ParseWords
%endif
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	speex-devel
BuildRequires:	subversion
BuildRequires:	zlib-devel
%if 0%{?fedora} < 18
BuildRequires:	libusb-devel
BuildRequires:	gstreamer-plugins-base-devel gstreamer-devel
%else
BuildRequires:	libusbx-devel
BuildRequires:	gstreamer1-plugins-base-devel gstreamer1-devel
%endif
BuildRequires:	libexif-devel
BuildRequires:	speech-dispatcher-devel
BuildRequires:	gpsd-devel
BuildRequires:	libsrtp-devel
BuildRequires:	libmtp-devel
BuildRequires:	libwebp-devel
BuildRequires:	libicu-devel
BuildRequires:	minizip-devel
BuildRequires:	yasm-devel
BuildRequires:	opus-devel
BuildRequires:	pciutils-devel
BuildRequires:	v8-devel
#BuildRequires:	sqlite-devel
BuildRequires:	harfbuzz-devel
BuildRequires:	GConf2-devel
#BuildRequires:  pkgconfig(protobuf)
BuildRequires:  libcap-devel

%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
BuildRequires:	libgnome-keyring-devel
%else
BuildRequires:	gnome-keyring-devel
%endif

# NaCl needs these
#%ifarch x86_64
#BuildRequires:	/lib/libc.so.6
#BuildRequires:	/lib/libz.so.1
#BuildRequires:	/lib/libgcc_s.so.1
#%endif

Requires:	hicolor-icon-theme

Obsoletes:	chromium-ffmpeg

ExclusiveArch: i686 x86_64 armv7l

%description
Chromium is a browser that combines a minimal design with sophisticated
technology to make the web faster, safer, and easier.

This is the stable channel Chromium browser. It offers a rock solid
browser which is updated with features and fixes once they have been
thoroughly tested. If you want the latest features, install the
chromium-browser-unstable package instead.

Note: If you are reverting from unstable to stable or beta channel, you may
experience tab crashes on startup. This crash only affects tabs restored
during the first launch due to a change in how tab state is stored.
See http://bugs.chromium.org/34688. It's always a good idea to back up
your profile before changing channels.


%package -n chromedriver
Summary:	WebDriver for Google Chrome/Chromium
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:	chromedriver-stable
Conflicts:	chromedriver-testing
Conflicts:	chromedriver-unstable

%description -n chromedriver
WebDriver is an open source tool for automated testing of webapps across many
browsers. It provides capabilities for navigating to web pages, user input,
JavaScript execution, and more. ChromeDriver is a standalone server which
implements WebDriver's wire protocol for Chromium. It is being developed by
members of the Chromium and WebDriver teams.


%prep
%setup -q -a 998 -a 997
%patch0 -p1 -b .master-prefs

# openSUSE patches
#%patch12 -p0
%patch13 -p1
%patch14 -p1
%patch15 -p1

%patch30 -p1

sed -i 's|icu)|icu-i18n)|g' build/linux/system.gyp

## Install the Native Client tarballs to the right location
#mkdir -p native_client/toolchain/.tars
#cp %{SOURCE1} native_client/toolchain/.tars/
#cp %{SOURCE2} native_client/toolchain/.tars/
#cp %{SOURCE3} native_client/toolchain/.tars/
#cp %{SOURCE4} native_client/toolchain/.tars/

## Extract the NaCl tarballs 
#python ./build/download_nacl_toolchains.py --no-arm-trusted --keep

# Hard code extra version
FILE=chrome/common/chrome_version_info_posix.cc
sed -i.orig -e 's/getenv("CHROME_VERSION_EXTRA")/"Russian Fedora"/' $FILE
cmp $FILE $FILE.orig && exit 1

%ifarch x86_64
sed -i "s#/lib/#/lib64/#g" %{SOURCE20}
%endif

%ifarch i686
sed -i "s#/lib64/#/lib/#g" %{SOURCE20}
%endif

%build
%if 0%{?fedora} >= 20
export GYP_GENERATORS='ninja'
./build/gyp_chromium build/all.gyp --depth=. \
%else
export GYP_GENERATORS='ninja'
./build/gyp_chromium build/all.gyp -f make --depth=. \
%endif
        -D linux_sandbox_path=%{_libdir}/%{name}/chrome-sandbox \
	-D linux_sandbox_chrome_path=%{_libdir}/%{name}/chrome \
	-D linux_link_gnome_keyring=0 \
	-D werror='' \
	-D use_system_sqlite=0 \
	-D use_system_libxml=1 \
	-D use_system_zlib=1 \
	-D use_system_bzip2=1 \
	-D use_system_libbz2=1 \
	-D use_system_libpng=1 \
	-D use_system_libjpeg=1 \
	-D use_system_libevent=1 \
	-D use_system_flac=1 \
	-D use_system_vpx=1 \
	-D use_system_speex=1 \
	-D use_system_libusb=1 \
	-D use_system_libexif=1 \
	-D use_system_libsrtp=1 \
	-D use_system_libmtp=1 \
	-D use_system_opus=1 \
	-D use_system_libwebp=1 \
	-D use_system_harfbuzz=1 \
	-D use_system_minizip=1 \
	-D use_system_yasm=1 \
	-D use_system_xdg_utils=1 \
	-D build_ffmpegsumo=1 \
	-D use_system_ffmpeg=0 \
        -D ffmpeg_branding=Chrome \
	-D proprietary_codecs=1 \
	-D use_pulseaudio=1 \
	-D use_system_v8=1 \
	-D use_system_nspr=1 \
	-D use_system_libxslt=1 \
	-D use_system_protobuf=0 \
	-D use_system_libyuv=1 \
	-D linux_link_libpci=1 \
	-D linux_link_gsettings=1 \
	-D linux_link_libspeechd=1 \
	-D linux_link_kerberos=1 \
	-D linux_link_libgps=1 \
	-D linux_fpic=1 \
	-D disable_nacl=1 \
        -D disable_glibc=0 \
        -D disable_pnacl=1 \
        -D disable_newlib_untar=0 \
	-D logging_like_official_build=1 \
	-D remove_webcore_debug_symbols=1 \
	-D use_aura=1 \
%if 0%{?fedora} > 19        
        -Dlinux_link_libspeechd=1 \
        -Dlibspeechd_h_prefix=speech-dispatcher/ \
%endif
        -Dgoogle_api_key='AIzaSyD1hTe85_a14kr1Ks8T3Ce75rvbR1_Dx7Q' \
	-Dgoogle_default_client_id='4139804441.apps.googleusercontent.com' \
	-Dgoogle_default_client_secret='KDTRKEZk2jwT_7CDpcmMA--P' \
%if %{defined rhel} && 0%{?rhel} < 7
	-D v8_use_snapshot=false \
%endif
	-D javascript_engine=v8 \
%if 0%{?fedora} >= 20
	-D use_system_icu=0 \
%else
	-D use_system_icu=1 \
%endif
%ifarch i686
	-D disable_sse2=1 \
	-D release_extra_cflags="-march=i686"
%endif
%ifarch armv7l
	-D target_arch=arm \
	-D linux_use_tcmalloc=0 \
	-D armv7=1 \
	-D release_extra_cflags="-marm"
%endif


%if 0%{?fedora} >= 20
mkdir -p out/Release

ninja-build -C out/Release chrome
# Build the required SUID_SANDBOX helper
ninja-build -C out/Release chrome_sandbox
# Build the ChromeDriver test suite
ninja-build -C out/Release chromedriver
%else
make %{_smp_mflags} chrome chrome_sandbox chromedriver BUILDTYPE=Release
%endif

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/%{name}/locales
mkdir -p %{buildroot}%{_libdir}/%{name}/themes
mkdir -p %{buildroot}%{_libdir}/%{name}/default_apps
mkdir -p %{buildroot}%{_mandir}/man1
install -m 755 %{SOURCE10} %{buildroot}%{_libdir}/%{name}/
install -m 755 out/Release/chrome %{buildroot}%{_libdir}/%{name}/
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{_libdir}/%{name}/chrome-sandbox
cp -a out/Release/chromedriver %{buildroot}%{_libdir}/%{name}/chromedriver
install -m 644 out/Release/chrome.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -m 644 out/Release/*.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/icudtl.dat %{buildroot}%{_libdir}/%{name}/
install -m 755 out/Release/libffmpegsumo.so %{buildroot}%{_libdir}/%{name}/
#%ifnarch armv7l
#install -m 755 out/Release/libppGoogleNaClPluginChrome.so %{buildroot}%{_libdir}/%{name}/
#install -m 755 out/Release/nacl_helper_bootstrap %{buildroot}%{_libdir}/%{name}/
#install -m 755 out/Release/nacl_helper %{buildroot}%{_libdir}/%{name}/
#install -m 644 out/Release/nacl_irt_*.nexe %{buildroot}%{_libdir}/%{name}/
#%endif
install -m 644 out/Release/locales/*.pak %{buildroot}%{_libdir}/%{name}/locales/
install -m 644 out/Release/chrome_100_percent.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/content_resources.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/resources.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 chrome/browser/resources/default_apps/* %{buildroot}%{_libdir}/%{name}/default_apps/

# install wrapper
ln -s %{_libdir}/%{name}/chromium-wrapper %{buildroot}%{_bindir}/%{name}
sed -i "s!@LIBDIR@!%{_libdir}!g" %{buildroot}%{_libdir}/%{name}/chromium-wrapper

ln -s %{_libdir}/%{name}/chromedriver %{buildroot}%{_bindir}/chromedriver

# create global config file
mkdir -p %{buildroot}%{_sysconfdir}/default
install -m644 %{SOURCE32} %{buildroot}%{_sysconfdir}/default/%{name}

# create pepper dir. talkplugin works fine only if sylinks in pepper
mkdir -p %{buildroot}%{_libdir}/%{name}/pepper

find out/Release/resources/ -name "*.d" -exec rm {} \;
cp -r out/Release/resources %{buildroot}%{_libdir}/%{name}

# desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{SOURCE20} %{buildroot}%{_datadir}/applications/

# icon
for i in 22 24 48 64 128 256; do
	mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
	install -m 644 chrome/app/theme/chromium/product_logo_$i.png \
		%{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

# Install the master_preferences file
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 %{SOURCE30} %{buildroot}%{_sysconfdir}/%{name}/
install -m 0644 %{SOURCE31} %{buildroot}%{_sysconfdir}/%{name}/


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

if [ -e /opt/google/talkplugin/libppgoogletalk.so ]; then
    if [ ! -e %{_libdir}/%{name}/pepper/libppgoogletalk.so ]; then
        ln -s /opt/google/talkplugin/libppgoogletalk.so \
		%{_libdir}/%{name}/pepper/libppgoogletalk.so
    fi
fi

if [ -e /opt/google/talkplugin/libppo1d.so ]; then
    if [ ! -e %{_libdir}/%{name}/pepper/libppo1d.so ]; then
        ln -s /opt/google/talkplugin/libppo1d.so \
                %{_libdir}/%{name}/pepper/libppo1d.so
    fi
fi

%preun
if [ $1 -eq 0 ] ; then
    if [ -e %{_libdir}/%{name}/pepper/libppo1d.so ]; then
        rm -f %{_libdir}/%{name}/pepper/libppo1d.so
    fi

    if [ -e %{_libdir}/%{name}/pepper/libppgoogletalk.so ]; then
        rm -f %{_libdir}/%{name}/pepper/libppgoogletalk.so
    fi

fi


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%defattr(-,root,root,-)
%doc LICENSE AUTHORS
%config %{_sysconfdir}/%{name}
%config %{_sysconfdir}/default/%{name}
%{_bindir}/%{name}
%{_libdir}/%{name}/chromium-wrapper
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/chrome-sandbox
%{_libdir}/%{name}/libffmpegsumo.so
#%ifnarch armv7l
#%{_libdir}/%{name}/libppGoogleNaClPluginChrome.so
#%{_libdir}/%{name}/nacl_helper_bootstrap
#%{_libdir}/%{name}/nacl_helper
#%{_libdir}/%{name}/nacl_irt_*.nexe
#%endif
%{_libdir}/%{name}/locales
%{_libdir}/%{name}/chrome_100_percent.pak
%{_libdir}/%{name}/content_resources.pak
%{_libdir}/%{name}/keyboard_resources.pak
%{_libdir}/%{name}/resources.pak
%{_libdir}/%{name}/icudtl.dat
%{_libdir}/%{name}/resources
%{_libdir}/%{name}/themes
%{_libdir}/%{name}/default_apps
%dir %{_libdir}/%{name}/pepper
%{_mandir}/man1/%{name}*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png


%files -n chromedriver
%defattr(-,root,root,-)
%doc LICENSE AUTHORS
%{_bindir}/chromedriver
%{_libdir}/%{name}/chromedriver


%changelog
* Wed Apr 23 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 34.0.1847.116-6.R
- build with ninja
- use new run wapper and default file

* Tue Apr 22 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 34.0.1847.116-5.R
- rebuilt

* Tue Apr 22 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 34.0.1847.116-4.R
- disable system protobuf. It crashes browser

* Tue Apr 15 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 34.0.1847.116-3.R
- build with enabled aura

* Thu Apr 10 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 34.0.1847.116-2.R
- install icudtl.dat to avoid segfault
- clean up spec

* Tue Apr  8 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 34.0.1847.116-1.R
- update to 34.0.1847.116

* Wed Mar  5 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 33.0.1750.146-1.R
- update to 32.0.1750.146

* Mon Feb 24 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 33.0.1750.117-1.R
- update to 32.0.1750.117

* Thu Feb 20 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 33.0.1750.115-1.R
- update to 32.0.1750.115

* Wed Feb 19 2014 Arkady L. Shane <ashejn@russianfedora.ru> - 32.0.1700.107-1.R
- update to 32.0.1700.107

* Wed Jan 29 2014 Arkady L. Shane <ashejn@russianfedora.ru> - 32.0.1700.102-1.R
- update to 32.0.1700.102

* Wed Jan 15 2014 Arkady L. Shane <ashejn@russianfedora.ru> - 32.0.1700.76-1.R
- update to 32.0.1700.76

* Thu Dec  5 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 31.0.1650.63-1.R
- update to 31.0.1650.63

* Thu Nov 14 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 31.0.1650.48-1.R
- update to 31.0.1650.48

* Thu Oct 31 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 30.0.1599.114-1.R
- update to 30.0.1599.114

* Wed Sep  4 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 29.0.1547.65-1.R
- update to 29.0.1547.65

* Mon Sep  2 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 29.0.1547.62-1.R
- update to 29.0.1547.62

* Thu Aug 22 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 29.0.1547.57-1.R
- update to 29.0.1547.57

* Wed Jul 31 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 28.0.1500.95-1.R
- update to 28.0.1500.95

* Wed Jul 10 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 28.0.1500.71-1.R
- update to 28.0.1500.71

* Fri Jun 21 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 28.0.1500.52-1.R
- update to 28.0.1500.52

* Wed Jun 19 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 28.0.1500.45-1.R
- update to 28.0.1500.45

* Sat Jun  8 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 27.0.1453.110-1.R
- update to 27.0.1453.110

* Thu May 23 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 27.0.1453.93-1.R
- update to 27.0.1453.93
- drop old glibc patch
- update master pref patch
- added BR: perl-Text-ParseWords for fedora >= 19

* Tue Apr 23 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 26.0.1410.63-2.R
- new harfbuzz still broken. Build with internal

* Mon Apr 22 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 26.0.1410.63-1.R
- update to 26.0.1410.63

* Wed Apr 17 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 26.0.1410.46-2.R
- fix crash (https://bugs.webkit.org/show_bug.cgi?id=110145)

* Wed Mar 27 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 26.0.1410.46-1.R
- update to 26.0.1410.46

* Mon Mar 25 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 25.0.1364.172-3.R
- apply many openSUSE patches and fixed webm/html5 playing (in youtube)
- build with internal zlib
- build with system libbz2
- do no use system v8 and ffmpeg options defined

* Fri Mar 22 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 25.0.1364.172-2.R
- do not build proprietary codecs as they break webm
- added BR: libusbx-devel and drop libusb-devel

* Tue Mar 19 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 25.0.1364.172-1.R
- update to 25.0.1364.172

* Mon Mar 11 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 25.0.1364.160-1.R
- update to 25.0.1364.160

* Sat Feb 23 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 25.0.1364.97-3.R
- rebuilt with internal png and system jpeg
- fix "Uncaught exception" in 2 calls to webkitTransform
- fix "Unable to set period time" alsa error, taken from chromiumOS

* Sat Feb 23 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 25.0.1364.97-2.R
- rebuilt with internal jpeg

* Fri Feb 22 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 25.0.1364.97-1.R
- update to 25.0.1364.97
- enable many new build options

* Tue Feb  5 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 24.0.1312.68-1.R
- update to 24.0.1312.68

* Wed Jan 23 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 24.0.1312.56-1.R
- update to 24.0.1312.56

* Fri Jan 11 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 24.0.1312.52-1.R
- update to 24.0.1312.52

* Fri Dec 21 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 23.0.1271.97-4.R
- added epoch to requires for chromedriver

* Mon Dec 17 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 23.0.1271.97-3.R
- create separate package for chromedriver

* Thu Dec 13 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 23.0.1271.97-2.R
- rebuild with ChromeDriver

* Wed Dec 12 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 23.0.1271.97-1.R
- update to 23.0.1271.97

* Sun Dec  2 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 23.0.1271.95-1.R
- update to 23.0.1271.95

* Tue Nov 27 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 23.0.1271.91-1.R
- update to 23.0.1271.91

* Wed Nov  7 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 23.0.1271.64-1.R
- update to 23.0.1271.64

* Mon Oct 22 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 22.0.1229.92-2.R
- build with internal libxml

* Tue Oct  9 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 22.0.1229.92-1.R
- update to 22.0.1229.92

* Thu Sep 27 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 22.0.1229.79-2.R
- pack new resource files

* Wed Sep 26 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 22.0.1229.79-1.R
- update to 22.0.1229.79
- turn off system zlib
  (http://code.google.com/p/chromium/issues/detail?id=143623)

* Thu Sep 20 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 21.0.1180.89-1.R
- update to 21.0.1180.89

* Thu Aug  9 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 21.0.1180.75-1.R
- update to 21.0.1180.75

* Wed Aug  1 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 21.0.1180.57-1.R
- update to 21.0.1180.57
- drop old patches

* Thu Jul 12 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 20.0.1132.57-1.R
- update to last stable 20.0.11.32.57

* Wed Jul 11 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 20.0.1132.47-3.R
- added O: chromium-ffmpeg

* Tue Jul 10 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 20.0.1132.47-2.R
- fix trouble with glibe 2.16 (is136023)
  http://code.google.com/p/chromium/issues/detail?id=136023

* Mon Jul  9 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 20.0.1132.47-1.R
- apply patch for getting bookmarks and preferences
- patch for gcc47
- many new build requires
- apply sqlite memory leak patch

* Sat Jun 30 2012 Andrew Wyatt <andrew@fuduntu.org> - 20.0.1132.47-1
- New upstream stable release

* Thu Jun 28 2012 Andrew Wyatt <andrew@fuduntu.org> - 20.0.1132.43-2
- New upstream stable release

* Sat Jun 09 2012 Andrew Wyatt <andrew@fuduntu.org> - 19.0.1084.56-1
- New upstream stable release

* Sun Jun 03 2012 Andrew Wyatt <andrew@fuduntu.org> - 19.0.1084.53-1
- New upstream stable release

* Tue May 15 2012 Andrew Wyatt <andrew@fuduntu.org> - 19.0.1084.47-1
- New upstream stable release (Chrome 19)
- Drop patch	chromium-16.0.912.32-include-glib.patch
		chromium-17.0.963.12-remove-inline.patch

* Sat May 12 2012 Andrew Wyatt <andrew@fuduntu.org> - 18.0.1025.168-1
- New upstream stable release

* Fri Apr 20 2012 Andrew Wyatt <andrew@fuduntu.org> - 18.0.1025.165-1
- New upstream stable release

* Wed Mar 07 2012 Andrew Wyatt <andrew@fuduntu.org> - 17.0.963.65-1
- Built for Fuduntu

* Tue Mar 06 2012 Claudio Matsuoka <claudio@mandriva.com> 17.0.963.65-1mdv2010.1
+ Revision: 782481
- new upstream release 17.0.963.65 (124686)
- move chromium 17 from beta to stable

* Thu Jan 26 2012 Claudio Matsuoka <claudio@mandriva.com> 16.0.912.77-1
+ Revision: 769167
- fix required package names
- new upstream release 16.0.912.77 (118311)
  * [106484] High CVE-2011-3924: Use-after-free in DOM selections
  * [107182] Critical CVE-2011-3925: Use-after-free in Safe Browsing navigation
  * [108461] High CVE-2011-3928: Use-after-free in DOM handling
  * [108605] High CVE-2011-3927: Uninitialized value in Skia
  * [109556] High CVE-2011-3926: Heap-buffer-overflow in tree builder

* Fri Jan 06 2012 Claudio Matsuoka <claudio@mandriva.com> 16.0.912.75-1
+ Revision: 758280
- new upstream release 16.0.912.75 (116452)
  * [106672] High CVE-2011-3921: Use-after-free in animation frames.
  * [107128] High CVE-2011-3919: Heap-buffer-overflow in libxml.
  * [108006] High CVE-2011-3922: Stack-buffer-overflow in glyph handling.
- detailed changelog: http://goo.gl/n2A6J

* Wed Dec 14 2011 Claudio Matsuoka <claudio@mandriva.com> 16.0.912.63-1
+ Revision: 741173
- fix libxt-devel package name in requires
- fix cups-devel package name in requires
- new upstream release 16.0.912.63 (113337)
- security fixes
  * [81753] Medium CVE-2011-3903: Out-of-bounds read in regex matching.
  * [95465] Low CVE-2011-3905: Out-of-bounds reads in libxml.
  * [98809] Medium CVE-2011-3906: Out-of-bounds read in PDF parser.
  * [99016] High CVE-2011-3907: URL bar spoofing with view-source.
  * [100863] Low CVE-2011-3908: Out-of-bounds read in SVG parsing.
  * [101010] Medium CVE-2011-3909: [64-bit only] Memory corruption in CSS
    property array.
  * [101494] Medium CVE-2011-3910: Out-of-bounds read in YUV video frame
    handling.
  * [101779] Medium CVE-2011-3911: Out-of-bounds read in PDF.
  * [102359] High CVE-2011-3912: Use-after-free in SVG filters.
  * [103921] High CVE-2011-3913: Use-after-free in Range handling.
  * [104011] High CVE-2011-3914: Out-of-bounds write in v8 i18n handling.
  * [104529] High CVE-2011-3915: Buffer overflow in PDF font handling.
  * [104959] Medium CVE-2011-3916: Out-of-bounds reads in PDF cross references.
  * [105162] Medium CVE-2011-3917: Stack-buffer-overflow in FileWatcher.
  * [107258] High CVE-2011-3904: Use-after-free in bidi handling.
- move chromium 16 to stable
- fix elfutils-devel package name in requires

* Sat Nov 12 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.120-1
+ Revision: 730285
- only include glib.h directly

* Wed Oct 26 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.106-1
+ Revision: 707420
- new upstream release 15.0.874.106 (107270)
  * fixes login issues to Barrons Online and The Wall Street Journal

* Tue Oct 25 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.102-1
+ Revision: 707191
- new upstream release 15.0.874.102 (106587)
  * [86758] High CVE-2011-2845: URL bar spoof in history handling.
  * [88949] Medium CVE-2011-3875: URL bar spoof with drag+drop of URLs.
  * [90217] Low CVE-2011-3876: Avoid stripping whitespace at the end of
    download filenames.
  * [91218] Low CVE-2011-3877: XSS in appcache internals page.
  * [94487] Medium CVE-2011-3878: Race condition in worker process
    initialization.
  * [95374] Low CVE-2011-3879: Avoid redirect to chrome scheme URIs.
  * [95992] Low CVE-2011-3880: Don't permit as a HTTP header delimiter.
  * [96047][96885][98053][99512][99750] High CVE-2011-3881: Cross-origin
    policy violations.
  * [96292] High CVE-2011-3882: Use-after-free in media buffer handling.
  * [96902] High CVE-2011-3883: Use-after-free in counter handling.
  * [97148] High CVE-2011-3884: Timing issues in DOM traversal.
  * [97599][98064][98556][99294][99880][100059] High CVE-2011-3885: Stale
    style bugs leading to use-after-free.
  * [98773][99167] High CVE-2011-3886: Out of bounds writes in v8.
  * [98407] Medium CVE-2011-3887: Cookie theft with javascript URIs.
  * [99138] High CVE-2011-3888: Use-after-free with plug-in and editing.
  * [99211] High CVE-2011-3889: Heap overflow in Web Audio.
  * [99553] High CVE-2011-3890: Use-after-free in video source handling.
  * [100332] High CVE-2011-3891: Exposure of internal v8 functions.
- move Chromium 15 from beta to stable
- remove Chromium 14
- add support to armv7l
- new upstream release 14.0.835.202 (103287)
- security fixes:
  * [93788] High CVE-2011-2876: Use-after-free in text line box handling
  * [95072] High CVE-2011-2877: Stale font in SVG text handling
  * [95671] High CVE-2011-2878: Inappropriate cross-origin access to the
    window prototype
  * [96150] High CVE-2011-2879: Lifetime and threading issues in audio node
    handling
  * [97451] [97520] [97615] High CVE-2011-2880: Use-after-free in the v8
    bindings
  * [97784] High CVE-2011-2881: Memory corruption with v8 hidden objects
  * [98089] Critical CVE-2011-3873: Memory corruption in shader translator
- detailed changelog at http://goo.gl/4dBM1
- new upstream release 14.0.835.186 (101821)

* Sat Sep 17 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.835.163-1
+ Revision: 700172
- new upstream release 14.0.835.163 (101024)
- security fixes:
  * [49377] High CVE-2011-2835: Race condition in the certificate cache
  * [57908] Low CVE-2011-2837: Use PIC / pie compiler flags
  * [75070] Low CVE-2011-2838: Treat MIME type more authoritatively when
    loading plug-ins
  * [76771] High CVE-2011-2839: Crash in v8 script object wrappers
  * [78427] [83031] Low CVE-2011-2840: Possible URL bar spoofs with unusual
    user interaction
  * [78639] High CVE-2011-2841: Garbage collection error in PDF
  * [82438] Medium CVE-2011-2843: Out-of-bounds read with media buffers
  * [85041] Medium CVE-2011-2844: Out-of-bounds read with mp3 files
  * [$1000] [89219] High CVE-2011-2846: Use-after-free in unload event handling
  * [$1000] [89330] High CVE-2011-2847: Use-after-free in document loader
  * [89564] Medium CVE-2011-2848: URL bar spoof with forward button
  * [89795] Low CVE-2011-2849: Browser NULL pointer crash with WebSockets
  * [89991] Medium CVE-2011-3234: Out-of-bounds read in box handling
  * [90134] Medium CVE-2011-2850: Out-of-bounds read with Khmer characters
  * [90173] Medium CVE-2011-2851: Out-of-bounds read in video handling
  * [91120] High CVE-2011-2852: Off-by-one in v8
  * [91197] High CVE-2011-2853: Use-after-free in plug-in handling
  * [92651] [94800] High CVE-2011-2854: Use-after-free in ruby / table style
    handing
  * [92959] High CVE-2011-2855: Stale node in stylesheet handling
  * [93416] High CVE-2011-2856: Cross-origin bypass in v8
  * [93420] High CVE-2011-2857: Use-after-free in focus controller
  * [93472] High CVE-2011-2834: Double free in libxml XPath handling
  * [93497] Medium CVE-2011-2859: Incorrect permissions assigned to
    non-gallery pages
  * [93587] High CVE-2011-2860: Use-after-free in table style handling
  * [93596] Medium CVE-2011-2861: Bad string read in PDF
  * [93906] High CVE-2011-2862: Unintended access to v8 built-in objects
  * [95563] Medium CVE-2011-2864: Out-of-bounds read with Tibetan characters
  * [95625] Medium CVE-2011-2858: Out-of-bounds read with triangle arrays
  * [95917] Low CVE-2011-2874: Failure to pin a self-signed cert for a session
  * [95920] High CVE-2011-2875: Type confusion in v8 object sealing
- detailed changelog at http://goo.gl/6B1kT
- copy release 14.0.835.163 from beta to stable

* Sun Sep 04 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.782.220-1
+ Revision: 698257
- new upstream release 13.0.782.220 (99552)
  * revoking trust for SSL certificates issued by DigiNotar-controlled
    intermediate CAs used by the Dutch PKIoverheid program

* Tue Aug 23 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.782.215-1
+ Revision: 696339
- add fix for tcmalloc build in cooker
- new upstream release 13.0.782.215 (97094)
- security fixes:
  * [82552] High CVE-2011-2823: Use-after-free in line box handling
  * [88216] High CVE-2011-2824: Use-after-free with counter nodes
  * [88670] High CVE-2011-2825: Use-after-free with custom fonts
  * [89402] High CVE-2011-2821: Double free in libxml XPath handling
  * [87453] High CVE-2011-2826: Cross-origin violation with empty origins
  * [90668] High CVE-2011-2827: Use-after-free in text searching
  * [91517] High CVE-2011-2828: Out-of-bounds write in v8
  * [32-bit only] [91598] High CVE-2011-2829: Integer overflow in uniform
    arrays
- detailed changelog at http://goo.gl/Lzn1m
- new upstream release 13.0.782.112 (95650)
- move release 13.0.782.107 (94237) from beta to stable
- security fixes:
  * [78841] High CVE-2011-2359: Stale pointer due to bad line box tracking
    in rendering.
  * [79266] Low CVE-2011-2360: Potential bypass of dangerous file prompt.
  * [79426] Low CVE-2011-2361: Improve designation of strings in the basic
    auth dialog.
  * [81307] Medium CVE-2011-2782: File permissions error with drag and drop.
  * [83273] Medium CVE-2011-2783: Always confirm a developer mode NPAPI
    extension install via a browser dialog.
  * [83841] Low CVE-2011-2784: Local file path disclosure via GL program log.
  * [84402] Low CVE-2011-2785: Sanitize the homepage URL in extensions.
  * [84600] Low CVE-2011-2786: Make sure the speech input bubble is always
    on-screen.
  * [84805] Medium CVE-2011-2787: Browser crash due to GPU lock re-entrancy
    issue.
  * [85559] Low CVE-2011-2788: Buffer overflow in inspector serialization.
  * [85808] Medium CVE-2011-2789: Use after free in Pepper plug-in
    instantiation.
  * [86502] High CVE-2011-2790: Use-after-free with floating styles.
  * [86900] High CVE-2011-2791: Out-of-bounds write in ICU.
  * [87148] High CVE-2011-2792: Use-after-free with float removal.
  * [87227] High CVE-2011-2793: Use-after-free in media selectors.
  * [87298] Medium CVE-2011-2794: Out-of-bounds read in text iteration.
  * [87339] Medium CVE-2011-2795: Cross-frame function leak.
  * [87548] High CVE-2011-2796: Use-after-free in Skia.
  * [87729] High CVE-2011-2797: Use-after-free in resource caching.
  * [87815] Low CVE-2011-2798: Prevent a couple of internal schemes from
    being web accessible.
  * [87925] High CVE-2011-2799: Use-after-free in HTML range handling.
  * [88337] Medium CVE-2011-2800: Leak of client-side redirect target.
  * [88591] High CVE-2011-2802: v8 crash with const lookups.
  * [88827] Medium CVE-2011-2803: Out-of-bounds read in Skia paths.
  * [88846] High CVE-2011-2801: Use-after-free in frame loader.
  * [88889] High CVE-2011-2818: Use-after-free in display box rendering.
  * [89142] High CVE-2011-2804: PDF crash with nested functions.
  * [89520] High CVE-2011-2805: Cross-origin script injection.
  * [90222] High CVE-2011-2819: Cross-origin violation in base URI handling.
- detailed changelog at http://goo.gl/25VH4

* Fri Jul 29 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.124-1
+ Revision: 692282
- new upstream release 112-12.0.742.124 (92024)

* Tue Jun 28 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.112-1
+ Revision: 687931
- new upstream release 12.0.742.112 (90785)
- security fixes:
  * [77493] Medium CVE-2011-2345: Out-of-bounds read in NPAPI string handling.
  * [84355] High CVE-2011-2346: Use-after-free in SVG font handling.
  * [85003] High CVE-2011-2347: Memory corruption in CSS parsing.
  * [85102] High CVE-2011-2350: Lifetime and re-entrancy issues in the HTML
    parser.
  * [85177] High CVE-2011-2348: Bad bounds check in v8.
  * [85211] High CVE-2011-2351: Use-after-free with SVG use element.
  * [85418] High CVE-2011-2349: Use-after-free in text selection.
- detailed changelog at http://goo.gl/PPBY4

* Tue Jun 07 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.91-1
+ Revision: 683117
- new upstream release 12.0.742.91 (stable)
  * Hardware accelerated 3D CSS
  * New Safe Browsing protection against downloading malicious files
  * Ability to delete Flash cookies from inside Chrome
  * Launch Apps by name from the Omnibox
  * Integrated Sync into new settings pages
  * Improved screen reader support
  * New warning when hitting Command-Q on Mac
  * Removal of Google Gears
- security fixes
  * [73962] [79746] High CVE-2011-1808: Use-after-free due to integer issues
    in float handling
  * [75496] Medium CVE-2011-1809: Use-after-free in accessibility support
  * [75643] Low CVE-2011-1810: Visit history information leak in CSS
  * [76034] Low CVE-2011-1811: Browser crash with lots of form submissions
  * [77026] Medium CVE-2011-1812: Extensions permission bypass
  * [78516] High CVE-2011-1813: Stale pointer in extension framework
  * [79362] Medium CVE-2011-1814: Read from uninitialized pointer
  * [79862] Low CVE-2011-1815: Extension script injection into new tab page
  * [80358] Medium CVE-2011-1816: Use-after-free in developer tools
  * [81916] Medium CVE-2011-1817: Browser memory corruption in history
    deletion
  * [81949] High CVE-2011-1818: Use-after-free in image loader
  * [83010] Medium CVE-2011-1819: Extension injection into chrome:// pages
  * [83275] High CVE-2011-2332: Same origin bypass in v8
  * [83743] High CVE-2011-2342: Same origin bypass in DOM
- copy release 12.0.742.91 from beta to stable

* Wed May 25 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.71-1
+ Revision: 678989
- new upstream release 11.0.696.71 (stable)
- security fixes
  * [72189] Low CVE-2011-1801: Pop-up blocker bypass.
  * [$1000] [82546] High CVE-2011-1804: Stale pointer in floats rendering.
  * [82873] Critical CVE-2011-1806: Memory corruption in GPU command buffer.
  * [82903] Critical CVE-2011-1807: Out-of-bounds write in blob handling.
- bug fixes
  * REGRESSION: selection extended by arrow keys flickers on LinkedIn.com.
    (Issue 83197).
  * Have ConnectBackupJob try IPv4 first to hide potential long IPv6 connect
    timeout (Issue 81686).

* Thu May 12 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.68-1
+ Revision: 673982
- new upstream release 11.0.696.68 (stable)
- security fixes
  * [64046] High CVE-2011-1799: Bad casts in Chromium WebKit glue.
  * [80608] High CVE-2011-1800: Integer overflows in SVG filters.

* Sat May 07 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.65-1
+ Revision: 671613
- new upstream release 11.0.696.65 (stable)
  * fix issue 80580: After deleting bookmarks on the Bookmark managers,
    the bookmark bar doesn't display properly with existing bookmarks.

* Fri Apr 29 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.57-1
+ Revision: 660171
- new upstream release 11.0.696.57 (stable)
- security fixes:
  * [61502] High CVE-2011-1303: Stale pointer in floating object handling
  * [70538] Low CVE-2011-1304: Pop-up block bypass via plug-ins
  * [70589] Medium CVE-2011-1305: Linked-list race in database handling
  * [71686] Medium CVE-2011-1434: Lack of thread safety in MIME handling
  * [72523] Medium CVE-2011-1435: Bad extension with tabs permission can
    capture local files
  * [72910] Low CVE-2011-1436: Possible browser crash due to bad interaction
    with X
  * [73526] High CVE-2011-1437: Integer overflows in float rendering
  * [74653] High CVE-2011-1438: Same origin policy violation with blobs
  * [74763] High CVE-2011-1439: Prevent interference between renderer
    processes
  * [75186] High CVE-2011-1440: Use-after-free with <ruby> tag and CSS
  * [75347] High CVE-2011-1441: Bad cast with floating select lists
  * [75801] High CVE-2011-1442: Corrupt node trees with mutation events
  * [76001] High CVE-2011-1443: Stale pointers in layering code
  * [76542] High CVE-2011-1444: Race condition in sandbox launcher
  * [76646] Medium CVE-2011-1445: Out-of-bounds read in SVG
  * [76666] [77507] [78031] High CVE-2011-1446: Possible URL bar spoofs with
    navigation errors and interrupted loads
  * [76966] High CVE-2011-1447: Stale pointer in drop-down list handling
  * [77130] High CVE-2011-1448: Stale pointer in height calculations
  * [77346] High CVE-2011-1449: Use-after-free in WebSockets
  * [77349] Low CVE-2011-1450: Dangling pointers in file dialogs
  * [77463] High CVE-2011-1451: Dangling pointers in DOM id map
  * [77786] Medium CVE-2011-1452: URL bar spoof with redirect and manual
    reload
  * [79199] High CVE-2011-1454: Use-after-free in DOM id handling
  * [79361] Medium CVE-2011-1455: Out-of-bounds read with multipart-encoded
    PDF
  * [79364] High CVE-2011-1456: Stale pointers with PDF forms
- detailed changelog at http://goo.gl/arI9m
- copy Chromium 11 sources from beta to stable
- remove Chromium 10 source files

* Fri Apr 15 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.205-1
+ Revision: 653084
- new upstream release 10.0.648.205 (stable)
  * Fix issue 75629: CVE-2011-1301: Use-after-free in the GPU process
  * Fix issue 78524: CVE-2011-1302: Heap overflow in the GPU process
- detailed changelog at http://goo.gl/wJg8b

* Mon Apr 04 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.204-2
+ Revision: 650370
- update chromium-browser package group
- bump release for buildsystem debug

* Fri Mar 25 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.204-1
+ Revision: 648498
- new upstream release 10.0.648.204 (stable)
  * support for password manager
  * performance and stability fixes
  * fix CVE-2011-1291: Buffer error in base string handling
  * fix CVE-2011-1292: Use-after-free in the frame loader
  * fix CVE-2011-1293: Use-after-free in HTMLCollection
  * fix CVE-2011-1294: Stale pointer in CSS handling
  * fix CVE-2011-1295: DOM tree corruption with broken node parentage
  * fix CVE-2011-1296: Stale pointer in SVG text handling
- fix some system library settings introduced in revision 647139

  + Funda Wang <fwang@mandriva.org>
    - build with more system libs

* Fri Mar 18 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.151-1
+ Revision: 646282
- new upstream release 10.0.648.151 (stable)
  * blacklist a small number of HTTPS certificates

* Sat Mar 12 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.133-1
+ Revision: 644042
- new upstream release 10.0.648.133 (stable)
  * [CVE-2011-1290] fix memory corruption in style handling
- check presence of patch files

* Fri Mar 11 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.127-2
+ Revision: 643848
- apply patches correctly

* Wed Mar 09 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.127-1
+ Revision: 643105
- new upstream release 10.0.648.127 (stable)
  * New version of V8 which greatly improves javascript performance
  * New settings pages that open in a tab, rather than a dialog box
  * Improved security with malware reporting and disabling outdated plugins
    by default
  * Password sync as part of Chrome Sync now enabled by default
  * GPU Accelerated Video
  * Background WebApps
  * webNavigation extension API
- annoucement and security fix list: http://goo.gl/PWdBi
- move chromium patch 10.0.648.114 from beta channel to stable
- move chromium patch 10.0.648.82 from beta channel to stable
- move chromium patch 10.0.648.127 from beta channel to stable
- move chromium patch 10.0.648.126 from beta channel to stable
- move chromium 10.0.648.45 from beta channel to stable
- move patch from beta channel to stable
- move patch from beta channel to stable

* Tue Mar 01 2011 Claudio Matsuoka <claudio@mandriva.com> 9.0.597.107-1
+ Revision: 641075
- new upstream release 9.0.597.107 (stable)
- contains security fixes, see detais at http://goo.gl/rkTSm
- add beta browser to the downgrade notice in spec description

* Sat Feb 12 2011 Claudio Matsuoka <claudio@mandriva.com> 9.0.597.98-1
+ Revision: 637364
- new upstream version 9.0.597.98
- add conflicts to beta channel browser
- add obsoletes entry for old (canary) chromium-browser package

* Thu Feb 10 2011 Claudio Matsuoka <claudio@mandriva.com> 9.0.597.94-1
+ Revision: 637082
- imported package chromium-browser-stable

