%define base_name oxygen

Name:           plasma-%{base_name}
Version:        5.0.2
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

%description
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

%install
%make_install -C %{_target_platform}
%find_lang oxygen5 --with-qt --all-name

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f oxygen5.lang
%doc COPYING
%{_bindir}/oxygen-demo5
%{_bindir}/oxygen-settings5
%{_libdir}/*.so.*
%{_kf5_qtplugindir}/kstyle_oxygen_config.so
%{_kf5_qtplugindir}/kwin/kdecorations/config/kwin_oxygen_config.so
%{_kf5_qtplugindir}/kwin/kdecorations/kwin3_oxygen.so
%{_kf5_qtplugindir}/styles/oxygen.so
%{_datadir}/kstyle/themes/oxygen.themerc
%{_datadir}/icons/*
%{_datadir}/sounds/*


%files devel
%{_libdir}/*.so

%changelog
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
