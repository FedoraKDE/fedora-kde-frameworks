Name:           extra-cmake-modules
Summary:        Additional modules for CMake build system
Version:        5.13.0
Release:        0.1%{?dist}

License:        BSD
URL:            https://projects.kde.org/projects/kdesupport/extra-cmake-modules
#URL:           http://community.kde.org/KDE_Core/Platform_11/Buildsystem/FindFilesSurvey

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{name}-%{version}.tar.xz
BuildArch:      noarch

BuildRequires:  cmake >= 2.8.12

Requires:       cmake >= 2.8.12

%description
Additional modules for CMake build system needed by KDE Frameworks.


%prep
%setup -q


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%files
%doc README.rst COPYING-CMAKE-SCRIPTS
%{_datadir}/ECM/


%changelog
* Tue Aug 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.13.0-0.1
- KDE Frameworks 5.13

* Thu Jul 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.12.0-1
- 5.12.0, update URL (to reference projects.kde.org), .spec cosmetics

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Daniel Vrátil <dvratil@redhat.com> - 5.11.0-1
- KDE Frameworks 5.11.0

* Mon May 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.10.0-1
- KDE Frameworks 5.10.0

* Tue Apr 07 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- KDE Frameworks 5.9.0

* Mon Mar 16 2015 Daniel Vrátil <dvratil@redhat.com> - 1.8.0-1
- extra-cmake-modules 1.8.0 (KDE Frameworks 5.8.0)

* Fri Feb 13 2015 Daniel Vrátil <dvratil@redhat.com> - 1.7.0-1
- extra-cmake-modules 1.7.0 (KDE Frameworks 5.7.0)

* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 1.6.1-1
- Update to 1.6.1 which includes upstream fix for kde#341717

* Sun Jan 11 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.6.0-3
- Use upstream version of the kde#342717 patch by Alex Merry

* Sun Jan 11 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.6.0-2
- Do not unset old-style variables in KDEInstallDirs.cmake, it breaks projects
  using GNUInstallDirs for some parts and KDEInstallDirs for others (kde#342717)

* Thu Jan 08 2015 Daniel Vrátil <dvratil@redhat.com> - 1.6.0-1
- extra-cmake-modules 1.6.0 (KDE Frameworks 5.6.0)

* Thu Dec 11 2014 Daniel Vrátil <dvratil@redhat.com> - 1.5.0-1
- extra-cmake-modules 1.5.0 (KDE Frameworks 5.5.0)

* Mon Nov 03 2014 Daniel Vrátil <dvratil@redhat.com> - 1.4.0-1
- extra-cmake-modules 1.4.0 (KDE Frameworks 5.4.0)

* Tue Oct 07 2014 Daniel Vrátil <dvratil@redhat.com> - 1.3.0-1
- extra-cmake-modules 1.3.0 (KDE Frameworks 5.3.0)

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 1.2.1-1
- extra-cmake-modules 1.2.1 (KDE Frameworks 5.2.0)

* Mon Sep 15 2014 Daniel Vrátil <dvratil@redhat.com> - 1.2.0-1
- extra-cmake-modules 1.2.0 (KDE Frameworks 5.2.0)

* Wed Aug 06 2014 Daniel Vrátil <dvratil@redhat.com> - 1.1.0-1
- extra-cmake-modules 1.1.0 (KDE Frameworks 5.1.0)

* Thu Jul 10 2014 Daniel Vrátil <dvratil@redhat.com> - 1.0.0-1
- extra-cmake-modules 1.0.0 (KDE Frameworks 5.0.0)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Daniel Vrátil <dvratil@redhat.com> 0.0.14-2
- Strip architecture check from a CMake-generated file to fix noarch build

* Tue Jun 03 2014 Daniel Vrátil <dvratil@redhat.com> 0.0.14-1
- extra-cmake-modules 0.0.14 (KDE Frameworks 4.100.0)

* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> 0.0.13-1
- extra-cmake-modules 0.0.13 (KDE Frameworks 4.99.0)

* Fri Apr 11 2014 Daniel Vrátil <dvratil@redhat.com> 0.0.12-3
- Remove debug_package, add %%{?dist} to Release

* Fri Apr 11 2014 Daniel Vrátil <dvratil@redhat.com> 0.0.12-2
- Don't depend on kf5-filesystem

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 0.0.12-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 0.0.11-1
- Update to KDE Frameworks 5 Alpha 2 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 0.0.10-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 0.0.10-0.1.20140205git
- Update to pre-relase snapshot of 0.0.10

* Tue Feb 04 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.0.9-1
- Update to Jan 7 release

* Mon Sep 16 2013 Lubomir Rintel <lkundrak@v3.sk> - 0.0.9-0.1.20130013git5367954
- Initial packaging
