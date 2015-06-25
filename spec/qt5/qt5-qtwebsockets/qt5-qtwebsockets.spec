
%global qt_module qtwebsockets
# define to build docs, need to undef this for bootstrapping
%define docs 1

%define pre rc

Summary: Qt5 - WebSockets component
Name:    qt5-%{qt_module}
Version: 5.5.0
Release: 0.1.rc%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://doc.qt.io/qt-5/licensing.html
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://www.qt.io
Source0: http://download.qt.io/development_releases/qt/5.5/%{version}%{?pre:-%{pre}}/submodules/%{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}.tar.xz
#%if 0%{?pre:1}
#Source0: http://download.qt-project.org/development_releases/qt/5.4/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
#%else
#Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
#%endif

BuildRequires:  qt5-qtbase-devel >= %{version}
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Core)

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
The QtWebSockets module implements the WebSocket protocol as specified in RFC
6455. It solely depends on Qt (no external dependencies).

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
License: GFDL
Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
BuildRequires: qt5-qttools-devel
BuildArch: noarch
%description doc
%{summary}.
%endif

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}
#%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}


%build
pushd %{qt_module}
mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} ..

make %{?_smp_mflags}

%if 0%{?docs}
# HACK to avoid multilib conflicts in noarch content
# see also https://bugreports.qt-project.org/browse/QTBUG-42071
QT_HASH_SEED=0; export QT_HASH_SEED
make %{?_smp_mflags} docs
%endif
popd
popd

%install
pushd %{qt_module}
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
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LICENSE.GPL* LICENSE.LGPL*
%{_qt5_libdir}/libQt5WebSockets.so.5*
%{_qt5_archdatadir}/qml/QtWebSockets/
%{_qt5_archdatadir}/qml/Qt/WebSockets/

%files devel
%{_qt5_headerdir}/QtWebSockets/
%{_qt5_libdir}/libQt5WebSockets.so
%{_qt5_libdir}/libQt5WebSockets.prl
%dir %{_qt5_libdir}/cmake/Qt5WebSockets/
%{_qt5_libdir}/cmake/Qt5WebSockets/Qt5WebSocketsConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5WebSockets.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_websockets*.pri

%if 0%{?docs}
%files doc
%{_qt5_docdir}/%{qt_module}.qch
%{_qt5_docdir}/%{qt_module}/
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Wed Jun 17 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-0.1.rc
- Qt 5.5.0 RC1

* Sun Jun 07 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-1
- 5.4.2

* Fri Apr 10 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-1
- 5.4.1

* Tue Dec 23 2014 Taylor Braun-Jones <taylor.braun-jones@ge.com> - 5.4.0-1
- Initial release.
