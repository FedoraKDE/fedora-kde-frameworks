Name:           kde-cli-tools
Version:        5.2.0
Release:        1%{?dist}
Summary:        Tools based on KDE Frameworks 5 to better interact with the system

License:        GPLv2+ and LGPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/kde-cli-tools

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kf5-rpm-macros

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kdesu-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kwindowsystem-devel

Requires:       kf5-filesystem

Provides:       kdesu = %{version}-%{release}

%description
Provides several KDE and Plasma specific command line tools to allow
better interaction with the system.

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
%find_lang kdeclitools_qt --with-qt --with-kde --all-name


%files -f kdeclitools_qt.lang
%{_bindir}/kcmshell5
%{_bindir}/kde-open5
%{_bindir}/kdecp5
%{_bindir}/kdemv5
%{_bindir}/keditfiletype5
%{_bindir}/kioclient5
%{_bindir}/kmimetypefinder5
%{_bindir}/kstart5
%{_bindir}/ksvgtopng5
%{_bindir}/ktraderclient5
%{_kf5_libdir}/libkdeinit5_kcmshell5.so
%{_kf5_qtplugindir}/kcm_filetypes.so
%{_libexecdir}/kdeeject
%{_libexecdir}/kdesu
%{_kf5_datadir}/kservices5/filetypes.desktop
%{_mandir}/man1/kdesu.1.gz
%{_docdir}/HTML/en/kdesu

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

* Wed Jul 23 2014 Daniel Vrátil <dvratli@redhat.com> - 5.0.0-2
- Rebuild

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Mon May 19 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1.20140519git60d6c72
- initial version
