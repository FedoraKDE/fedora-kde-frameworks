
%global qt_module qt3d
# define to build docs, need to undef this for bootstrapping
%define docs 1

%define pre rc

Summary: Qt5 - Qt3D QML bindings and C++ APIs
Name:    qt5-%{qt_module}
Version: 5.5.0
Release: 0.2.rc%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://doc.qt.io/qt-5/licensing.html
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://www.qt.io
Source0: http://download.qt.io/development_releases/qt/5.5/%{version}%{?pre:-%{pre}}/submodules/%{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}.tar.xz

BuildRequires:  qt5-qtbase-static >= %{version}
BuildRequires:  qt5-qtxmlpatterns-devel >= %{version}
BuildRequires:  qt5-qtdeclarative-devel >= %{version}
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5XmlPatterns)
BuildRequires:  pkgconfig(Qt5Declarative)
BuildRequires:  pkgconfig(Qt5OpenGL)

Requires:       qt5-qtimageformats >= %{version}

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


%build
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
%doc LICENSE.GPL* LICENSE.LGPL*
%{_qt5_libdir}/libQt53DQuickRenderer.so.5*
%{_qt5_libdir}/libQt53DQuick.so.5*
%{_qt5_libdir}/libQt53DInput.so.5*
%{_qt5_libdir}/libQt53DRenderer.so.5*
%{_qt5_libdir}/libQt53DCore.so.5*
%{_qt5_archdatadir}/qml/Qt3D/
%{_qt5_archdatadir}/qml/QtQuick/Scene3D

%files devel
%{_qt5_libdir}/libQt53DQuickRenderer.so
%{_qt5_libdir}/libQt53DQuickRenderer.prl
%{_qt5_libdir}/cmake/Qt53DQuickRenderer
%{_qt5_headerdir}/Qt3DQuickRenderer
%{_qt5_libdir}/libQt53DQuick.so
%{_qt5_libdir}/libQt53DQuick.prl
%{_qt5_libdir}/cmake/Qt53DQuick
%{_qt5_headerdir}/Qt3DQuick
%{_qt5_libdir}/libQt53DInput.so
%{_qt5_libdir}/libQt53DInput.prl
%{_qt5_libdir}/cmake/Qt53DInput
%{_qt5_headerdir}/Qt3DInput/
%{_qt5_libdir}/libQt53DRenderer.so
%{_qt5_libdir}/libQt53DRenderer.prl
%{_qt5_libdir}/cmake/Qt53DRenderer
%{_qt5_headerdir}/Qt3DRenderer/
%{_qt5_libdir}/libQt53DCore.so
%{_qt5_libdir}/libQt53DCore.prl
%{_qt5_libdir}/cmake/Qt53DCore/
%{_qt5_headerdir}/Qt3DCore/
%{_qt5_archdatadir}/mkspecs/modules/*.pri


%if 0%{?docs}
%files doc
%{_qt5_docdir}/qt3dcore.qch
%{_qt5_docdir}/qt3dcore/
%{_qt5_docdir}/qt3drender.qch
%{_qt5_docdir}/qt3drenderer/
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Thu Jun 25 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages

* Wed Jun 17 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-0.1.rc
- Qt 5.5.0 RC1 (initial version)

