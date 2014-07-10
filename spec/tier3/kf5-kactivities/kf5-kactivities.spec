%define framework kactivities

Name:           kf5-%{framework}
Summary:        A KDE Frameworks 5 Tier 3 to organize user work into separate activities
Version:        5.0.0
Release:        1%{?dist}

License:        GPLv2+ and LGPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}-%{snapshot}/ \
#             --remote=git://anongit.kde.org/kactivities.git | \
# bzip2 -c > ${name}-%{version}-%{snapshot}.tar.bz2
Source0:        http://download.kde.org/stable/frameworks/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  boost-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtxmlpatterns-devel
BuildRequires:  qt5-qtdeclarative-devel

BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kwindowsystem-devel

Requires:       kf5-kactivities-libs%{?_isa} = %{version}-%{release}

Conflicts:      kactivities < 0:4.90.0
Provides:       kactivities%{?_isa} = 0:%{version}-%{release}
Provides:       kactivities = 0:%{version}-%{release}

%description
A KDE Frameworks 5 Tier 3 API for using and interacting with Activities as a
consumer, application adding information to them or as an activity manager.


%package libs
Summary:        Libraries fro KActivities framework
Requires:       kf5-filesystem
%description    libs
%{summary}.


%package devel
Summary:        Developer files for %{name}-libs
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
%description    devel
%{summary}.


%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang kactivities5_qt --with-qt --all-name

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%files
%doc README README.md README.packagers README.developers MAINTAINER
%{_kf5_bindir}/kactivitymanagerd
%{_kf5_datadir}/kservices5/kactivitymanagerd.desktop
%{_kf5_datadir}/kservicetypes5/kactivitymanagerd-plugin.desktop
%{_kf5_qtplugindir}/kactivitymanagerd/

%files libs -f kactivities5_qt.lang
%{_kf5_libdir}/libKF5Activities.so.*
%{_kf5_qmldir}/org/kde/activities/

%files devel
%{_kf5_libdir}/libKF5Activities.so
%{_kf5_libdir}/cmake/KF5Activities/
%{_kf5_includedir}/KActivities/
%{_kf5_includedir}/kactivities_version.h
%{_kf5_libdir}/pkgconfig/libKActivities.pc
%{_kf5_archdatadir}/mkspecs/modules/qt_KActivities.pri


%changelog
* Thu Jul 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- KDE Frameworks 5.0.0

* Tue Jun 03 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-1
- KDE Frameworks 4.100.0

* Mon May 19 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-5
- Fix provides: kactivities(4) has an epoch set

* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-4
- Add Conflicts to -runtime

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-3
- Remove Conflicts: kactivities, per change in kactivties(4) package

* Tue May 13 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-2
- Add missing kf5-kactivities package
- Fix Conflicts/Provides versions

* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0
- KDE Frameworks 4.99.0

* Mon Apr 28 2014 Daniel Vrátil <dvratil@redhat.com> - 4.98.0-2.20140425gitd1cbd36f
- kf5-kactivities-runtime provides kactivities

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Thu Feb 13 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1
- upgrade to Tier 3 Framework and rename from kactivities-qt5 to kf5-kactivities

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-0.1.20140109git
- fork from kactivities and build against Qt5
- omitted changelog
