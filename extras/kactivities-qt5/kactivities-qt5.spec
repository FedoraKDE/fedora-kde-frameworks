%define snapshot        20140109

Name:           kactivities-qt5
Summary:        API for using and interacting with Activities (Qt5 version)
Version:        5.0.0
Release:        0.1.%{snapshot}git

License:        GPLv2+ and LGPLv2+
URL:            https://projects.kde.org/projects/kde/kdelibs/kactivities

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/kactivities.git frameworks | \
# gzip -c > ${name}-%{snapshot}.tar.gz
Source0:        %{name}-%{snapshot}.tar.gz

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtxmlpatterns-devel

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
%setup -q 


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} .. -DCMAKE_PREFIX_PATH=/opt/kf5/
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_kf5_bindir}/kactivitymanagerd
%{_kf5_libdir}/libKActivities.so.*
%{_kf5_libdir}/plugins/kf5/activitymanager/
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
* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- fork from kactivities and build against Qt5
- omitted changelog

* Wed Dec 18 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.12.0-1
- 4.12.0

* Sun Dec 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.97-1
- 4.11.97

* Thu Nov 21 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.95-1
- 4.11.95

* Fri Nov 15 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.90-1
- 4.11.90

* Sat Nov 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.3-1
- 4.11.3

* Sat Sep 28 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.2-1
- 4.11.2

* Tue Sep 03 2013 Rex Dieter <rdieter@fedoraproject.org> 4.11.1-1
- 4.11.1

* Thu Aug 08 2013 Than Ngo <than@redhat.com> - 4.11.0-1
- 4.11.0
