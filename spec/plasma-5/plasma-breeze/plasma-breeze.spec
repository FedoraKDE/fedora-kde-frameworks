%global         base_name   breeze

%global         build_kde4  1

Name:           plasma-breeze
Version:        5.2.2
Release:        1%{?dist}
Summary:        Artwork, styles and assets for the Breeze visual style for the Plasma Desktop

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/breeze

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{base_name}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:	kf5-kservice-devel

# kde4breeze
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kconfig-devel

# kstyle
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-frameworkintegration-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kdecoration-devel

BuildRequires:  libxcb-devel

BuildRequires:  gettext

Requires:       kf5-filesystem

Requires:       %{name}-common = %{version}-%{release}

%description
%{summary}.

%package        common
Summary:        Common files shared between KDE 4 and Plasma 5 versions of the Breeze style
BuildArch:      noarch
%description    common
%{summary}.

%package -n     breeze-icon-theme
Summary:        Breeze icon theme
BuildArch:      noarch
%description -n breeze-icon-theme
%{summary}.

%if 0%{?build_kde4:1}
%package -n     kde-style-breeze
Summary:        KDE 4 version of Plasma 5 artwork, style and assets
BuildRequires:  kdelibs4-devel
BuildRequires:  libxcb-devel
Requires:       %{name}-common = %{version}-%{release}
Obsoletes:      plasma-breeze-kde4 < 5.1.95
Provides:       plasma-breeze-kde4%{?_isa} = %{version}-%{release}
%description -n kde-style-breeze
%{summary}.
%endif


%prep
%autosetup -n %{base_name}-%{version} -p1


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%if 0%{?build_kde4:1}
mkdir -p %{_target_platform}_kde4
pushd %{_target_platform}_kde4
%{cmake_kde4} -DUSE_KDE4=TRUE ..
popd

make %{?_smp_mflags} -C %{_target_platform}_kde4
%endif


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang breeze --with-qt --all-name

%if 0%{?build_kde4:1}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}_kde4
%endif


%files
%doc cursors/Breeze/README COPYING COPYING-ICONS
%{_kf5_qtplugindir}/org.kde.kdecoration2/breezedecoration.so
%{_kf5_qtplugindir}/styles/breeze.so
%{_kf5_datadir}/kstyle/themes/breeze.themerc
%{_kf5_qtplugindir}/kstyle_breeze_config.so
%{_bindir}/breeze-settings5
%{_kf5_datadir}/kconf_update/kde4breeze.upd
%{_kf5_libdir}/kconf_update_bin/kde4breeze
%{_kf5_datadir}/kconf_update/gtkbreeze.upd
%{_kf5_libdir}/kconf_update_bin/gtkbreeze
%{_kf5_qmldir}/QtQuick/Controls/Styles/Breeze

%files common -f breeze.lang
%{_datadir}/color-schemes/*.colors
%{_datadir}/QtCurve/Breeze.qtcurve
%{_datadir}/wallpapers/Next

%post -n breeze-icon-theme
touch --no-create %{_datadir}/icons/{breeze_cursors,breeze,breeze-dark,Breeze_Snow} &> /dev/null || :

%posttrans -n breeze-icon-theme
gtk-update-icon-cache %{_datadir}/icons/{breeze_cursors,breeze,breeze-dark,Breeze_Snow} &> /dev/null || :

%postun -n breeze-icon-theme
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/{breeze_cursors,breeze,breeze-dark,Breeze_Snow} &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/{breeze_cursors,breeze,breeze-dark,Breeze_Snow} &> /dev/null || :
fi

%files -n breeze-icon-theme
%{_datadir}/icons/breeze_cursors
%{_datadir}/icons/breeze
%{_datadir}/icons/breeze-dark
%{_datadir}/icons/Breeze_Snow

%if 0%{?build_kde4:1}
%files -n kde-style-breeze
%{_kde4_libdir}/kde4/plugins/styles/breeze.so
%{_kde4_libdir}/kde4/kstyle_breeze_config.so
%{_kde4_appsdir}/kstyle/themes/breeze.themerc
%endif


%changelog
* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Tue Mar 10 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.2.1-3
- backport upstream fixes (mostly crashers)
- .spec cosmetics

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Mon Jan 05 2015 Jan Grulich <jgrulich@redhat.com> - 5.1.1-2
- better URL
  breeze-kde4 renamed to kde-style-breeze
  created breeze-icon-theme subpackage
  used make install instead of make_install macro

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

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140514git73a19ea
- Update to latest upstream

* Fri May 02 2014 Jan Grulich <jgrulich@redhat.com> 4.90.1-0.1.20140502git
- Initial version
