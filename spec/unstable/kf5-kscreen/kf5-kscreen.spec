%define         framework kscreen
%define         git_commit 4ab583f

Name:           kf5-%{framework}
Version:        4.90.0
Release:        2.20140611git%{git_commit}%{?dist}
Summary:        A Tier 3 KDE Frameworks 5 Library with API to control screen settings

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://www.kde.org
# Source0:        http://download.kde.org/unstable/networkmanagement/%{version}/src/%{name}-%{version}.tar.xz
# # Package from git snapshots using releaseme scripts
#Source0:        http://download.kde.org/unstable/frameworks/4.99.0/%{framework}-4.99.0.tar.xz
#Source0:        %{framework}-%{git_commit}.tar.xz
Source0:        %{framework}-%{git_commit}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXrandr-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

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
%{cmake_kf5} .. \
        -DPLUGIN_INSTALL_DIR=%{_kf5_qtplugindir}
# FIXME Remove ^^ once fixed upstream
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_kf5_libdir}/libKF5Screen.so.*
%{_kf5_plugindir}/kscreen/


%files devel
%{_kf5_libdir}/libKF5Screen.so
%{_kf5_libdir}/cmake/KF5Screen
%{_kf5_includedir}/KScreen
%{_kf5_includedir}/kscreen_version.h
%{_kf5_archdatadir}/mkspecs/modules/qt_KScreen.pri
%{_kf5_libdir}/pkgconfig/kscreen2.pc

%changelog
* Wed Jun 11 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.0-2.20140611git4ab583f
- Update to latest git snapshot

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 2.0.0-2.20140611gitdda3e7d
- Initial version
