Name:           khelpcenter
Version:        5.2.95
Release:        1%{?dist}
Summary:        Application to show KDE Application's documentation

License:        GPLv2 or GPLv3
URL:            https://projects.kde.org/projects/kde/workspace/khelpcenter

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros

BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kinit-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-khtml-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kdoctools-devel

BuildRequires:  desktop-file-utils

# _kde4_* macros
BuildRequires:  kde-filesystem

Requires:       kf5-filesystem

%description
%{summary}.

%prep
%setup -q -n %{name}-%{version}


%build
sed -i "s/add_subdirectory( doc )/#add_subdirectory( doc )/" CMakeLists.txt

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang khelpcenter5 --with-qt --with-kde --all-name

# Provide khelpcenter service for KDE 3 and KDE 4 applications
mkdir -p %{buildroot}/%{_kde4_datadir}/services
cp %{buildroot}/%{_datadir}/kservices5/khelpcenter.desktop \
   %{buildroot}/%{_kde4_datadir}/services
mkdir -p %{buildroot}/%{_kde4_datadir}/kde4/services
cp %{buildroot}/%{_datadir}/kservices5/khelpcenter.desktop \
   %{buildroot}/%{_kde4_datadir}/kde4/services


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.kde.Help.desktop

%files -f khelpcenter5.lang
%doc README.htdig README.metadata COPYING
%{_bindir}/khelpcenter
%{_libexecdir}/khc_indexbuilder
%{_libexecdir}/khc_htdig.pl
%{_libexecdir}/khc_htsearch.pl
%{_libexecdir}/khc_mansearch.pl
%{_libexecdir}/khc_docbookdig.pl
%{_kf5_libdir}/libkdeinit5_khelpcenter.so
%{_kf5_datadir}/khelpcenter
%{_kf5_datadir}/kxmlgui5/khelpcenter/khelpcenterui.rc
%{_datadir}/applications/org.kde.Help.desktop
%{_datadir}/config.kcfg/khelpcenter.kcfg
%{_datadir}/kservices5/khelpcenter.desktop
%{_datadir}/dbus-1/interfaces/org.kde.khelpcenter.kcmhelpcenter.xml
%{_kde4_datadir}/services/khelpcenter.desktop
%{_kde4_datadir}/kde4/services/khelpcenter.desktop

%changelog
* Wed Apr 22 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-1
- Plasma 5.2.95

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Tue Jan 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-2.beta
- Updated tarball

* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Tue Jan 06 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-3
- better URL
- remove unnecessary scriptlets
- validate desktop files
- ship service files for KDE 3 and KDE 4
- fix license

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

* Wed Aug 06 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-2
- No longer obsoletes kde-runtime-khelpcenter

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140514git6bfae0d
- Intial snapshot
