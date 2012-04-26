%define v8_ver 3.10.5.0
%define svn_revision 133754
%define debug_package %{nil}

Name:           chromium
Version:        20.0.1116.0
Release:        1%{?dist}
Summary:        Google's opens source browser project

License:        BSD-3-Clause and LGPL-2.1+
Group:          Applications/Internet
Url:            http://code.google.com/p/chromium/
Source0:        %{version}/%{name}.%{version}.svn%{svn_revision}.tar.bz2
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
# PATCH-FIX-OPENSUSE Fix build with GCC 4.6, GCC 4.7
Patch1:         chromium-gcc46.patch
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
Patch2:         chromium-gcc47.patch
%endif
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
%if 0%{?fedora} < 13 || 0%{?rhel} < 7
# Remove udev build requires and gamepad
Patch100: chromium-remove-linux-gamepad.patch
%endif

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
BuildRequires:  perl(Digest::MD5)
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
BuildRequires:  v8-devel >= %{v8_ver}
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
%if 0%{?fedora} < 13 || 0%{?rhel} < 7
BuildRequires:  libudev-devel
%endif
BuildRequires:  libXt-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXrender-devel
BuildRequires:  libXScrnSaver-devel

# NaCl needs these
%ifarch x86_64
BuildRequires:	/lib/libc.so.6
BuildRequires:  /lib/libz.so.1
BuildRequires:  /lib/libgcc_s.so.1
%endif

Requires:       hicolor-icon-theme
#Requires:       chromium-ffmpeg >= 19.0.1037.0
Requires:       v8 >= %{v8_ver}


%description
Chromium is the open-source project behind Google Chrome. We invite you to join
us in our effort to help build a safer, faster, and more stable way for all
Internet users to experience the web, and to create a powerful platform for
developing a new generation of web applications.


%prep
%setup -q -n %{name}

%patch1 -p1
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%patch2 -p1
%endif
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
%if 0%{?fedora} < 13 || 0%{?rhel} < 7
%patch100 -p1
%endif

echo "svn%{svn_revision}" > src/build/LASTCHANGE.in

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
-Dbuild_ffmpegsumo=1 \
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
%endif
-Dlinux_use_gold_flags=0 \
-Dlinux_use_gold_binary=0 \
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
* Thu Apr 26 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 20.0.1116.0-1.R
- update to 20.0.1116.0

* Thu Apr 19 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 20.0.1106.0-1.R
- update to 20.0.1106.0
- Fixes issues with fonts (Issue: 108645).
- Enable the Chrome To Mobile page action for users with 
  compatible registered devices

* Sun Apr  8 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 20.0.1096.0-1
- Update to 20.0.1096.0
- Other Devices menu shows last update time for other sessions, 
  and allows sessions to be hidden using a context menu.
- Fix sync issue with sessions (open tabs) triggering an 
  unrecoverable error.
- Fixed Sync/Apps: NTP apps icons missing after sync. 
  [Issue: 117857]
- Fixed bookmarks drag-n-drop in Bookmark Manager. 
  [Issue: 118715]
- Medium CVE-2011-3066: Out-of-bounds read in Skia clipping.
- Medium CVE-2011-3067: Cross-origin iframe replacement.
- High CVE-2011-3068: Use-after-free in run-in handling.
- High CVE-2011-3069: Use-after-free in line box handling.
- High CVE-2011-3070: Use-after-free in v8 bindings.
- High CVE-2011-3071: Use-after-free in HTMLMediaElement.
- Low CVE-2011-3072: Cross-origin violation parenting pop-up 
  window.
- High CVE-2011-3073: Use-after-free in SVG resource handling.
- Medium CVE-2011-3074: Use-after-free in media handling.
- High CVE-2011-3075: Use-after-free applying style command.
- High CVE-2011-3076: Use-after-free in focus handling.
- Medium CVE-2011-3077: Read-after-free in script bindings.

* Wed Apr  4 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 20.0.1090.0-1
- Update to 20.0.1090
- Fixed issue cannot add GMail app to Chrome. [Issue: 119975]
- Fixed theme and bookmarks bar notifications. [Issue: 117027]
- Fixed popup prompting permission for flash plugin. 
  [Issue: 120358]
- Medium CVE-2011-3058: Bad interaction possibly leading to 
  XSS in EUC-JP.
- Medium CVE-2011-3059: Out-of-bounds read in SVG text handling.
- Medium CVE-2011-3060: Out-of-bounds read in text fragment 
  handling.
- Medium CVE-2011-3061: SPDY proxy certificate checking error.
- High CVE-2011-3062: Off-by-one in OpenType Sanitizer.
- Low CVE-2011-3063: Validate navigation requests from the 
  renderer more carefully.
- High CVE-2011-3064: Use-after-free in SVG clipping.
- High CVE-2011-3065: Memory corruption in Skia.
- Medium CVE-2011-3057: Invalid read in v8.

* Wed Mar 28 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 19.0.1079.0-1
- Update to 19.0.1079
- High CVE-2011-3050: Use-after-free with first-letter handling
- High CVE-2011-3045: libpng integer issue from upstream
- High CVE-2011-3051: Use-after-free in CSS cross-fade handling
- High CVE-2011-3052: Memory corruption in WebGL canvas handling
- High CVE-2011-3053: Use-after-free in block splitting
- Low CVE-2011-3054: Apply additional isolations to webui 
  privileges
- Low CVE-2011-3055: Prompt in the browser native UI for unpacked 
  extension installation
- High CVE-2011-3056: Cross-origin violation with “magic iframe”.
- Low CVE-2011-3049: Extension web request API can interfere with
  system requests
- The short-cut key for caps lock (Shift + Search) is disabled 
  when an accessibility screen reader is enabled
- Fixes an issue with files not being displayed in File Manager 
  when some file names contain UTF-8 characters (generally 
  accented characters)
- Fixed dialog boxes in settings. (Issue: 118031)
- Fixed flash videos turning white on mac when running with 
  --disable-composited-core-animation-plugins (Issue: 117916) 
- Change to look for correctly sized favicon when multiple images 
  are provided. (Issue: 118275)
- Fixed issues - 116044, 117470, 117068, 117668, 118620

* Thu Mar 15 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 19.0.1071.0-1
- Several fixes and improvements in the new Settings, Extensions, and Help
  pages.
- Fixed the flashing when switched between composited and 
  non-composited mode. [Issue: 116603]
- Fixed stability issues 116913, 117217, 117347, 117081
- Fixed Chrome install/update resets Google search preferences 
  (Issue: 105390)
- Don't trigger accelerated compositing on 3D CSS when using 
  swiftshader (Issue: 116401)
- Fixed a GPU crash (Issue: 116096)
- More fixes for Back button frequently hangs (Issue: 93427)
- Bastion now works (Issue: 116285)
- Fixed Composited layer sorting irregularity with accelerated
  canvas (Issue: 102943)
- Fixed Composited layer sorting irregularity with accelerated 
  canvas (Issue: 102943)
- Fixed Google Feedback causes render process to use too much 
  memory (Issue: 114489)
- Fixed after upgrade, some pages are rendered as blank 
  (Issue: 109888)
- Fixed Pasting text into a single-line text field shouldn't 
  keep literal newlines (Issue: 106551)
- Critical CVE-2011-3047: Errant plug-in load and GPU process 
  memory corruption
- Critical CVE-2011-3046: UXSS and bad history navigation.

* Sat Mar  3 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 19.0.1060.0-1
- update to 19.0.1060.0
- Fixed NTP signed in state is missing (Issue: 112676)
- Fixed gmail seems to redraw itself (all white) occasionally 
  (Issue: 111263)
- Focus "OK" button on Javascript dialogs (Issue: 111015)
- Fixed Back button frequently hangs (Issue: 93427)
- Increase the buffer size to fix muted playback rate 
  (Issue: 108239)
- Fixed Empty span with line-height renders with non-zero height
  (Issue: 109811)
- Marked the Certum Trusted Network CA as an issuer of 
  extended-validation (EV) certificates.
- Fixed importing of bookmarks, history, etc. from Firefox 10+.
- Fixed issues - 114001, 110785, 114168, 114598, 111663, 113636, 
  112676
- Fixed several crashes (Issues: 111376, 108688, 114391)
- Fixed Firefox browser in Import Bookmarks and Settings 
  drop-down (Issue: 114476)
- Sync: Sessions aren't associating pre-existing tabs
  (Issue: 113319)
- Fixed All "Extensions" make an entry under the "NTP Apps"
  page (Issue: 113672)
- Security Fixes (bnc#750407): 
- High CVE-2011-3031: Use-after-free in v8 element wrapper.
- High CVE-2011-3032: Use-after-free in SVG value handling.
- High CVE-2011-3033: Buffer overflow in the Skia drawing library.
- High CVE-2011-3034: Use-after-free in SVG document handling.
- High CVE-2011-3035: Use-after-free in SVG use handling.
- High CVE-2011-3036: Bad cast in line box handling.
- High CVE-2011-3037: Bad casts in anonymous block splitting.
- High CVE-2011-3038: Use-after-free in multi-column handling.
- High CVE-2011-3039: Use-after-free in quote handling.
- High CVE-2011-3040: Out-of-bounds read in text handling.
- High CVE-2011-3041: Use-after-free in class attribute handling.
- High CVE-2011-3042: Use-after-free in table section handling.
- High CVE-2011-3043: Use-after-free in flexbox with floats.
- High CVE-2011-3044: Use-after-free with SVG animation elements.
- Remove the external ffmepg headers and start using the ones 
  delivered with Chromium. Changes to Chromium are no longer in line 
  with any ffmpeg version :-(. So we can only use the Chromium 
  ffmpeg headers.

* Sat Mar  3 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 19.0.1046.0-4
- added patch to remove gamepad support for old udev

* Fri Feb 24 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 19.0.1046.0-3.R
- build with internal NaCl
- added BR for some i686 libs in x86_64 build
- fix distribution name in useragent
- GNOME 3.4 has new keyring packages
- added gcc 4.7 patch
- added R: perl(Digest::MD5)

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
