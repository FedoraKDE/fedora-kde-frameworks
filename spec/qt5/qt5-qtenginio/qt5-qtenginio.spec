
%global qt_module qtenginio
# define to build docs, need to undef this for bootstrapping
%define docs 1

%define prerelease rc

Summary: Qt5 - Enginio component
Name:    qt5-%{qt_module}
Version: 5.5.0
Release: 0.2.rc%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://doc.qt.io/qt-5/licensing.html
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://www.qt.io
Source0: http://download.qt.io/development_releases/qt/5.5/%{version}%{?prerelease:-%{prerelease}}/submodules/%{qt_module}-opensource-src-%{version}%{?prerelease:-%{prerelease}}.tar.xz

BuildRequires:  qt5-qtbase-devel >= %{version}
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Quick)

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
Client library for accessing Enginio service from Qt and QML code.

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
%setup -q -n %{qt_module}-opensource-src-%{version}%{?prerelease:-%{prerelease}}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} ..

make %{?_smp_mflags}

%if 0%{?docs}
# HACK to avoid multilib conflicts in noarch content
# see also https://bugreports.qt.io/browse/QTBUG-42071
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
for prl_file in libEng*.prl ; do
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
%doc LICENSE* LGPL_EXCEPTION.txt
%{_qt5_libdir}/libEnginio.so.1*
%{_qt5_archdatadir}/qml/Enginio/

%files devel
%{_qt5_headerdir}/Enginio/
%{_qt5_libdir}/libEnginio.so
%{_qt5_libdir}/libEnginio.prl
%dir %{_qt5_libdir}/cmake/Qt5Enginio/
%{_qt5_libdir}/cmake/Qt5Enginio/Qt5EnginioConfig*.cmake
%{_qt5_libdir}/pkgconfig/Enginio.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_enginio*.pri

%if 0%{?docs}
%files doc
%{_qt5_docdir}/qtenginio.qch
%{_qt5_docdir}/qtenginio
%{_qt5_docdir}/qtenginiooverview.qch
%{_qt5_docdir}/qtenginiooverview
%{_qt5_docdir}/qtenginioqml.qch
%{_qt5_docdir}/qtenginioqml
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Thu Jun 25 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages

* Thu Jun 25 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.1.rc
- First release
