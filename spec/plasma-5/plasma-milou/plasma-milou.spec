%define base_name milou

Name:           plasma-%{base_name}
Version:        5.0.0
Release:        1%{?dist}
Summary:        A dedicated KDE search application built on top of Baloo

License:        GPLv2+
URL:            http://www.kde.org
Source0:        http://download.kde.org/stable/plasma/%{version}/%{base_name}-%{version}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtxmlpatterns-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  qt5-qtscript-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-krunner-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-baloo-devel

Requires:       kf5-filesystem

Obsoletes:      kde-plasma-milou < 5.0.0

%description
%{summary}.

%prep
%setup -q -n %{base_name}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}
%find_lang milou --with-qt --all-name

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f milou.lang
%{_kf5_datadir}/kservicetypes5/miloupreviewplugin.desktop
%{_kf5_datadir}/kservices5/plasma-applet-org.kde.milou.desktop
%{_libdir}/libmilou.so.*
%{_qt5_prefix}/qml/org/kde/milou
%{_datadir}/plasma/plasmoids/org.kde.milou


%changelog
* Thu Jul 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140515gitc11b832c
- Intial snapshot
