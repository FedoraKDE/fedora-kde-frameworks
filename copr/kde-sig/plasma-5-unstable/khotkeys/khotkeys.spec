Name:    khotkeys
Version: 5.5.95
Release: 1%{?dist}
Summary: Application to configure hotkeys in KDE

License: GPLv2+
URL:     https://projects.kde.org/projects/kde/workspace/khotkeys

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

## downstream patches
# kcm_hotkeys, use qdbusviewer-qt5, see also http://bugs.kde.org/329094
Patch100: khotkeys-5.4.2-qdbusviewer-qt5.patch

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-rpm-macros
BuildRequires:  libX11-devel
BuildRequires:  plasma-workspace-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

Requires:       kf5-filesystem
# not sure if we want a hard dep on this (yet) -- rex
%if 0%{?fedora} > 21
Recommends:     qt5-qdbusviewer
%endif

# when khotkeys was split out of kde-workspace-4.11.x
Conflicts:      kde-workspace < 4.11.15-3

# upgrade path from khotkeys-libs-4.11.x (skip Provides for now, it was only ever a private library)
Obsoletes:      khotkeys-libs < 5.0.0
#Provides:       khotkeys-libs = %{version}-%{release}

%description
An advanced editor component which is used in numerous KDE applications
requiring a text editing component.

%package        devel
Summary:        Development files for %{name}
# strictly speaking, not required in this case, but still often expected to pull in subpkg -- rex
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}

%patch100 -p1 -b .qtdbusviewer-qt5


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang khotkeys


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f khotkeys.lang
%license COPYING
%{_kf5_libdir}/libkhotkeysprivate.so.*
%{_kf5_qtplugindir}/kcm_hotkeys.so
%{_kf5_plugindir}/kded/khotkeys.so
%{_kf5_datadir}/kservices5/khotkeys.desktop
%{_datadir}/khotkeys/
%{_datadir}/doc/HTML/en/kcontrol/khotkeys/

%files devel
%{_datadir}/dbus-1/interfaces/org.kde.khotkeys.xml
%{_libdir}/cmake/KHotKeysDBusInterface/


%changelog
* Sat Mar 05 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.95-1
- Plasma 5.5.95

* Tue Mar 01 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.5-1
- Plasma 5.5.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.4-1
- Plasma 5.5.4

* Thu Jan 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.3-1
- Plasma 5.5.3

* Thu Dec 31 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.5.2-1
- 5.5.2

* Fri Dec 18 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.1-1
- Plasma 5.5.1

* Thu Dec 03 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.0-1
- Plasma 5.5.0

* Wed Nov 25 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.95-1
- Plasma 5.4.95

* Thu Nov 05 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.3-1
- Plasma 5.4.3

* Mon Oct 19 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-2
- kcm_hotkeys: use qdbusviewer-qt5, Recommends: qt5-qdbusviewer (kde#329094)

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

* Tue Jun 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.3.1-2
- re-add versioned Conflicts: kde-workspace (gives hints on upgrade path for older releases)
- improve Obsoletes khotkeys-libs
- improve %%find_lang usage
- -devel: move dbus-1 xml interface here
- .spec cosmetics

* Tue May 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma 5.3.1

* Mon May 11 2015 Nils Philippsen <nils@redhat.com> - 5.3.0-2
- don't conflict kde-workspace anymore
- obsolete khotkeys-libs

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

* Mon Jan 12 2015 Daniel Vrátil <dvraitl@redhat.com> - 5.1.95-1.beta
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

* Thu Jul 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140514gite1c386a
- Intial snapshot
