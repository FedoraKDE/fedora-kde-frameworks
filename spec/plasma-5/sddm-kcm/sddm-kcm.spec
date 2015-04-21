Name:           sddm-kcm
Version:        5.2.2
Release:        1%{?dist}
License:        GPLv2+
Summary:        SDDM KDE configuration module

Url:            https://projects.kde.org/projects/kde/workspace/sddm-kcm

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz


BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-qtdeclarative-devel

BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kio-devel

BuildRequires:  libX11-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-image-devel

# kinda makes sense, right?
Requires:       sddm


%description
This is a System Settings configuration module for configuring the
SDDM Display Manager

%prep
%setup -q -n %{name}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang kcmsddm5_qt --with-qt --all-name

%files -f kcmsddm5_qt.lang
%doc COPYING README
%{_kf5_qtplugindir}/kcm_sddm.so
%{_kf5_datadir}/kservices5/kcm_sddm.desktop
%{_kf5_datadir}/sddm-kcm
%{_kf5_libexecdir}/kauth/kcmsddm_authhelper
%config %{_sysconfdir}/dbus-1/system.d/org.kde.kcontrol.kcmsddm.conf
%{_datadir}/dbus-1/system-services/org.kde.kcontrol.kcmsddm.service
%{_datadir}/polkit-1/actions/org.kde.kcontrol.kcmsddm.policy



%changelog
* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Wed Jan 21 2015 Martin Briza <mbriza@redhat.com> - 0-0.5.20140114gitfe615f21
- Applied patch by Vincent Damewood to fix configuration file incompatibility (thanks!)
- Fixed theme listing
- Resolves: #1172276 #1173825

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.4.20140114gitfe615f21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.3.20140114gitfe615f21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 14 2014 Martin Briza <mbriza@redhat.com> - 0-0.2.20140114gitfe615f21
- Update to the latest upstream commit (fixes theme list)

* Thu Nov 14 2013 Martin Briza <mbriza@redhat.com> - 0-0.1.20131114gitafdda33c
- Initial import
