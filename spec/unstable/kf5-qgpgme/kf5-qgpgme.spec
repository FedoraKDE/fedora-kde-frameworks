%define         framework qgpgme
%define         git_commit 887e946
Name:           kf5-%{framework}
Version:        4.98.0
Release:        2.20140611git%{git_commit}%{?dist}
Summary:        A Tier 3 KDE Frameworks 5 Library that provides gpgme Qt API

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://www.kde.org
# Source0:        http://download.kde.org/unstable/networkmanagement/%{version}/src/%{name}-%{version}.tar.xz
# # Package from git snapshots using releaseme scripts
#Source0:        http://download.kde.org/unstable/frameworks/4.99.0/%{framework}-4.99.0.tar.xz
#Source0:        %{framework}-%{git_commit}.tar.xz
Source0:        kdepimlibs-frameworks-%{git_commit}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-gpgme++-devel

BuildRequires:  gpgme-devel

Requires:       kf5-filesystem

%description
%{Summary}.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kio-devel
Requires:       kf5-gpgme++-devel
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qn kdepimlibs-%{version}

%build
mkdir -p %{_target_platform}/%{framework}
pushd %{_target_platform}/%{framework}
%{cmake_kf5} ../../%{framework}
popd

make %{?_smp_mflags} -C %{_target_platform}/%{framework}


%install
make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}/%{framework}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_kf5_libdir}/libKF5QGpgme.so.*

%files devel
%{_kf5_libdir}/libKF5QGpgme.so
%{_kf5_libdir}/cmake/KF5QGpgme
%{_kf5_includedir}/qgpgme
%{_kf5_includedir}/qgpgme_version.h

%changelog
* Wed Jun 11 2014 Daniel Vrátil <dvratil@redhat.com> - 4.98.0-2.20140611git887e946
- Update to latest git snapshot


* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.98.0-2.20140611gitdda3e7d
- KF5 QGpgme 4.98.0 (git snapshot built from common kdepimlibs/frameworks repo)
