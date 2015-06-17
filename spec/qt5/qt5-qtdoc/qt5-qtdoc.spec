
%global qt_module qtdoc

Summary: Main Qt5 Reference Documentation
Name:    qt5-%{qt_module}
Version: 5.5.0
Release: 0.1.rc%{?dist}

License: GFDL
Url:     http://www.qt.io
Source0: http://download.qt.io/snapshots/qt/5.5/latest_srcs/qt-everywhere-opensource-src-%{version}-rc.tar.xz
#%if 0%{?pre:1}
#Source0: http://download.qt-project.org/development_releases/qt/5.4/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
#%else
#Source0: http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
#%endif

BuildArch: noarch

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qttools-devel

%description
QtDoc contains the main Qt Reference Documentation, which includes
overviews, Qt topics, and examples not specific to any Qt module.


%prep
%setup -q -n qt-everywhere-opensource-src-%{version}-rc
#%setup -q -n %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}


%build
pushd %{qt_module}
qmake-qt5
make docs %{?_smp_mflags}
popd

%install
pushd %{qt_module}
make install_docs INSTALL_ROOT=%{buildroot}
popd


%files
%doc LICENSE.FDL
%{_qt5_docdir}/qtdoc.qch
%{_qt5_docdir}/qtdoc/


%changelog
* Wed Jun 17 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-0.1-rc
- Qt 5.5.0 RC1

* Wed Jun 03 2015 Jan Grulich <jgrulich@redhat.com> -5.4.2-1
- 5.4.2

* Tue Feb 24 2015 Jan Grulich <jgrulich@redhat.com> 5.4.1-1
- 5.4.1

* Wed Dec 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-1
- 5.4.0 (final)

* Fri Nov 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.2.rc
- 5.4.0-rc

* Mon Oct 20 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.1.beta
- 5.4.0-beta

* Wed Sep 17 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.3.2-1
- 5.3.2

* Tue Jun 17 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-1
- 5.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> 5.3.0-1
- 5.3.0

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Fri Dec 06 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.11.rc1
- BR: qt5-qtbase-devel

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.2.beta1
- 5.2.0-beta1

* Thu Oct 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha

* Mon Sep 30 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-2
- License: GFDL

* Sun Sep 22 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- Initial packaging
