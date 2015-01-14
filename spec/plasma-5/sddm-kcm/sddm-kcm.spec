Name:           sddm-kcm
Summary:        KDE System Settings module to configure SDDM
Version:        5.1.95
Release:        1.beta%{?dist}

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/sddm-kcm

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

# Workaround KAuth bug (see https://git.reviewboard.kde.org/r/122029/)
sed -i "s/\/usr\/\/usr\//\/usr\//" %{buildroot}/%{_datadir}/dbus-1/system-services/org.kde.kcontrol.kcmsddm.service

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
* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta
