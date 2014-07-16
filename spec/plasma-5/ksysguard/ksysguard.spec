Name:           ksysguard
Version:        5.0.0
Release:        1%{?dist}
Summary:        KDE Process Management application

License:        GPLv2+
URL:            http://www.kde.org
Source0:        http://download.kde.org/stable/plasma/%{version}/%{name}-%{version}.tar.xz

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

%description
%{summary}.

%prep
%setup -q

%build

sed -e "s/PO_FILES //" -i po/*/CMakeLists.txt

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}
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
%{_datadir}/applications/ksysguard.desktop
%{_datadir}/doc/HTML/en/ksysguard
%{_datadir}/icons/hicolor/*/apps/*.png
%{_kf5_datadir}/knotifications5/ksysguard.notifyrc

%changelog
* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140515gitf7a2bbe
- Intial snapshot
