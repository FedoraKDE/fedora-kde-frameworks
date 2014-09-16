Name:           plasma-desktop
Version:        5.0.2
Release:        1%{?dist}
Summary:        Plasma 5 Desktop

License:        GPLv2+
URL:            http://www.kde.org

Source0:        http://download.kde.org/stable/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  libusb-devel
BuildRequires:  fontconfig-devel
BuildRequires:  libX11-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-renderutil-devel
BuildRequires:  xcb-util-devel
BuildRequires:  libxkbcommon-devel

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  phonon-qt5-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-knewstuff-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-knotifyconfig-devel
BuildRequires:  kf5-kdesu-devel
BuildRequires:  kf5-attica-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-krunner-devel
BuildRequires:  kf5-ksysguard-devel

BuildRequires:  plasma-workspace-devel
BuildRequires:  kwin-devel

# Optional
BuildRequires:  kf5-kactivities-devel
BuildRequires:  libcanberra-devel

BuildRequires:  chrpath

Requires:       plasma-workspace
Requires:       kf5-filesystem


Obsoletes:      kde-workspace < 5.0.0-1

%description
%{summary}.

%package        doc
Summary:        Documentation and user manuals for %{name}

%description    doc
Documentation and user manuals for %{name}.


%prep
%setup -q

%build

sed -e "s/PO_FILES //" -i po/*/CMakeLists.txt

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}
%find_lang plasmadesktop5 --with-qt --all-name

# No -devel
rm %{buildroot}/%{_libdir}/libkfontinst{,ui}.so

# KDM is dead
rm -r %{buildroot}/%{_datadir}/kdm

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f plasmadesktop5.lang
%{_bindir}/kapplymousetheme
%{_bindir}/kaccess
%{_bindir}/kfontinst
%{_bindir}/kfontview
%{_bindir}/krdb
%{_bindir}/knetattach
%{_kf5_libexecdir}/kauth/kcmdatetimehelper
%{_kf5_libexecdir}/kauth/fontinst
%{_kf5_libexecdir}/kauth/fontinst_helper
%{_kf5_libexecdir}/kauth/fontinst_x11
%{_libexecdir}/kfontprint
%{_qt5_prefix}/qml/org/kde/plasma/private
%{_kf5_libdir}/libkdeinit5_kaccess.so
%{_kf5_libdir}/kconf_update_bin/*
%{_libdir}/libkfontinst.so.*
%{_libdir}/libkfontinstui.so.*
#%{_libdir}/attica_kde.so
%{_kf5_qtplugindir}/*.so
%{_datadir}/plasma/*
%{_datadir}/kcminput
%{_datadir}/color-schemes
%{_datadir}/kconf_update/*
%{_datadir}/kthememanager
%{_datadir}/kdisplay
%{_datadir}/kcontrol
%{_datadir}/kcmkeys
%{_datadir}/kcm_componentchooser
#%{_datadir}/kcmlocale
%{_datadir}/kcm_phonon
%{_datadir}/kfontinst
%{_datadir}/kfontview
%{_datadir}/kcmkeyboard
%{_datadir}/ksmserver
%{_datadir}/konqsidebartng/virtual_folders/services/fonts.desktop
%config %{_sysconfdir}/dbus-1/system.d/*.conf
%config %{_sysconfdir}/xdg/*.knsrc
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservices5/ServiceMenus/installfont.desktop
%{_kf5_datadir}/kservices5/fonts.protocol
%{_kf5_datadir}/kservices5/kded/*.desktop
%{_kf5_datadir}/knotifications5/*.notifyrc
%{_kf5_datadir}/config.kcfg/*
%{_datadir}/icons/*/*/*/*
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/polkit-1/actions/*.policy

%files doc
# %doc COPYING COPYING.DOC COPYING.LIB README README.pam
%{_datadir}/doc/HTML/en/*


%changelog
* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.2-1
- Plasma 5.0.2

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Thu Jul 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1.20140515git532fc47
- Initial version of kde5-plasma-desktop
