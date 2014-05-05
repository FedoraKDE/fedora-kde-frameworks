#global snapshot 20140205
%global frameworksversion 4.99.0

Name:           extra-cmake-modules
Summary:        Additional modules for CMake build system
# ECM does not follow the frameworks versioning, but is currently being
# release together with it
Version:        0.0.13
Release:        1%{?dist}

License:        BSD
URL:            http://community.kde.org/KDE_Core/Platform_11/Buildsystem/FindFilesSurvey

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name},git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        http://download.kde.org/unstable/frameworks/%{frameworksversion}/%{name}-%{version}.tar.xz

BuildArch:      noarch

BuildRequires:  cmake >= 2.8.12

Requires:       cmake >= 2.8.12

%description
Additional modules for CMake build system needed by KDE Frameworks.


%prep
%setup -q -n %{name}-%{version}


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
* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> - 0.0.13-1
- KDE Frameworks 4.99.0

* Mon May 05 2014 dvratil <dvratil@redhat.com> - 0.0.12-4.20140505git73992f13
- Update to git: 73992f13

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 0.0.12-4.20140428gitf0607b48
- Update to git: f0607b48

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 0.0.12-3.20140428gitf0607b48
- Update to git: f0607b48

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 0.0.12-3.20140428gitf0607b48
- Update to git: f0607b48

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 0.0.12-3.20140428gitf0607b48
- Update to git: f0607b48

* Fri Apr 25 2014 dvratil <dvratil@redhat.com> - 0.0.12-20140425gitb3bf34a7
- Update to git: b3bf34a7

* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 0.0.12-20140422gite7ca63c7
- Update to git: e7ca63c7

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
