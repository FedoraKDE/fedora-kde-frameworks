%global frameworksversion 5.1.0

Name:           extra-cmake-modules
Summary:        Additional modules for CMake build system
# ECM does not follow the frameworks versioning, but is currently being
# release together with it
Version:        1.1.0
Release:        1%{?dist}

License:        BSD
URL:            http://community.kde.org/KDE_Core/Platform_11/Buildsystem/FindFilesSurvey
Source0:        http://download.kde.org/stable/frameworks/%{frameworksversion}/%{name}-%{version}.tar.xz
BuildArch:      noarch

BuildRequires:  cmake >= 2.8.12

Requires:       cmake >= 2.8.12

%description
Additional modules for CMake build system needed by KDE Frameworks.


%prep
%setup -q


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%files
%doc README.rst COPYING-CMAKE-SCRIPTS
%{_datadir}/ECM


%changelog
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
