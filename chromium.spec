%define v8_ver 3.9.7.0
%define svn_revision 122684
%define debug_package %{nil}

Name:           chromium
Version:        19.0.1046.0
Release:        3%{?dist}.R
Summary:        Google's opens source browser project

License:        BSD
Group:          Applications/Internet
Url:            http://code.google.com/p/chromium/
Source0:        http://download.rfremix.ru/storage/chromium/%{version}/%{name}.%{version}.svn%{svn_revision}.tar.bz2
Source8:        http://download.rfremix.ru/storage/chromium/19.0.1031.0/ffmpeg-0.6-headers.tar.bz2
Source20:       chromium-vendor.patch.in
Source30:       master_preferences
Source31:       default_bookmarks.html
Source99:       chrome-wrapper
Source100:      chromium-browser.sh
Source101:      chromium-browser.desktop
Source102:      chromium-browser.xml
Source105:      chromium-12-256x256.svg
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:       chromium-browser = %{version}
Provides:       chromium-based-browser = %{version}
Obsoletes:      chromium-browser < %{version}

## Start Patches
# Many changes to the gyp systems so we can use system libraries
# PATCH-FIX-OPENSUSE Fix build with GCC 4.6
Patch1:         chromium-gcc46.patch
# PATCH-FIX-OPENSUSE patches in system zlib library
Patch8:         chromium-codechanges-zlib.patch
# PATCH-FIX-OPENSUSE removes build part for courgette
Patch13:        chromium-no-courgette.patch
# PATCH-FIX-OPENSUSE enables reading of the master preference
Patch14:        chromium-master-prefs-path.patch
# PATCH-FIX-OPENSUSE patches in system glew library
Patch17:        chromium-system-glew.patch
# PATCH-FIX-OPENSUSE patches in system expat library
Patch18:        chromium-system-expat.patch
# PATCH-FIX-OPENSUSE disables the requirement for ffmpeg
Patch20:        chromium-6.0.425.0-ffmpeg-no-pkgconfig.patch
# PATCH-FIX-OPENSUSE disable the use of tcmallic function
Patch25:        tcmalloc-factory.patch
# PATCH-FIX-OPENSUSE make sure that Chrome remoting is linking against the system libvpx
Patch26:        chromium-remoting-build-fix.diff
# PATCH-FIX-OPENSUSE patches in system speex library
Patch28:        chromium-7.0.500.0-system-speex.patch
# PATCH-FIX-OPENSUSE patches in the system libvpx library
Patch32:        chromium-7.0.542.0-system-libvpx.patch
# PATCH-FIX-OPENSUSE remove the rpath in the libraries
Patch62:        chromium-norpath.patch
# PATCH-FIX-OPENSUSE patches in the system v8 library
Patch63:        chromium-6.0.406.0-system-gyp-v8.patch
# PATCH-FIX-UPSTREAM Add more charset aliases
Patch64:        chromium-more-codec-aliases.patch
# PATCH-FIX-OPENSUSE Compile the sandbox with -fPIE settings
Patch66:        chromium-sandbox-pie.patch

BuildRequires:  libjpeg-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  bison
BuildRequires:  cups-devel
BuildRequires:  desktop-file-utils
BuildRequires:  flex
BuildRequires:  freetype-devel
BuildRequires:  gperf
BuildRequires:  hunspell-devel
BuildRequires:  bzip2-devel
BuildRequires:  libevent-devel
BuildRequires:  expat-devel
BuildRequires:  gnutls-devel
BuildRequires:  libpng-devel
BuildRequires:  libvpx-devel
BuildRequires:  libxslt-devel
BuildRequires:  libzip-devel
BuildRequires:  nspr-devel
BuildRequires:  nss-devel
BuildRequires:  krb5-devel
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
BuildRequires:  pkgconfig
BuildRequires:  perl(Switch)
BuildRequires:  pkgconfig(cairo) >= 1.6
BuildRequires:  dbus-glib-devel
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  dbus-devel
BuildRequires:  python
BuildRequires:	libselinux-devel
BuildRequires:  sqlite-devel
BuildRequires:  v8-devel = %{v8_ver}
BuildRequires:  zlib-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  elfutils-libelf-devel
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
BuildRequires:	libgnome-keyring-devel
%else
BuildRequires:  gnome-keyring-devel
%endif
BuildRequires:  python-devel
BuildRequires:  speex-devel
BuildRequires:  hicolor-icon-theme
BuildRequires:  libudev-devel
BuildRequires:  libXt-devel
BuildRequires:  libXScrnSaver-devel

# NaCl needs these
%ifarch x86_64
BuildRequires:	/lib/libc.so.6
BuildRequires:  /lib/libz.so.1
BuildRequires:  /lib/libgcc_s.so.1
%endif

Requires:       hicolor-icon-theme
Requires:       chromium-ffmpeg >= 19.0.1037.0
Requires:       v8 >= %{v8_ver}


%description
Chromium is the open-source project behind Google Chrome. We invite you to join
us in our effort to help build a safer, faster, and more stable way for all
Internet users to experience the web, and to create a powerful platform for
developing a new generation of web applications.


%prep
%setup -q -n %{name}

%patch1 -p1
%patch62 -p1
%patch63 -p1
%patch64
%patch8 -p1
%patch13 -p1
%patch14 -p1
%patch17 -p1
%patch18 -p1
%patch20 -p1
%patch25 -p1
%patch26 -p1
%patch28 -p1
%patch32 -p1
%patch66 -p1

echo "%{svn_revision}" > src/build/LASTCHANGE.in

pushd src/third_party/ffmpeg/
tar xf %{SOURCE8}
popd

# apply vendor patch after substitution
sed "s:RPM_VERSION:%{version}:" %{SOURCE20} | patch -p0

# Make sure that the requires legal files can be found
cp -a src/AUTHORS src/LICENSE .


%build

## create make files

PARSED_OPT_FLAGS=`echo \'%{optflags} -DUSE_SYSTEM_LIBEVENT -fPIC -fno-ipa-cp -fno-strict-aliasing \' | sed "s/ /',/g" | sed "s/',/', '/g"`
for i in src/build/common.gypi; do
        sed -i "s|'-march=pentium4',||g" $i
%ifnarch x86_64
        sed -i "s|'-mfpmath=sse',||g" $i
%endif
        sed -i "s|'-O<(debug_optimize)',||g" $i
        sed -i "s|'-m32',||g" $i
        sed -i "s|'-fno-exceptions',|$PARSED_OPT_FLAGS|g" $i
        sed -i "s|'-Werror'|'-Wno-error'|g" $i
done
# '
%if 0%{?rhel} <= 7
for i in src/build/common.gypi; do
        sed -i "s|'-Wno-unused-result',||g" $i
done
%endif

pushd src

./build/gyp_chromium -f make build/all.gyp \
-Dlinux_sandbox_path=%{_libdir}/chrome_sandbox \
-Dlinux_sandbox_chrome_path=%{_libdir}/chromium/chromium \
-Duse_openssl=0 \
-Duse_system_ffmpeg=1 \
-Duse_system_zlib=1 \
-Duse_system_libpng=1 \
-Duse_system_bzip2=1 \
-Duse_system_libbz2=1 \
-Duse_system_libjpeg=1 \
-Duse_system_libxml=1 \
-Duse_system_libxslt=1 \
-Duse_system_libevent=1 \
-Duse_system_vpx=1 \
-Dremove_webcore_debug_symbols=1 \
-Duse_system_v8=1 \
-Dproprietary_codecs=1 \
-Dlinux_fpic=1 \
%ifnarch x86_64
-Ddisable_sse2=1 \
%endif
%ifarch x86_64
-Dtarget_arch=x64 \
-Dlinux_use_gold_flags=0 \
%endif
-Djavascript_engine=v8

make -r %{?_smp_mflags} chrome V=1 BUILDTYPE=Release

# Build the required SUID_SANDBOX helper
make -r %{?_smp_mflags} chrome_sandbox V=1 BUILDTYPE=Release

popd


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/chromium/
mkdir -p %{buildroot}%{_bindir}
install -m 755 %{SOURCE100} %{buildroot}%{_bindir}/chromium
# x86_64 capable systems need this
sed -i "s|/usr/lib/chromium|%{_libdir}/chromium|g" %{buildroot}%{_bindir}/chromium
sed -i "s|/usr/lib/chrome_sandbox|%{_libdir}/chrome_sandbox|g" %{buildroot}%{_bindir}/chromium

pushd src/out/Release

cp -a chrome_sandbox %{buildroot}%{_libdir}/
cp -a chrome.pak locales xdg-mime %{buildroot}%{_libdir}/chromium/

# Patch xdg-settings to use the chromium version of xdg-mime as that the system one is not KDE4 compatible
sed "s|xdg-mime|%{_libdir}/chromium/xdg-mime|g" xdg-settings > %{buildroot}%{_libdir}/chromium/xdg-settings

cp -a resources.pak %{buildroot}%{_libdir}/chromium/
cp -a chrome %{buildroot}%{_libdir}/chromium/chromium
mkdir -p %{buildroot}%{_mandir}/man1/
cp -a chrome.1 %{buildroot}%{_mandir}/man1/chrome.1
cp -a chrome.1 %{buildroot}%{_mandir}/man1/chromium.1

# NaCl
cp -a nacl_helper %{buildroot}%{_libdir}/chromium/
cp -a nacl_helper_bootstrap %{buildroot}%{_libdir}/chromium/
cp -a nacl_irt_*.nexe %{buildroot}%{_libdir}/chromium/
cp -a libppGoogleNaClPluginChrome.so %{buildroot}%{_libdir}/chromium/
popd

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
cp -a %{SOURCE105} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/chromium-browser.svg

mkdir -p %{buildroot}%{_datadir}/applications/
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE101}

mkdir -p %{buildroot}%{_datadir}/gnome-control-center/default-apps/
cp -a %{SOURCE102} %{buildroot}%{_datadir}/gnome-control-center/default-apps/

# link to browser plugin path.  Plugin patch doesn't work. Why?
mkdir -p mkdir -p %{buildroot}%{_libdir}/chromium/plugins/

# Install the master_preferences file
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 %{SOURCE30} %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 %{SOURCE31} %{buildroot}%{_sysconfdir}/%{name}

# Strip manually
pushd %{buildroot}%{_libdir}/chromium/
strip -p chromium nacl_* *.so
popd

strip -p %{buildroot}%{_libdir}/chrome_sandbox


%clean
rm -rf %{buildroot}


%post
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


%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE
%config %{_sysconfdir}/%{name}
%dir %{_datadir}/gnome-control-center
%dir %{_datadir}/gnome-control-center/default-apps
%dir %{_libdir}/chromium/
%{_bindir}/chromium
%{_libdir}/chromium/chromium
%{_libdir}/chromium/plugins/
%{_libdir}/chromium/locales/
%{_libdir}/chromium/nacl_*
%{_libdir}/chromium/libppGoogleNaClPluginChrome.so
%attr(755,root,root) %{_libdir}/chromium/xdg-settings
%attr(755,root,root) %{_libdir}/chromium/xdg-mime
%{_libdir}/chromium/*.pak
%{_mandir}/man1/chrom*
%{_datadir}/applications/*.desktop
%{_datadir}/gnome-control-center/default-apps/chromium-browser.xml
%{_datadir}/icons/hicolor/scalable/apps/chromium-browser.svg
%attr(4755, root, root) %{_libdir}/chrome_sandbox


%changelog
* Fri Feb 24 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 19.0.1046.0-3.R
- build with internal NaCl
- added BR for some i686 libs in x86_64 build
- fix distribution name in useragent
- GNOME 3.4 has new keyring packages

* Thu Feb 23 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 19.0.1046.0-2.R
- fix chromium-ffmpeg version

* Wed Feb 22 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 19.0.1046.0-1.R
- update to 19.0.1046.0
- added R: v8
- drop not supported gold linker options

* Mon Feb 20 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 19.0.1031.0-1.R
- update to 19.0.1031.0

* Sun Feb 19 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 18.0.972.0-1.R
- initial build for EL6
