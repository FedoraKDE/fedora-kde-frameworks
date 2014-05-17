%define         framework kblog
%define         git_commit dda3e7d
Name:           kf5-%{framework}
Version:        4.98.0
Release:        1.20140514git%{git_commit}%{?dist}
Summary:        A Tier 3 KDE Frameworks 5 Library for working with blogging CMS

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
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kcalcore-devel
BuildRequires:  kf5-syndication-devel
BuildRequires:  kf5-kxmlrpcclient-devel

BuildRequires:  boost-devel

Requires:       kf5-filesystem

%description
%{Summary}.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kcalcore-devel
Requires:       kf5-syndication-devel
Requires:       kf5-kxmlrpcclient-devel
Requires:       kf5-kdelibs4support-devel
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
%{_kf5_libdir}/libKF5Blog.so.*

%files devel
%{_kf5_libdir}/libKF5Blog.so
%{_kf5_libdir}/cmake/KF5Blog
%{_kf5_includedir}/KBlog
%{_kf5_includedir}/kblog_version.h
%{_kf5_archdatadir}/mkspecs/modules/qt_KBlog.pri

%changelog
* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.98.0-1.20140514gitdda3e7d
- KF5 KBlog 4.98.0 (git snapshot built from common kdepimlibs/frameworks repo)
