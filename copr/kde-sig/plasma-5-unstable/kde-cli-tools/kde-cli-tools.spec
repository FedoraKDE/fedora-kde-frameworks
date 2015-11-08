Name:           kde-cli-tools
Version: 5.4.90
Release: 1%{?dist}
Summary:        Tools based on KDE Frameworks 5 to better interact with the system

License:        GPLv2+
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
BuildRequires:  kf5-kinit-devel >= 5.10.0-3
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kdesu-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kwindowsystem-devel

Requires:       kf5-filesystem

# probably could be unversioned, but let's play it safe so we can avoid adding Conflicts: -- rex
Requires:       kdesu = 1:%{version}-%{release}

# libkdeinit5_kcmshell5
%{?kf5_kinit_requires}

%description
Provides several KDE and Plasma specific command line tools to allow
better interaction with the system.

%package -n kdesu
Summary: Runs a program with elevated privileges
Epoch: 1
Conflicts: kde-runtime < 14.12.3-2
Conflicts: kde-runtime-docs < 14.12.3-2
## added deps below avoidable to due main pkg Requires: kdesu -- rex
# upgrade path, when kdesu was introduced
#Obsoletes: kde-cli-tools < 5.2.1-3
#Requires: %{name} = %{version}-%{release}
%description -n kdesu
%{summary}.


%prep
%setup -q -n %{name}-%{version}

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang kdeclitools_qt --with-qt --with-kde --all-name

ln -s %{_kf5_libexecdir}/kdesu %{buildroot}%{_bindir}/kdesu

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
%{_kf5_libexecdir}/kdeeject
%{_kf5_libdir}/libkdeinit5_kcmshell5.so
%{_kf5_qtplugindir}/kcm_filetypes.so
%{_kf5_datadir}/kservices5/filetypes.desktop

%files -n kdesu
%{_bindir}/kdesu
%{_kf5_libexecdir}/kdesu
%{_mandir}/man1/kdesu.1.gz
%{_datadir}/doc/HTML/*/kdesu


%changelog
* Sun Nov 08 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.90-1
- Plasma 5.4.90

* Thu Nov 05 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.3-1
- Plasma 5.4.3

* Thu Oct 01 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-1
- 5.4.2

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-1
- 5.4.1

* Fri Aug 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- Plasma 5.4.0

* Thu Aug 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-1
- Plasma 5.3.95

* Thu Jun 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.2-1
- Plasma 5.3.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 01 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-2
- %%{?kf5_kinit_requires}

* Tue May 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma 5.3.1

* Mon Apr 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- Plasma 5.3.0

* Wed Apr 22 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-1
- Plasma 5.2.95

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Thu Mar 12 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-5
- kdesu: Epoch:1 to be able to upgrade from kdesu-14.12.x

* Sat Mar 07 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-4
- kdesu: Conflicts: kde-runtime < 14.12.3-2

* Sat Mar 07 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-3
- kdesu subpkg (#1199720)

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Thu Jan 29 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-2
- Provide kdesu symlink in /usr/bin (instead of kde-runtime)

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

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
