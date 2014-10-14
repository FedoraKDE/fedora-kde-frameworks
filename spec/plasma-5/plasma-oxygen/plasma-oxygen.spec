%global base_name oxygen
%global build_kde4 1

Name:           plasma-%{base_name}
Version:        5.1.0.1
Release:        1%{?dist}
Summary:        Plasma 5 and KDE default style and look

License:        GPLv2+
URL:            http://www.kde.org
Source0:        http://download.kde.org/stable/plasma/%{version}/%{base_name}-%{version}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-frameworkintegration-devel
BuildRequires:  kf5-kwindowsystem-devel

BuildRequires:  kwin-devel

Requires:       kf5-filesystem

Requires:       %{name}-common = %{version}-%{release}

%description
%{summary}.

%if 0%{?build_kde4:1}
%package        kde4
Summary:        KDE 4 version of Oxygen style for Plasma 5
BuildRequires:  kdelibs4-devel
#BuildRequires:  kdeworkspace-devel
BuildRequires:  libxcb-devel
Requires:       %{name}-common = %{version}-%{release}
%description    kde4
%{summary}.
%endif

%package        common
Summary:        Common date shared between Plasma 5 and KDE 4 versions of the Oxygen style
BuildArch:      noarch
%description    common
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

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
%find_lang oxygen5 --with-qt --all-name

%if 0%{?build_kde4:1}
%make_install -C %{_target_platform}_kde4
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f oxygen5.lang
%doc COPYING
%{_bindir}/oxygen-demo5
%{_bindir}/oxygen-settings5
%{_libdir}/liboxygenstyle5.so.*
%{_libdir}/liboxygenstyleconfig5.so.*
%{_kf5_qtplugindir}/kstyle_oxygen_config.so
%{_kf5_qtplugindir}/kwin/kdecorations/config/kwin_oxygen_config.so
%{_kf5_qtplugindir}/kwin/kdecorations/kwin3_oxygen.so
%{_kf5_qtplugindir}/styles/oxygen.so
%{_datadir}/kstyle/themes/oxygen.themerc
%{_kf5_datadir}/plasma/look-and-feel/org.kde.oxygen

%files common
%{_datadir}/icons/*
%{_datadir}/sounds/*

%if 0%{?build_kde4:1}
%files kde4
%{_kde4_libdir}/liboxygenstyle.so.*
%{_kde4_libdir}/liboxygenstyleconfig.so.*
%{_kde4_libdir}/kde4/kstyle_oxygen_config.so
%{_kde4_libdir}/kde4/plugins/styles/oxygen.so
%{_kde4_appsdir}/kstyle/themes/oxygen.themerc
%{_kde4_bindir}/oxygen-demo
%endif

%files devel
%{_libdir}/*.so
%if 0%{?build_kde4:1}
%{_kde4_libdir}/kde4/*.so
%endif

%changelog
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
