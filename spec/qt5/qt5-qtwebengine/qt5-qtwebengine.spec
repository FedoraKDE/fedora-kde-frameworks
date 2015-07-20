
%global qt_module qtwebengine

%global _hardened_build 1

# define to build docs, need to undef this for bootstrapping
# where qt5-qttools builds are not yet available
# only primary archs (for now), allow secondary to bootstrap
%ifarch %{arm} %{ix86} x86_64
%define docs 1
%endif

#define prerelease rc

Summary: Qt5 - QtWebEngine components
Name:    qt5-qtwebengine
Version: 5.5.0
Release: 2%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://qt-project.org/doc/qt-5.0/qtdoc/licensing.html
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://www.qt.io
Source0: http://download.qt.io/official_releases/qt/5.5/%{version}%{?prerelease:-%{prerelease}}/submodules/%{qt_module}-opensource-src-%{version}%{?prerelease:-%{prerelease}}.tar.xz
Patch0:  qtwebengine-opensource-5.5.0-no-format.patch
Patch1:  qtwebengine-opensource-5.5.0-unbundle-gyp.patch

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtdeclarative-devel >= %{version}
BuildRequires: qt5-qtxmlpatterns-devel >= %{version}
BuildRequires: qt5-qtlocation-devel >= %{version}
BuildRequires: qt5-qtsensors-devel >= %{version}
BuildRequires: qt5-qtwebchannel-devel >= %{version}
BuildRequires: qt5-qttools-static >= %{version}
BuildRequires: bison
BuildRequires: flex
BuildRequires: gperf
BuildRequires: libicu-devel
BuildRequires: libjpeg-devel
BuildRequires: libgcrypt-devel
BuildRequires: bzip2-devel
BuildRequires: v8-devel
Buildrequires: re2-devel
BuildRequires: snappy-devel
BuildRequires: yasm
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gobject-2.0) 
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(hunspell)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libpcre)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(libssl)
%if 0%{?fedora} || 0%{?rhel} > 6
BuildRequires: pkgconfig(libwebp)
%endif
BuildRequires: pkgconfig(harfbuzz)
BuildRequires: pkgconfig(jsoncpp)
BuildRequires: pkgconfig(protobuf)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(opus)
BuildRequires: pkgconfig(libcrypto)
BuildRequires: pkgconfig(libevent)
BuildRequires: pkgconfig(libmtp)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(libexif)
BuildRequires: pkgconfig(flac++)
BuildRequires: pkgconfig(minizip)
BuildRequires: pkgconfig(liblzma)
BuildRequires: pkgconfig(libxslt)
#BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xcomposite) 
BuildRequires: pkgconfig(xrandr) 
BuildRequires: pkgconfig(xcursor) 
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xtst)
BuildRequires: pkgconfig(libcap)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(cairo)
BuildRequires: pkgconfig(libpci)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(nss)
BuildRequires: pkgconfig(libusb)
BuildRequires: pkgconfig(speex)
BuildRequires: pkgconfig(libsrtp)
BuildRequires: perl perl(version) perl(Digest::MD5) perl(Text::ParseWords)
BuildRequires: ruby
BuildRequires: python-devel

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}


%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
Requires: qt5-qtdeclarative-devel%{?_isa}
%description devel
%{summary}.

%package examples
Summary: Example files for %{name}

%description examples
%{summary}.


%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
# for qhelpgenerator
BuildRequires: qt5-qttools-devel
BuildArch: noarch
%description doc
%{summary}.
%endif


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?prerelease:-%{prerelease}}
%patch0 -p1 -b .noformat
%patch1 -p1 -b .gypchange

%build
export STRIP=strip
export NINJAFLAGS="-v %{_smp_mflags}"

# Something to evaluate 
# libvpx not compiles against Fedora 1.4.0  -Duse_system_libvpx=1
# sqlite3 extra functions - Read src/3rdparty/chromium/third_party/sqlite/README.chromium -Duse_system_sqlite=1"

unbundle_conf+="
	-Duse_system_expat=1
	-Duse_system_flac=1
	-Duse_system_icu=1
	-Duse_system_jsoncpp=1
	-Duse_system_libevent=1
	-Duse_system_libjpeg=1
	-Duse_system_libpng=1
	-Duse_system_libusb=1
	-Duse_system_libxml=1
	-Duse_system_libxslt=1
	-Duse_system_opus=1
	-Duse_system_snappy=1
	-Duse_system_speex=1
	-Duse_system_harfbuzz=1
	-Duse_system_libwebp=1
	-Duse_system_re2=1
	-Duse_system_openssl=1
	-Duse_system_zlib=1"
												   
pushd src/3rdparty/chromium/
	build/linux/unbundle/replace_gyp_files.py $unbundle_conf
popd
												    
mkdir %{_target_platform}
pushd %{_target_platform}

%{qmake_qt5} .. 

# workaround, disable parallel compilation as it fails to compile in brew
make %{?_smp_mflags}

%if 0%{?docs}
make %{?_smp_mflags} docs
%endif
popd

%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot} -C %{_target_platform}
%endif

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_qt5_libdir}/libQt5*.so.*
%{_qt5_libdir}/qt5/qml/*
%{_qt5_libdir}/qt5/libexec/QtWebEngineProcess
%{_qt5_translationdir}/*

%{_qt5_plugindir}/qtwebengine
%{_qt5_datadir}/qtwebengine_resources.pak

%files devel
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/libQt5*.so
%{_qt5_libdir}/libQt5*.prl
%{_qt5_libdir}/cmake/Qt5*/
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%files examples
%{_qt5_libdir}/qt5/examples

%if 0%{?docs}
%files doc
%{_qt5_docdir}/*
%endif


%changelog
* Fri Jul 17 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-2
- Update with unbundle flags. Adapted from original 5.4 Suse package
- Disable vpx and sqlite as unbundle due some compilation issues
- Enable verbose build

* Fri Jul 17 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-1
- Initial spec

* Thu Jun 25 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages
