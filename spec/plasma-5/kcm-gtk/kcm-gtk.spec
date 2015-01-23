Name:           kcm-gtk
Summary:        Configure the appearance of GTK apps in KDE 
Version:        5.2.0
Release:        1%{?dist}

License:        GPLv2+ and LGPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/kde-gtk-config

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/kde-gtk-config-%{version}.tar.xz


BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-knewstuff-devel
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kcmutils-devel

BuildRequires:  gtk3-devel
BuildRequires:  gtk2-devel

# need kcmshell5 from kde-cli-tools
Requires:       kde-cli-tools
# not *required*, but very nice.  allows support for instant changes, gtk3.
Requires:       xsettings-kde

%description
This is a System Settings configuration module for configuring the
appearance of GTK apps in KDE.

%prep
%setup -q -n kde-gtk-config-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang kcmgtk5_qt --with-qt --all-name


%files -f kcmgtk5_qt.lang
%doc ChangeLog COPYING COPYING.LIB
%{_kf5_qtplugindir}/kcm_kdegtkconfig.so
%config %{_sysconfdir}/xdg/*.knsrc
%{_kf5_datadir}/kservices5/kde-gtk-config.desktop
%{_libexecdir}/reload_gtk_apps
%{_libexecdir}/gtk_preview
%{_libexecdir}/gtk3_preview
%{_datadir}/kcm-gtk-module/preview.ui
%{_datadir}/icons/hicolor/*/apps/kde-gtk-config.*


%changelog
* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Rex Dieter <rdieter@fedoraproject.org> 0.5.3-14
- Requires: xsettings-kde

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 14 2012 Rex Dieter <rdieter@fedoraproject.org>
- 0.5.3-10
- update kcm_category patch
- kubuntu_01_xsettings_kipc.patch
- drop old Obsoletes: gtk-qt-engine

* Tue Jan 17 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.5.3-9
- drop gtk3 patch again, the new plan is to handle this through xsettings-kde

* Fri Jan 06 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.5.3-8
- add support for GTK+ 3 (backported from upstream bzr gtk3 branch)
- drop ancient Fedora < 13 env_script conditional, now always in kde-settings

* Mon Mar 14 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.5.3-7
- drop cursortheme patch, now set automatically by xsettings-kde (#591746)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.5.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 08 2010 Rex Dieter <rdieter@fedoraproject.org> 0.5.3-5
- kcm-gtk : "GTK+ Appearance" in systemsettings->lost and found (#628381)
- Requires: kdebase-runtime

* Wed Jul  7 2010 Ville Skyttä <ville.skytta@iki.fi> 0.5.3-4
- Apply modified upstream patch to add cursor theme support (#600976).

* Fri Dec 25 2009 Rex Dieter <rdieter@fedoraproject.org> 0.5.3-3
- GTK2_RC_FILES handling moved to kde-settings (#547700)

* Sun Dec 20 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.5.3-2
- fix missing umlauts and sharp s in the German translation

* Fri Oct 30 2009 Rex Dieter <rdieter@fedoraproject.org> 0.5.3-1
- kcm-gtk-0.5.3
- .gtkrc-2.0-kde4 doesn't get used (#531788)

* Thu Oct 22 2009 Rex Dieter <rdieter@fedoraproject.org> 0.5.1-2
- Requires: kde4-macros(api)...

* Thu Oct 22 2009 Rex Dieter <rdieter@fedoraproject.org> 0.5.1-1
- kcm-gtk-0.5.1 (first try)

