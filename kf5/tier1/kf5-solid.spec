#%define snapshot 20140205
%define framework solid

Name:           kf5-%{framework}
Version:        4.98.0
Release:        2%{?dist}
Summary:        KDE Frameworks 5 Tier 1 integration module that provides hardware information

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  libupnp-devel
BuildRequires:  systemd-devel

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel

%description
Solid provides the following features for application developers:
 - Hardware Discovery
 - Power Management
 - Network Management


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        runtime
Summary:        Runtime for %{name}
Conflicts:      kde-runtime

%description    runtime
%{summary}.
The runtime package contains solid-hardware, which is a tool for querying
your hardware from the command line.

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

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING.LIB README.md TODO
%{_kf5_libdir}/qml/org/kde/solid/*
%{_kf5_libdir}/libKF5Solid.so.*


%files devel
%{_kf5_datadir}/dbus-1/interfaces/*
%{_kf5_includedir}/solid_version.h
%{_kf5_includedir}/Solid
%{_kf5_libdir}/libKF5Solid.so
%{_kf5_libdir}/cmake/KF5Solid
%{_kf5_archdatadir}/mkspecs/modules/qt_Solid.pri

%files runtime
%{_kf5_bindir}/solid-hardware


%changelog
* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-2
- Move solid-hardware to kf5-solid-runtime

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-release snapshot of 4.96.0

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
