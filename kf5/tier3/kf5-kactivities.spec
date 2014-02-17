%define framework kactivities

Name:           kf5-%{framework}
Summary:        A KDE Frameworks 5 Tier 3 runtime and library to organize the user work in separate activitie
Version:        4.96.0
Release:        1%{?dist}

License:        GPLv2+ and LGPLv2+
URL:            https://projects.kde.org/projects/kde/kdelibs/kactivities

# git archive --format=tar --prefix=%{name}-%{version}-%{snapshot}/ \
#             --remote=git://anongit.kde.org/kactivities.git | \
# bzip2 -c > ${name}-%{version}-%{snapshot}.tar.bz2
Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz

Obsoletes:      kactivities-qt5
Provides:       kactivities-qt5

BuildRequires:  boost-devel

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtxmlpatterns-devel
BuildRequires:  qt5-qtdeclarative-devel
# FIXME: Why do I need to isntall all backends when depending on QtSql?
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
%{_kf5_datadir}/kde5/servicetypes/activitymanager-plugin.desktop
%{_kf5_qtplugindir}/kf5/activitymanager/
%{_kf5_datadir}/ontology/kde/kao.*

%files libs
%{_kf5_libdir}/libKF5Activities.so.*
%{_kf5_libdir}/qml/org/kde/activities/

%files libs-devel
%{_kf5_libdir}/libKF5Activities.so
%{_kf5_libdir}/cmake/KF5Activities/
%{_kf5_includedir}/KActivities/
%{_kf5_includedir}/kactivities_version.h
%{_kf5_libdir}/pkgconfig/libKActivities.pc

%changelog
* Thu Feb 13 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1
- upgrade to Tier 3 Framework and rename from kactivities-qt5 to kf5-kactivities

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-0.1.20140109git
- fork from kactivities and build against Qt5
- omitted changelog
