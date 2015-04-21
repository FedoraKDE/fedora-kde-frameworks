%define         base_name milou

Name:           plasma-%{base_name}
Version:        5.2.2
Release:        1%{?dist}
Summary:        A dedicated KDE search application built on top of Baloo

License:        GPLv2+
URL:            https://projects.kde.org/kde/workspace/milou

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{base_name}-%{version}.tar.xz

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
Provides:       kde-plasma-milou = %{version}-%{release}

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
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang milou --with-qt --all-name

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f milou.lang
%{_kf5_qtplugindir}/miloutextplugin.so
%{_kf5_datadir}/kservicetypes5/miloupreviewplugin.desktop
%{_kf5_datadir}/kservices5/plasma-applet-org.kde.milou.desktop
%{_kf5_datadir}/kservices5/miloutextpreview.desktop
%{_libdir}/libmilou.so.*
%{_kf5_qmldir}/org/kde/milou
%{_datadir}/plasma/plasmoids/org.kde.milou


%changelog
* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Tue Jan 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Mon Jan 05 2015 Jan Grulich <jgrulich@redhat.com> - 5.1.1-2
- Better URL
  Used make install instead of make_install macro
  Fixed macros

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- Plasma 5.1.2

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.2-1
- Plasma 5.0.2

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Thu Jul 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140515gitc11b832c
- Intial snapshot
