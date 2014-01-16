%define framework kprintutils

Name:           kf5-%{framework}
Version:        4.95.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 addon with utilities for printing

License:        GPLv2+
URL:            http://www.kde.org
Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  libX11-devel
BuildRequires:  attica-qt5-devel

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-knotifications-devel

%description
KDE Frameworks 5 Tier 3 addon with utilities for printing


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

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
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5PrintUtils.so.*

%files devel
%{_kf5_includedir}/kprintutils_version.h
%{_kf5_includedir}/KPrintUtils
%{_kf5_libdir}/libKF5PrintUtils.so
%{_kf5_libdir}/cmake/KF5PrintUtils


%changelog
* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
