%define framework kactivities

Name:           kf5-%{framework}
Summary:        A KDE Frameworks 5 Tier 3 runtime and library to organize the user work in separate activitie
Version:        4.98.0
Release:        2.20140428gite1ef22a9%{?dist}

License:        GPLv2+ and LGPLv2+
URL:            https://projects.kde.org/projects/kde/kdelibs/kactivities

# git archive --format=tar --prefix=%{name}-%{version}-%{snapshot}/ \
#             --remote=git://anongit.kde.org/kactivities.git | \
# bzip2 -c > ${name}-%{version}-%{snapshot}.tar.bz2
Source0:        kf5-kactivities-e1ef22a9.tar

Obsoletes:      kactivities-qt5
Provides:       kactivities-qt5

BuildRequires:  boost-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtxmlpatterns-devel
BuildRequires:  qt5-qtdeclarative-devel
# FIXME: Why do I need to install all backends when depending on QtSql?
BuildRequires:  qt5-qtbase-ibase
BuildRequires:  qt5-qtbase-odbc
BuildRequires:  qt5-qtbase-mysql
BuildRequires:  qt5-qtbase-postgresql
BuildRequires:  qt5-qtbase-tds

BuildRequires:  kf5-umbrella
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kjs-devel

Requires:       kf5-kactivities-libs%{?_isa} = %{version}-%{release}
Requires:       kf5-kactivities-runtime%{?_isa} = %{version}-%{release}

%description
A KDE Frameworks 5 Tier 3 API for using and interacting with Activities as a
consumer, application adding information to them or as an activity manager.

%package libs
Summary:        Libraries fro KActivities framework
Requires:       kf5-filesystem
%description    libs
%{summary}.

# We have libs-devel and not -devel, so that we can have Requires %{name}-libs
# and prevent kactivities dragging in kactivities-runtime, which conflicts with
# KDE 4 KActivities. This solves the co-installibility at least a bit
%package libs-devel
Summary:        Developer files for %{name}-libs
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

Obsoletes:      kactivties-qt5-devel
Provides:       kactivties-qt5-devel
Conflicts:      kactivities-devel
%description    libs-devel
%{summary}.


%package runtime
Summary:        Runtime for KActivities framework
Conflicts:      kactivities
Provides:       kactivities
%description    runtime
%{summary}.

The runtime module is a drop-in replacement for KActivities runtime module from
KDE 4 and can be safely used with KDE 4.


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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files runtime
%{_kf5_bindir}/kactivitymanagerd
%{_kf5_datadir}/kde5/services/kactivitymanagerd.desktop
%{_kf5_datadir}/kde5/servicetypes/kactivitymanagerd-plugin.desktop
%{_kf5_qtplugindir}/kf5/kactivitymanagerd/

%files libs
%{_kf5_libdir}/libKF5Activities.so.*
%{_kf5_qmldir}/org/kde/activities/

%files libs-devel
%{_kf5_libdir}/libKF5Activities.so
%{_kf5_libdir}/cmake/KF5Activities/
%{_kf5_includedir}/KActivities/
%{_kf5_includedir}/kactivities_version.h
%{_kf5_libdir}/pkgconfig/libKActivities.pc

%changelog
* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140428gite1ef22a9
- Update to git: e1ef22a9

* Mon Apr 28 2014 Daniel Vrátil <dvratil@redhat.com> - 4.98.0-2.20140425gitd1cbd36f
- kf5-kactivities-runtime provides kactivities

* Fri Apr 25 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140425gitd1cbd36f
- Update to git: d1cbd36f

* Wed Apr 23 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140423git5cf107cc
- Update to git: 5cf107cc

* Wed Apr 23 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140423gita87d66aa
- Update to git: a87d66aa

* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140422git367a5ffe
- Update to git: 367a5ffe

* Mon Apr 21 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140421git5792c6a7
- Update to git: 5792c6a7

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418git4576ec65
- Update to git: 4576ec65

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Thu Feb 13 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1
- upgrade to Tier 3 Framework and rename from kactivities-qt5 to kf5-kactivities

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-0.1.20140109git
- fork from kactivities and build against Qt5
- omitted changelog
