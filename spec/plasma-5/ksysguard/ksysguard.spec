Name:           ksysguard
Version:        5.1.95
Release:        1.beta%{?dist}
Summary:        KDE Process Management application

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/ksysguard

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-knewstuff-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-ksysguard-devel
BuildRequires:  kf5-kdoctools-devel

BuildRequires:  lm_sensors-devel

Requires:       kf5-filesystem

Obsoletes:      ksysguardd < 5.0.0-1

%description
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang ksysguard5 --with-qt --all-name

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f ksysguard5.lang
%doc COPYING COPYING.DOC README
%{_bindir}/ksysguard
%{_bindir}/ksysguardd
%{_kf5_libdir}/libkdeinit5_ksysguard.so
%{_datadir}/ksysguard
%config %{_sysconfdir}/xdg/ksysguard.knsrc
%config %{_sysconfdir}/ksysguarddrc
%{_datadir}/applications/org.kde.ksysguard.desktop
%{_datadir}/doc/HTML/en/ksysguard
%{_datadir}/icons/hicolor/*/apps/*.png
%{_kf5_datadir}/knotifications5/ksysguard.notifyrc
%{_kf5_datadir}/kxmlgui5/ksysguard

%changelog
* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

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

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140515gitf7a2bbe
- Intial snapshot
