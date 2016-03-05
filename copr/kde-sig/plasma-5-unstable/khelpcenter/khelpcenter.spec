Name:    khelpcenter
Summary: Show documentation for KDE applications
# Override khelpcenter subpackage from kde-runtime-15.04 (no longer built)
Epoch:   1
Version: 5.5.95
Release: 1%{?dist}

License: GPLv2 or GPLv3
URL:     https://projects.kde.org/khelpcenter

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  extra-cmake-modules
# _kde4_* macros
BuildRequires:  kde-filesystem
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-khtml-devel
BuildRequires:  kf5-kinit-devel >= 5.10.0-3
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel

Requires:       kf5-filesystem

# libkdeinit5_*
%{?kf5_kinit_requires}

%description
%{summary}.


%prep
%setup -q


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
%doc README.htdig README.metadata
%license COPYING
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
%lang(ca) %{_kf5_docdir}/HTML/ca/fundamentals/
%lang(ca) %{_kf5_docdir}/HTML/ca/glossary/
%lang(ca) %{_kf5_docdir}/HTML/ca/khelpcenter/
%lang(ca) %{_kf5_docdir}/HTML/ca/onlinehelp/
%lang(en) %{_kf5_docdir}/HTML/en/fundamentals/
%lang(en) %{_kf5_docdir}/HTML/en/khelpcenter/
%lang(en) %{_kf5_docdir}/HTML/en/onlinehelp/
%lang(it) %{_kf5_docdir}/HTML/it/khelpcenter/
%lang(nl) %{_kf5_docdir}/HTML/nl/khelpcenter/
%lang(pt_BR) %{_kf5_docdir}/HTML/pt_BR/khelpcenter/
%lang(sr) %{_kf5_docdir}/HTML/sr/khelpcenter/
%lang(sr@latin) %{_kf5_docdir}/HTML/sr@latin/khelpcenter/
%lang(sv) %{_kf5_docdir}/HTML/sv/khelpcenter/
%lang(uk) %{_kf5_docdir}/HTML/uk/khelpcenter/


%changelog
* Sat Mar 05 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.95-1
- Plasma 5.5.95

* Tue Mar 01 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.5-1
- Plasma 5.5.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.4-1
- Plasma 5.5.4

* Thu Jan 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.3-1
- Plasma 5.5.3

* Wed Jan 06 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:5.5.2-2
- .spec cosmetics, (re)enable all HTML docs

* Thu Dec 31 2015 Rex Dieter <rdieter@fedoraproject.org> - 1:5.5.2-1
- 5.5.2

* Fri Dec 18 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.1-1
- Plasma 5.5.1

* Thu Dec 03 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.0-1
- Plasma 5.5.0

* Wed Nov 25 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.95-1
- Plasma 5.4.95

* Thu Nov 05 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.3-1
- Plasma 5.4.3

* Thu Oct 01 2015 Rex Dieter <rdieter@fedoraproject.org> - 1:5.4.2-1
- 5.4.2

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 1:5.4.1-1
- 5.4.1

* Fri Aug 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- Plasma 5.4.0

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
