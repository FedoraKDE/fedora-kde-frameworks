Name:           khelpcenter
Version:        5.3.95
Release:        1%{?dist}
Summary:        Application to show KDE Application's documentation
# Override khelpcenter subpackage from kde-runtime-15.04 (no longer built)
Epoch:          1

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
BuildRequires:  kf5-kinit-devel >= 5.10.0-3
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-khtml-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kdoctools-devel

BuildRequires:  desktop-file-utils

# _kde4_* macros
BuildRequires:  kde-filesystem

Requires:       kf5-filesystem

# libkdeinit5_*
%{?kf5_kinit_requires}

%description
%{summary}.


%prep
%setup -q

mv doc/CMakeLists.txt doc/CMakeLists.txt.en_only
grep 'add_subdirectory(en)' doc/CMakeLists.txt.en_only > doc/CMakeLists.txt


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang khelpcenter5 --with-qt --all-name

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
%{_kf5_datadir}/khelpcenter/
%{_kf5_datadir}/kxmlgui5/khelpcenter/khelpcenterui.rc
%{_datadir}/applications/org.kde.Help.desktop
%{_datadir}/config.kcfg/khelpcenter.kcfg
%{_datadir}/kservices5/khelpcenter.desktop
%{_datadir}/dbus-1/interfaces/org.kde.khelpcenter.kcmhelpcenter.xml
%{_kde4_datadir}/services/khelpcenter.desktop
%{_kde4_datadir}/kde4/services/khelpcenter.desktop
%lang(en) /usr/share/doc/HTML/en/fundamentals/
%lang(en) /usr/share/doc/HTML/en/khelpcenter/
%lang(en) /usr/share/doc/HTML/en/onlinehelp/


%changelog
* Thu Aug 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-1
- Plasma 5.3.95

* Thu Jun 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.2-1
- Plasma 5.3.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 01 2015 Rex Dieter <rdieter@fedoraproject.org> - 1:5.3.1-3
- (re)enable en-only HTML docs (others provided by kde-l10n)
- +%%{?kf5_kinit_requires},
- .spec cosmetics

* Fri May 29 2015 Daniel Vrátil <dvratil@redhat.com> - 1:5.3.1-2
- bump Epoch to override khelpcenter subpackage from kde-runtime-15.04

* Tue May 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma 5.3.1

* Mon Apr 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- Plasma 5.3.0

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
