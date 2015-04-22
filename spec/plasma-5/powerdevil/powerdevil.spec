Name:           powerdevil
Version:        5.2.95
Release:        1%{?dist}
Summary:        Manages the power consumption settings of a Plasma Shell

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/powerdevil

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

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

Requires:       kf5-filesystem

%description
Powerdevil is an utility for powermanagement. It consists
of a daemon (a KDED module) and a KCModule for its configuration.

%prep
%setup -q -n %{name}-%{version}

%patch0 -p1 -b .enable-upower

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang powerdevil5 --with-qt --with-kde --all-name

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
* Wed Apr 22 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-1
- Plasma 5.2.95

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Fri Feb 06 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-2
- add upstream patch for BKO#337674

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Wed Jan 14 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Mon Jan 05 2015 Jan Grulich <jgrulich@redhat.com> - 5.1.1-2
- Better URL
  Used make install instead make_install macro
  Fixed search for localization
  Dropped unused BR: chrpath

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

* Wed May 21 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-3.20140515gitf7a2bbe
- Fix missing BR
- Add a patch to fix UPower support

* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140515gitf7a2bbe
- Intial snapshot
