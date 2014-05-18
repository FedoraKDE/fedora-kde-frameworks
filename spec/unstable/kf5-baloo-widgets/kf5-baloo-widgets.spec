%define         framework baloo-widgets
%define         git_commit c9e6dcd
Name:           kf5-%{framework}
Version:        4.96.0
Release:        1.20140518git%{git_commit}%{?dist}
Summary:        A Tier 3 KDE Frameworks 5 module that provides widgets built on top of Baloo

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://www.kde.org
# Source0:        http://download.kde.org/unstable/networkmanagement/%{version}/src/%{name}-%{version}.tar.xz
# # Package from git snapshots using releaseme scripts
#Source0:        http://download.kde.org/unstable/frameworks/4.99.0/%{framework}-4.99.0.tar.xz
#Source0:        %{framework}-%{git_commit}.tar.xz
Source0:        %{framework}-%{git_commit}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kfilemetadata-devel
BuildRequires:  kf5-baloo-devel
BuildRequires:  kf5-umbrella

Requires:       kf5-filesystem

%description
%{Summary}.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qn %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ../ \
         -DKDEPIM_SUPPORT_BUILD:BOOL=ON \
         -DINCLUDE_INSTALL_DIR:PATH=/usr/include/KF5
# FIXME: Remove ^^ once fixed upstream
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_kf5_libdir}/libbaloowidgets.so.*

%files devel
%{_kf5_libdir}/libbaloowidgets.so
%{_kf5_libdir}/cmake/BalooWidgets
%{_kf5_includedir}/baloo

%changelog
* Sun May 18 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1.20140518gitc9e6dcd
- KF5 Baloo Widgets 4.90.0 (git snapshot built from common kdepimlibs/frameworks repo)
