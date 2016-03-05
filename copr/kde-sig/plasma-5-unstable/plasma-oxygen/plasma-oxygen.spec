%global         base_name oxygen

Name:           plasma-%{base_name}
Version: 5.5.95
Release: 1%{?dist}
Summary:        Plasma and Qt widget style and window decorations for Plasma 5 and KDE 4

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/oxygen

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{base_name}-%{version}.tar.xz

# Qt 4 dependencies
BuildRequires:  kdelibs-devel
BuildRequires:  libxcb-devel
# Don't build the KWin style, we don't need that
#BuildRequires: kde-workspace-devel

# Qt 5
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

# KF5
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-frameworkintegration-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kcmutils-devel

BuildRequires:  kdecoration-devel

Requires:       kf5-filesystem

Requires:       qt4-style-oxygen = %{version}-%{release}
Requires:       qt5-style-oxygen = %{version}-%{release}
Requires:       oxygen-cursor-themes = %{version}-%{release}
Requires:       oxygen-sound-theme = %{version}-%{release}

# kwin-oxygen was removed in 5.1.95
Obsoletes:	kwin-oxygen < 5.1.95-1

%description
%{summary}.

%package -n     qt4-style-oxygen
Summary:        Oxygen widget style for Qt 4
Provides:       kde-style-oxygen%{?_isa} = %{version}-%{release}
# When this was created
Obsoletes:      kde-style-oxygen < 5.1.1-2
Obsoletes:      plasma-oxygen-kde4 < 5.1.1-2
%description -n qt4-style-oxygen
%{summary}.

%package -n     qt5-style-oxygen
Summary:        Oxygen widget style for Qt 5
Obsoletes:      plasma-oxygen < 5.1.1-2
%description -n qt5-style-oxygen
%{summary}.

%package -n     oxygen-cursor-themes
Summary:        Oxygen cursor themes
BuildArch:      noarch
Obsoletes:      plasma-oxygen-common < 5.1.1-2
%description -n oxygen-cursor-themes
%{summary}.

%package -n     oxygen-sound-theme
Summary:        Sounds for Oxygen theme
BuildArch:      noarch
Obsoletes:      plasma-oxygen-common < 5.1.1-2
%description -n oxygen-sound-theme
%{summary}.

%prep
%setup -q -n %{base_name}-%{version}

%build
%define qt5_target_platform %{_target_platform}-qt5
%define qt4_target_platform %{_target_platform}-qt4

# Build for Qt 4
mkdir -p %{qt4_target_platform}
pushd %{qt4_target_platform}
%{cmake_kde4} .. -DOXYGEN_USE_KDE4:BOOL=ON
popd

make %{?_smp_mflags} -C %{qt4_target_platform}

# Build for Qt 5
mkdir -p %{qt5_target_platform}
pushd %{qt5_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{qt5_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{qt4_target_platform}
make install/fast DESTDIR=%{buildroot} -C %{qt5_target_platform}

%find_lang oxygen --with-qt --all-name

# Don't both with -devel subpackages, there are no headers anyway
rm %{buildroot}/%{_libdir}/liboxygenstyle5.so
rm %{buildroot}/%{_libdir}/liboxygenstyleconfig5.so
rm %{buildroot}/%{_kde4_libdir}/liboxygenstyle.so
rm %{buildroot}/%{_kde4_libdir}/liboxygenstyleconfig.so

%post -n    qt4-style-oxygen -p /sbin/ldconfig
%postun -n  qt4-style-oxygen -p /sbin/ldconfig

%files
# Empty

%files -n   qt4-style-oxygen
%{_kde4_libdir}/liboxygenstyle.so.*
%{_kde4_libdir}/liboxygenstyleconfig.so.*
%{_kde4_libdir}/kde4/kstyle_oxygen_config.so
%{_kde4_libdir}/kde4/plugins/styles/oxygen.so
%{_kde4_appsdir}/kstyle/themes/oxygen.themerc
%{_kde4_bindir}/oxygen-demo

%post -n    qt5-style-oxygen -p /sbin/ldconfig
%postun -n  qt5-style-oxygen -p /sbin/ldconfig

%files -n   qt5-style-oxygen -f oxygen.lang
%{_bindir}/oxygen-demo5
%{_bindir}/oxygen-settings5
%{_libdir}/liboxygenstyle5.so.*
%{_libdir}/liboxygenstyleconfig5.so.*
%{_kf5_qtplugindir}/styles/oxygen.so
%{_kf5_qtplugindir}/kstyle_oxygen_config.so
%{_kf5_qtplugindir}/org.kde.kdecoration2/oxygendecoration.so
%{_kf5_datadir}/kservices5/oxygenstyleconfig.desktop
%{_kf5_datadir}/kservices5/oxygendecorationconfig.desktop
%{_kf5_datadir}/kstyle/themes/oxygen.themerc
%{_kf5_datadir}/plasma/look-and-feel/org.kde.oxygen/

%post -n    oxygen-cursor-themes
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun -n  oxygen-cursor-themes
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans -n oxygen-cursor-themes
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -n   oxygen-cursor-themes
%{_datadir}/icons/*

%files -n   oxygen-sound-theme
%{_datadir}/sounds/*


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

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

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

* Tue Jan 27 2015 Daniel Vrátil <dvratil2redhat.com> - 5.2.0-2
- fix Requires: kwin-devel (unversioned)

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1
- Plasma 5.1.95 Beta
- removed kwin-oxygen subpackage, as Oxygen does not provide KDecoration1-based windecos as of 5.1.95

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- Plasma 5.1.2

* Wed Nov 19 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.1.1-9
- Move kstyle_oxygen_config.so from kwin-oxygen to qt5-style-oxygen

* Wed Nov 19 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-8
- Remove Conflicts kde-style-oxygen from kwin-oxygen
- Remove Requires themes from qt{4,5}-style-oxygen
- Fixed scriptlets

* Thu Nov 13 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-7
- Fix Obsoletes issue when updating

* Wed Nov 12 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-2
- change subpackages, merge with plasma-oxygen-kde4

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

* Thu Jul 24 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-2
- Does not conflict with kde-style-oxygen 4

* Thu Jul 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140515git9651288
- Intial snapshot
