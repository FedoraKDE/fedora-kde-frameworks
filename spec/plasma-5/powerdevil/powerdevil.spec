Name:           powerdevil
Version:        5.0.0
Release:        1%{?dist}
Summary:        Manages the power consumption settings of a Plasma Shell

License:        GPLv2+
URL:            http://www.kde.org
Source0:        http://download.kde.org/stable/plasma/%{version}/%{name}-%{version}.tar.xz

Patch0:         powerdevil-enable-upower.patch

BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  libXrandr-devel
BuildRequires:  systemd-devel

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kidletime-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-knotifyconfig-devel
BuildRequires:  kf5-kdelibs4support-devel

BuildRequires:  plasma-workspace-devel

BuildRequires:  chrpath

Requires:       kf5-filesystem

Obsoletes:      kde-workspace < 5.0.0-1

%description
%{summary}.

%prep
%setup -q

%patch0 -p1 -b .enable-upower

%build

sed -e "s/PO_FILES //" -i po/*/CMakeLists.txt

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}
%find_lang powerdevil5 --with-qt --all-name

# FIXME: This is result of broken Cmake Config files from kde5-plasma-workspace-devel
#chrpath --delete %{buildroot}/%{_kde5_plugindir}/kded_powerdevil.so
#chrpath --delete %{buildroot}/%{_kde5_plugindir}/kcm_powerdevilglobalconfig.so
#chrpath --delete %{buildroot}/%{_kde5_plugindir}/kcm_powerdevilprofilesconfig.so
#chrpath --delete %{buildroot}/%{_kde5_libdir}/libpowerdevilcore.so.1.1.0
#chrpath --delete %{buildroot}/%{_kde5_libdir}/libpowerdevilconfigcommonprivate.so.%{version}

# Don't bother with -devel
rm %{buildroot}/%{_libdir}/libpowerdevil{configcommonprivate,core,ui}.so

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f powerdevil5.lang
%doc COPYING
%config %{_sysconfdir}/dbus-1/system.d/org.kde.powerdevil.backlighthelper.conf
%{_libdir}/libpowerdevilconfigcommonprivate.so.*
%{_libdir}/libpowerdevilcore.so.*
%{_libdir}/libpowerdevilui.so.*
%{_kf5_qtplugindir}/*.so
%{_kf5_libexecdir}/kauth/backlighthelper
%{_datadir}/dbus-1/system-services/org.kde.powerdevil.backlighthelper.service
%{_kf5_datadir}/knotifications5/powerdevil.notifyrc
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservices5/kded/*.desktop
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_datadir}/polkit-1/actions/org.kde.powerdevil.backlighthelper.policy
%{_datadir}/doc/HTML/en/kcontrol/powerdevil


%changelog
* Thu Jul 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Wed May 21 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-3.20140515gitf7a2bbe
- Fix missing BR
- Add a patch to fix UPower support

* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140515gitf7a2bbe
- Intial snapshot
