%global         base_name   breeze

%global         build_kde4  1

Name:           plasma-breeze
Version:        5.1.0.1
Release:        1%{?dist}
Summary:        Artwork, styles and assets for the Breeze visual style for the Plasma Desktop

License:        GPLv2+
URL:            http://www.kde.org

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

# kde4breeze
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kconfig-devel

# kstyle
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-frameworkintegration-devel
BuildRequires:  kf5-kwindowsystem-devel

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


%if 0%{?build_kde4:1}
%package        kde4
Summary:        KDE 4 version of Plasma 5 artwork, style and assets
BuildRequires:  kdelibs4-devel
BuildRequires:  libxcb-devel
Requires:       %{name}-common = %{version}-%{release}
%description    kde4
%{summary}.
%endif

%prep
%setup -q -n %{base_name}-%{version}

%build
mkdir -p %{_target_platform}
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
%make_install -C %{_target_platform}
%find_lang breeze --with-qt --all-name
%if 0%{?build_kde4:1}
%make_install -C %{_target_platform}_kde4
%endif

%files
%doc cursors/src/README COPYING
%{_datadir}/kwin/decorations/kwin4_decoration_qml_breeze
%{_kf5_datadir}/kservices5/kwin/kwin4_decoration_qml_breeze.desktop
%{_qt5_prefix}/qml/QtQuick/Controls/Styles/Breeze
%{_kf5_libdir}/kconf_update_bin/kde4breeze
%{_kf5_datadir}/kconf_update/kde4breeze.upd
%{_kf5_qtplugindir}/kstyle_breeze_config.so
%{_kf5_qtplugindir}/styles/breeze.so
%{_datadir}/kstyle/themes/breeze.themerc

%files common -f breeze.lang
%{_datadir}/color-schemes/*.colors
%{_datadir}/icons/breeze_cursors
%{_datadir}/icons/breeze
%{_datadir}/icons/breeze-dark
%{_datadir}/QtCurve/Breeze.qtcurve
%{_datadir}/wallpapers/Next

%if 0%{?build_kde4:1}
%files kde4
%{_kde4_libdir}/kde4/plugins/styles/breeze.so
%{_kde4_libdir}/kde4/kstyle_breeze_config.so
%{_kde4_appsdir}/kstyle/themes/breeze.themerc
%endif

%changelog
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
