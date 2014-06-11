%define         framework networkmanagerqt
%define         git_commit ef654fd
Name:           kf5-%{framework}
Version:        5.0.90
Release:        3.20140611git%{git_commit}%{?dist}
Summary:        A Tier 1 KDE Frameworks 5 module that wraps NetworkManager DBus API

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://projects.kde.org/projects/extragear/libs/libnm-qt
# Source0:        http://download.kde.org/unstable/networkmanagement/%{version}/src/%{name}-%{version}.tar.xz
# # Package from git snapshots using releaseme scripts
#Source0:        http://download.kde.org/unstable/frameworks/4.99.0/%{framework}-4.99.0.tar.xz
Source0:        %{framework}-%{git_commit}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  pkgconfig(NetworkManager) >= 0.9.8
BuildRequires:  pkgconfig(libnm-glib) pkgconfig(libnm-util)

Requires:  NetworkManager >= 0.9.9.0
Requires:  kf5-filesystem

%description
A Tier 2 KDE Frameworks 5 Qt library for NetworkManager

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
Qt libraries and header files for developing applications
that use NetworkManager

%prep
%setup -qn %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} .. \
         -DINCLUDE_INSTALL_DIR:PATH=/usr/include \
         -DKF5_INCLUDE_INSTALL_DIR=/usr/include/KF5
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_kf5_libdir}/libKF5NetworkManagerQt.so.*

%files devel
%{_kf5_libdir}/libKF5NetworkManagerQt.so
%{_kf5_libdir}/cmake/KF5NetworkManagerQt
%{_kf5_includedir}/NetworkManagerQt
%{_kf5_includedir}/networkmanagerqt_version.h
%{_kf5_archdatadir}/mkspecs/modules/qt_NetworkManagerQt.pri

%changelog
* Wed Jun 11 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.90-3.20140611gitef654fd
- Update to latest git snapshot

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.90-2.20140514git107e27d
- Update to latest git snapshot

* Fri Apr 18 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.90-1.20140418git2afe13e
- Upgrade libnm-qt to a Tier 2 KDE Frameworks module kf5-networkmanagerqt

* Thu Apr 03 2014 Daniel Vrátil <dvratil@redhat.com> - 1:0.9.9.1-1.20140403git2afe13e
- Qt 5 fork of libnm-qt
