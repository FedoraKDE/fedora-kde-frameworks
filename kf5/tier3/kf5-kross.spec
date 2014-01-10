%define framework kross

Name:           kf5-%{framework}
Version:        4.95.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution for application scripting

License:        LGPL2+
URL:            http://www.kde.org
Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  attica-qt5-devel

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  qt5-qtxmlpatterns-devel
BuildRequires:  qt5-qttools-static

BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-knotifications-devel

Requires:       kf5-kross-core
Requires:       kf5-kross-ui

%description
KDE Frameworks 5 Tier 3 solution for application scripting


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        core
Summary:        Non-gui part of the Kross framework

%description    core
Non-gui part of the Kross framework.

%package        ui
Summary:        Gui part of the Kross framework
Requires:       kf5-kross-core

%description    ui
Gui part of the Kross framework.

%package        doc
Summary:        Documentation and user manuals for the Kross framework

%description    doc
Documentation and user manuals for the Kross framework

%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} DESTDIR=%{buildroot} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files core
%{_kf5_bindir}/kf5kross
%{_kf5_libdir}/libKF5KrossCore.so
%{_kf5_qtplugindir}/krossqts.so
%{_kf5_qtplugindir}/scripts/libkrossqtsplugin.so.*

%files ui
%{_kf5_libdir}/libKF5KrossUi.so

%files doc
%doc COPYING.LIB README.md
%{_kf5_datadir}/man/*

%files devel
%{_kf5_includedir}/kross_version.h
%{_kf5_includedir}/Kross
%{_kf5_libdir}/libKF5Kross*.so
%{_kf6_libdir}/plugins/scripts/libkrossqtsplugin.so
%{_kf5_libdir}/cmake/KF5Kross


%changelog
* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan 4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
