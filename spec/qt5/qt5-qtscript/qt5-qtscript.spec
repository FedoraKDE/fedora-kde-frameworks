
%global qt_module qtscript

# define to build docs, need to undef this for bootstrapping
# where qt5-qttools builds are not yet available
%define docs 1

Summary: Qt5 - QtScript component
Name:    qt5-%{qt_module}
Version: 5.5.0
Release: 0.1.rc%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://www.qt.io
Source0: http://download.qt.io/snapshots/qt/5.5/latest_srcs/qt-everywhere-opensource-src-%{version}-rc.tar.xz
#%if 0%{?pre:1}
#Source0: http://download.qt-project.org/development_releases/qt/5.4/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
#%else
#Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
#%endif

# add s390(x0 support to Platform.h (taken from webkit)
Patch0: qtscript-opensource-src-5.2.0-s390.patch

BuildRequires: qt5-qtbase-devel >= %{version}
#if 0%{?_qt5_examplesdir:1}
BuildRequires: pkgconfig(Qt5UiTools)
#endif

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
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
%setup -q -n qt-everywhere-opensource-src-%{version}-rc
#%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}

pushd %{qt_module}
%patch0 -p1 -b .s390
popd


%build
pushd %{qt_module}
mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} ..

make %{?_smp_mflags}

%if 0%{?docs}
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

## .prl file love (maybe consider just deleting these -- rex
# nuke dangling reference(s) to %%buildroot, excessive (.la-like) libs
sed -i \
  -e "/^QMAKE_PRL_BUILD_DIR/d" \
  -e "/^QMAKE_PRL_LIBS/d" \
  %{buildroot}%{_qt5_libdir}/*.prl

## unpackaged files
# .la files, die, die, die.
rm -fv %{buildroot}%{_qt5_libdir}/lib*.la

popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LGPL_EXCEPTION.txt LICENSE.LGPL*
%{_qt5_libdir}/libQt5Script.so.5*
%{_qt5_libdir}/libQt5ScriptTools.so.5*

%files devel
%{_qt5_headerdir}/Qt*/
%{_qt5_libdir}/libQt5Script.so
%{_qt5_libdir}/libQt5Script.prl
%{_qt5_libdir}/libQt5ScriptTools.so
%{_qt5_libdir}/libQt5ScriptTools.prl
%dir %{_qt5_libdir}/cmake/Qt5Script/
%{_qt5_libdir}/cmake/Qt5Script/Qt5ScriptConfig*.cmake
%dir %{_qt5_libdir}/cmake/Qt5ScriptTools/
%{_qt5_libdir}/cmake/Qt5ScriptTools/Qt5ScriptToolsConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri

%if 0%{?docs}
%files doc
%{_qt5_docdir}/qtscript.qch
%{_qt5_docdir}/qtscript/
%{_qt5_docdir}/qtscripttools.qch
%{_qt5_docdir}/qtscripttools/
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Wed Jun 17 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-0.1.rc
- Qt 5.5.0 RC1

* Thu Jun 04 2015 Jan Grulich <jgrulich@redhat.com> - 5.4.2-1
- 5.4.2

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 5.4.1-3
- Rebuilt for GCC 5 C++11 ABI change

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-2
- rebuild (gcc5)

* Tue Feb 24 2015 Jan Grulich <jgrulich@redhat.com> 5.4.1-1
- 5.4.1

* Mon Feb 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-2
- rebuild (gcc5)

* Wed Dec 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-1
- 5.4.0 (final)

* Fri Nov 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.3.rc
- 5.4.0-rc

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.2.beta
- out-of-tree build, use %%qmake_qt5, support %%docs macro

* Sun Oct 19 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.1.beta
- 5.4.0-beta

* Tue Sep 16 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-1
- 5.3.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-1
- 5.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> 5.3.0-1
- 5.3.0

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Sun Feb 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-3
- Add AArch64 support to qtscript (#1056071)

* Mon Jan 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- -examples subpkg
- -doc for all archs

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Mon Nov 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.5.beta1
- enable -doc only on primary archs (allow secondary bootstrap)

* Sun Nov 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.4.beta1
- rebuild (arm/qreal)

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.3.beta1
- 5.2.0-beta1

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.2.alpha
- bootstrap ppc

* Tue Oct 01 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha
- -doc subpkg

* Wed Aug 28 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- 5.1.1

* Wed Aug 28 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-2
- update Source URL
- %%doc LGPL_EXCEPTION.txt LICENSE.GPL LICENSE.LGPL

* Thu Apr 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-1
- 5.0.2

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-1
- first try

