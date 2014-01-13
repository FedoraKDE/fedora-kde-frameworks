%define snapshot 20140109

Name:           kactivities-qt5
Summary:        API for using and interacting with Activities (Qt5 version)
Version:        5.0.0
Release:        0.1.%{snapshot}git

License:        GPLv2+ and LGPLv2+
URL:            https://projects.kde.org/projects/kde/kdelibs/kactivities

# git archive --format=tar --prefix=%{name}-%{version}-%{snapshot}/ \
#             --remote=git://anongit.kde.org/kactivities.git frameworks | \
# bzip2 -c > ${name}-%{version}-%{snapshot}.tar.bz2
Source0:        %{name}-%{version}-%{snapshot}.tar.bz2

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
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kservice-devel

%description
API for using and interacting with Activities as a consumer,
application adding information to them or as an activity manager.


%package devel
Summary:        Developer files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
%{summary}.


%prep
%setup -q -n %{name}-%{version}-%{snapshot}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} .. -DCMAKE_PREFIX_PATH=/opt/kf5/
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

mkdir -p %{buildroot}/%{_kf5_plugindir}/plugins && mv %{buildroot}/%{_kf5_plugindir}/activitymanager %{buildroot}/%{_kf5_plugindir}/plugins/activitymanager

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_kf5_bindir}/kactivitymanagerd
%{_kf5_libdir}/libKActivities.so.*
%{_kf5_plugindir}/plugins/activitymanager/
%{_kf5_libdir}/qml/org/kde/activities/
%{_kf5_datadir}/kde5/services/kactivitymanagerd.desktop
%{_kf5_datadir}/kde5/servicetypes/activitymanager-plugin.desktop
%{_kf5_datadir}/ontology/kde/*

%files devel
%{_kf5_libdir}/libKActivities.so
%{_kf5_libdir}/cmake/KActivities/
%{_kf5_includedir}/kactivities/
%{_kf5_includedir}/KDE/KActivities/
%{_kf5_includedir}/kactivities_version.h
%{_kf5_libdir}/pkgconfig/libKActivities.pc

%changelog
* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-0.1.20140109git
- fork from kactivities and build against Qt5
- omitted changelog
