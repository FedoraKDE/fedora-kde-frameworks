# There's nothing to debug
%global debug_package   %{nil}
%define framework umbrella
#%define snapshot 20140205

Name:           kf5-%{framework}
Version:        4.98.0
Epoch:          1
Release:        1.20140428gitd83f508d%{?dist}
Summary:        CMake configuration for KDE Frameworks 5

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=kf5umbrella-%{version}/ \
#             --remote=git://anongit.kde.org/kf5umbrella,git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        kf5umbrella-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-umbrella-d83f508d.tar

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

Requires:       kf5-filesystem

%description
Provides CMake configuration file for KDE Frameworks 5


%prep
%setup -q -n umbrella-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%files
%doc README.md
%{_kf5_libdir}/cmake/KF5


%changelog
* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-1.20140428gitd83f508d
- Update to git: d83f508d

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418gitf5306606
- Update to git: f5306606

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 1:4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 1:4.97.0-1
- Update to KDE Frameworks 5 Alpha 2 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 1:4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 1:0.0.10-0.1.20140205git
- Update to pre-release snapshot of 0.0.10

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Thu Jan  9 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version

