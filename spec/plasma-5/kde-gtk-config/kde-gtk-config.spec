Name:           kde-gtk-config
Summary:        Configure the appearance of GTK apps in KDE
Version:        5.3.95
Release:        1%{?dist}

# KDE e.V. may determine that future GPL versions are accepted
# KDE e.V. may determine that future LGPL versions are accepted
License:        (GPLv2 or GPLv3) and (LGPLv2 or LGPLv3)
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
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-knewstuff-devel
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kcmutils-devel

BuildRequires:  gtk3-devel
BuildRequires:  gtk2-devel

# need kcmshell5 from kde-cli-tools
Requires:       kde-cli-tools

%description
This is a System Settings configuration module for configuring the
appearance of GTK apps in KDE.

%prep
%setup -q -n kde-gtk-config-%{version}

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang kcmgtk5_qt --with-qt --all-name


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f kcmgtk5_qt.lang
%doc ChangeLog COPYING COPYING.LIB
%{_kf5_qtplugindir}/kcm_kdegtkconfig.so
%{_sysconfdir}/xdg/*.knsrc
%{_kf5_datadir}/kservices5/kde-gtk-config.desktop
%{_libexecdir}/reload_gtk_apps
%{_libexecdir}/gtk_preview
%{_libexecdir}/gtk3_preview
%{_datadir}/kcm-gtk-module/
%{_datadir}/icons/hicolor/*/apps/kde-gtk-config.*


%changelog
* Thu Aug 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-1
- Plasma 5.3.95

* Thu Jun 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.2-1
- Plasma 5.3.2

* Wed Jun 17 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-3
- BR: kf5-kiconthemes-devel kf5-kio-devel

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma 5.3.1

* Fri May 01 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-1
- 5.3.0

* Tue Jan 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-2
- fix license
- remove Obsoletes/Provides kcm-gtk
- remove Requires xsettings-kde

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta
