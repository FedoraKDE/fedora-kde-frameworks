#
# TODO: Split packages
#  -core
#  -widgets
#  -agent-base
#  -xml
#

%global         framework akonadi
%global         git_commit dda3e7d
Name:           kf5-%{framework}
Version:        4.98.0
Release:        1.20140514git%{git_commit}%{?dist}
Summary:        A Tier 3 KDE Frameworks 5 Library that provides access to PIM storage

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://www.kde.org
# Source0:        http://download.kde.org/unstable/networkmanagement/%{version}/src/%{name}-%{version}.tar.xz
# # Package from git snapshots using releaseme scripts
#Source0:        http://download.kde.org/unstable/frameworks/4.99.0/%{framework}-4.99.0.tar.xz
#Source0:        %{framework}-%{git_commit}.tar.xz
Source0:        kdepimlibs-frameworks-%{git_commit}.tar.xz

Patch0:         akonadi-selftest.patch
Patch1:         akonadi-fix-config.patch

BuildRequires:  qt5-qtbase-devel
BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  akonadi-qt5-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-qttools-static
BuildRequires:  boost-devel
BuildRequires:  libxml2-devel

BuildRequires:  chrpath

Requires:       kf5-filesystem

%description
%{Summary}.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kio-devel
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qn kdepimlibs-%{version}

%patch0 -p1 -b .selftest
%patch1 -p1 -b .config

%build
mkdir -p %{_target_platform}/%{framework}
pushd %{_target_platform}/%{framework}
%{cmake_kf5} ../../%{framework}
popd

make %{?_smp_mflags} -C %{_target_platform}/%{framework}


%install
make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}/%{framework}

chrpath --delete %{buildroot}/%{_kf5_qtplugindir}/designer/akonadiwidgets.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_kf5_libdir}/libKF5AkonadiAgentBase.so.*
%{_kf5_libdir}/libKF5AkonadiCore.so.*
%{_kf5_libdir}/libKF5AkonadiWidgets.so.*
%{_kf5_libdir}/libKF5AkonadiXml.so.*
%{_kf5_bindir}/akonadiselftest
%{_kf5_qtplugindir}/designer/akonadiwidgets.so
%{_kf5_datadir}/config.kcfg/resourcebase.kcfg

%files devel
%{_kf5_libdir}/libKF5AkonadiAgentBase.so
%{_kf5_libdir}/libKF5AkonadiCore.so
%{_kf5_libdir}/libKF5AkonadiWidgets.so
%{_kf5_libdir}/libKF5AkonadiXml.so
%{_kf5_libdir}/cmake/KF5Akonadi
%{_kf5_includedir}/AkonadiAgentBase
%{_kf5_includedir}/AkonadiCore
%{_kf5_includedir}/AkonadiWidgets
%{_kf5_includedir}/AkonadiXml
%{_kf5_includedir}/akonadi_version.h
%{_kf5_archdatadir}/mkspecs/modules/qt_AkonadiAgentBase.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_AkonadiCore.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_AkonadiWidgets.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_AkonadiXml.pri
%{_kf5_datadir}/kf5/akonadi/kcfg2dbus.xsl
%{_kf5_datadir}/kf5/akonadi/akonadi-xml.xsd
%{_kf5_bindir}/akonadi2xml

%changelog
* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.98.0-1.20140514gitdda3e7d
- KF5 Akonadi 4.98.0 (git snapshot built from common kdepimlibs/frameworks repo)
