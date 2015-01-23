#%global git_version  4c5da6e
#%global git_date     20150112

%global base_name    libkscreen

Name:           libkscreen-qt5
Version:        5.2.0
Release:        2%{?dist}
Summary:        KDE display configuration library

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/libkscreen


# git archive --format=tar.gz --remote=git://anongit.kde.org/libkscreen.git \
#             --prefix=libkscreen-%%{version}/ --output=libkscreen-qt5-%%{git_version}.tar.gz %%{git_version}
#Source0:        libkscreen-%{git_version}.tar.gz

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{base_name}-%{version}.tar.xz

## upstreamable patches
## upstream patches

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXrandr-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

Requires:       kf5-filesystem

Provides:       kf5-kscreen%{?_isa} = %{version}-%{release}
Provides:       kf5-kscreen = %{version}-%{release}
Obsoletes:      kf5-kscreen%{?_isa} <= 1:5.1.95-2.beta


%description
LibKScreen is a library that provides access to current configuration
of connected displays and ways to change the configuration.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       kf5-kscreen-devel = %{version}-%{release}
Provides:       kf5-kscreen-devel%{?_isa} = %{version}-%{release}
Obsoletes:      kf5-kscreen-devel%{?_isa} = 1:5.1.95-1

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{base_name}-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_kf5_libexecdir}/kscreen_backend_launcher
%{_kf5_libdir}/libKF5Screen.so.*
%{_kf5_plugindir}/kscreen/

%files devel
%{_kf5_includedir}/KScreen/
%{_kf5_includedir}/kscreen_version.h
%{_kf5_libdir}/libKF5Screen.so
%{_kf5_libdir}/cmake/KF5Screen/
%{_libdir}/pkgconfig/kscreen2.pc
%{_kf5_archdatadir}/mkspecs/modules/qt_KScreen.pri


%changelog
* Fri Jan 23 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-2
- rename to libkscreen-qt5, fix Requries

* Wed Jan 14 2015 Daniel Vrátil <dvratil@redhat.com> 1:5.1.95-2
- rename back to kf5-kscreen to avoid conflict with libkscreen(4)

* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> 1:5.1.95-1
- Plasma 5.1.95 Beta

* Thu Jan 08 2015 Daniel Vrátil <dvratil@redhat.com> 1:5.0.94-2
- update to upstream git snapshot
- rename to libkscreen

* Tue Dec 23 2014 Daniel Vrátil <dvratil@redhat.com> 1:5.0.93-1
- update to upstream git snapshot (Qt 5)

* Sat Nov 01 2014 Rex Dieter <rdieter@fedoraproject.org> 1.0.5-2
- pkgconfig-style deps, -devel: +Requires: pkgconfig(QJson)

* Fri Oct 31 2014 Rex Dieter <rdieter@fedoraproject.org> 1.0.5-1
- 1.0.5

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Rex Dieter <rdieter@fedoraproject.org> 1:1.0.4-2
- update URL

* Tue May 13 2014 Rex Dieter <rdieter@fedoraproject.org> 1:1.0.4-1
- 1.0.4

* Tue Apr 22 2014 Daniel Vrátil <dvratil@redhat.com> - 1:1.0.2-3
- backport upstream crash fix
- Resolves: rhbz#998395 rhbz#1004558 rhbz#1016769 rhbz#1023816

* Mon Nov 25 2013 Rex Dieter <rdieter@fedoraproject.org> - 1:1.0.2-2
- backport pkgconfig fix (verify in %%check)
- track soname
- fix changelog date

* Wed Nov 20 2013 Dan Vrátil <dvratil@redhat.com> - 1:1.0.2-1
 - libkscreen 1.0.2

* Thu Aug 01 2013 Dan Vrátil <dvratil@redhat.com> - 1:1.0.1-1
 - libkscreen 1.0.1

* Mon Jun 17 2013 Dan Vrátil <dvratil@redhat.com> - 1:1.0-1
 - libkscreen 1.0

* Thu May 02 2013 Dan Vrátil <dvratil@redhat.com> - 1:0.0.92-1
 - libkscreen 0.0.92

* Tue Apr 23 2013 Dan Vrátil <dvratil@redhat.com> - 1:0.0.82.git20130423-1
 - dev git build

* Wed Mar 27 2013 Dan Vrátil <dvratil@redhat.com> - 1:0.0.81-1
 - libkscreen 0.0.81

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.0.71-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Dan Vrátil <dvratil@redhat.com> 1:0.0.71-2
 - fix dependency of libkscreen-devel
 
* Sun Jan 20 2013 Dan Vrátil <dvratil@redhat.com> 1:0.0.71-1
 - update to 0.0.71 - first official release
 - remove kscreen-console, it's now shipped in kscreen package
 
* Wed Jan 09 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.0-2.20121228git
- remove redundant BR's
- BR: qjson-devel >= 0.8.1
- fix dir ownership

* Fri Dec 28 2012 Dan Vrátil <dvratil@redhat.com> 0.9.0-1.20121228git
 - Fixed versioning
 - Added instructions how to retrieve sources
 - Fixed URL
 - Removed 'rm -rf $RPM_BUILD_ROOT'

* Wed Dec 26 2012 Dan Vrátil <dvratil@redhat.com> 20121226gitecc8d1a-1
 - Initial SPEC
