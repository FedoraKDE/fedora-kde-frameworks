#%define snapshot 20140205
%define framework kservice

Name:           kf5-%{framework}
Version:        4.98.0
Release:        3.20140505git9146596a%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution for working with .desktop files

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-kservice-9146596a.tar

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-karchive-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 solution for working with .desktop files


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

mv %{buildroot}/%{_kf5_sysconfdir}/xdg/menus/applications.menu %{buildroot}/%{_kf5_sysconfdir}/xdg/menus/kf5-applications.menu

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING COPYING.LIB README.md
%{_kf5_bindir}/kbuildsycoca5
%{_kf5_libdir}/libKF5Service.so.*
%{_kf5_sysconfdir}/xdg/menus/kf5-applications.menu
%{_kf5_datadir}/kde5/servicetypes/*.desktop
%{_kf5_mandir}/man8/*

%files devel
%{_kf5_includedir}/kservice_version.h
%{_kf5_includedir}/KService
%{_kf5_bindir}/desktoptojson
%{_kf5_libdir}/libKF5Service.so
%{_kf5_libdir}/cmake/KF5Service
%{_kf5_archdatadir}/mkspecs/modules/qt_KService.pri


%changelog
* Mon May 05 2014 dvratil <dvratil@redhat.com> - 4.98.0-3.20140505git9146596a
- Update to git: 9146596a

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-3.20140428git00e3b75e
- Update to git: 00e3b75e

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140428git00e3b75e
- Update to git: 00e3b75e

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140428gitc951637f
- Update to git: c951637f

* Fri Apr 25 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140425git9e9982ad
- Update to git: 9e9982ad

* Wed Apr 23 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140423git81276b32
- Update to git: 81276b32

* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140422git59362034
- Update to git: 59362034

* Mon Apr 21 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140421gitbd57633a
- Update to git: bd57633a

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418gitff1082d3
- Update to git: ff1082d3

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-relase snapshot of 4.96.0

* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-2
- rebuild against new kf5-filesystem

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
