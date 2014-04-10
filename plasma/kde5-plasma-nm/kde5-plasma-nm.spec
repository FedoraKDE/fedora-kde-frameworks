%global         git_commit 2333fd4

Name:           kde5-plasma-nm
Version:        0.9.3.3
Release:        1%{?dist}
Summary:        Plasma Next applet written in QML for managing network connections
License:        LGPLv2+ and GPLv2+
URL:            https://projects.kde.org/projects/playground/network/plasma-nm
#Source0:        http://download.kde.org/unstable/plasma-nm//plasma-nm-%{version}.tar.xz
Source0:        kde5-plasma-nm-%{version}-git%{git_commit}.tar.xz

# Add plasma-nm to default systray if needed, for upgraders...
Source10: 01-fedora-plasma-nm.js

## upstream patches
#Patch0:   openconnect.patch
#Patch1:   item-text.patch

BuildRequires:  gettext

BuildRequires:  kde5-filesystem
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-attica-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-kinit-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kdesignerplugin-devel
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kemoticons-devel
BuildRequires:  kf5-kitemmodels-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kunitconversion-devel
BuildRequires:  kf5-kde4support-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-umbrella
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  libmm-qt5-devel >= 1.0.0
BuildRequires:  libnm-qt5-devel >= 0.9.8.1
BuildRequires:  pkgconfig(NetworkManager) >= 0.9.8
BuildRequires:  pkgconfig(ModemManager) >= 1.0.0
BuildRequires:  pkgconfig(libnm-glib) pkgconfig(libnm-util)
%if 0%{?fedora} || 0%{?epel}
BuildRequires:  pkgconfig(openconnect) >= 4.00
%endif

Requires:  NetworkManager >= 0.9.8
Requires:  libnm-qt5 >= 0.9.8.1

Obsoletes: kde-plasma-networkmanagement < 1:0.9.1.0
Obsoletes: kde-plasma-networkmanagement-libs < 1:0.9.1.0
Provides:  kde-plasma-networkmanagement = 1:%{version}-%{release}
Provides:  kde-plasma-networkmanagement-libs = 1:%{version}-%{release}

%description
Plasma applet and editor for managing your network connections in KDE 4 using
the default NetworkManager service.

# Required for properly working GMS/CDMA connections
%package mobile
Summary: Mobile support for %{name}
Requires:  ModemManager
Requires:  mobile-broadband-provider-info
Requires:  libmm-qt5 >= 1.0.0
Obsoletes: kde-plasma-networkmanagement-mobile < 1:0.9.1.0
Provides:  kde-plasma-networkmanagement-mobile = 1:%{version}-%{release}
%description mobile
%{summary}.

%if 0%{?fedora} || 0%{?epel}
%package openvpn
Summary:        OpenVPN support for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-openvpn
Obsoletes:      kde-plasma-networkmanagement-openvpn < 1:0.9.1.0
Provides:       kde-plasma-networkmanagement-openvpn = 1:%{version}-%{release}
%description openvpn
%{summary}.

%package vpnc
Summary:        Vpnc support for %{name} 
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-vpnc
Obsoletes:      kde-plasma-networkmanagement-vpnc < 1:0.9.1.0
Provides:       kde-plasma-networkmanagement-vpnc = 1:%{version}-%{release}
%description vpnc
%{summary}.

%package openconnect
Summary:        OpenConnect support for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-openconnect
Obsoletes:      kde-plasma-networkmanagement-openconnect < 1:0.9.1.0
Provides:       kde-plasma-networkmanagement-openconnect = 1:%{version}-%{release}
%description openconnect
%{summary}.

%package openswan
Summary:        Openswan support for %{name} 
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-openswan
%description openswan
%{summary}.

%package strongswan
Summary:        Strongswan support for %{name} 
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       strongswan
%description strongswan
%{summary}.

%package l2tp
Summary:        L2TP support for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-l2tp
%description l2tp
%{summary}.

%package pptp
Summary:        PPTP support for %{name} 
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-pptp
Obsoletes:      kde-plasma-networkmanagement-pptp < 1:0.9.1.0
Provides:       kde-plasma-networkmanagement-pptp = 1:%{version}-%{release}
%description pptp
%{summary}.
%endif

%prep
%setup -qn plasma-nm-%{version}

#%patch0 -p1 -b .openconnect
#%patch1 -p1 -b .item-text

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}

#%find_lang plasma_applet_org.kde.networkmanagement
#%find_lang plasmanetworkmanagement-kded
#%find_lang kde-nm-connection-editor
#%find_lang libplasmanetworkmanagement-editor
#%find_lang plasmanetworkmanagement_vpncui
#%find_lang plasmanetworkmanagement_openvpnui
#%find_lang plasmanetworkmanagement_openconnectui
#%find_lang plasmanetworkmanagement_openswanui
#%find_lang plasmanetworkmanagement_strongswanui
#%find_lang plasmanetworkmanagement_l2tpui
#%find_lang plasmanetworkmanagement_pptpui

# migrate to nm plasmoid
install -m644 -p -D %{SOURCE10} %{buildroot}%{_kde5_appsdir}/plasma/updates/01-fedora-plasma-nm.js

%post
touch --no-create %{_kde5_iconsdir}/oxygen &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kde5_iconsdir}/oxygen &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde5_iconsdir}/oxygen &> /dev/null || :
gtk-update-icon-cache %{_kde5_iconsdir}/oxygen &> /dev/null || :
fi

#%files -f plasma_applet_org.kde.networkmanagement.lang -f plasmanetworkmanagement-kded.lang -f kde-nm-connection-editor.lang -f libplasmanetworkmanagement-editor.lang
%files
%defattr(-,root,root,-)
# kde-nm-connection-editor
%{_kde5_bindir}/kde-nm-connection-editor
%{_kde5_libdir}/libplasmanetworkmanagement-editor.so
%{_kde5_datadir}/kde-nm-connection-editor/kde-nm-connection-editorui.rc
%{_kde5_datadir}/applications/kde-nm-connection-editor.desktop
# plasma-nm applet
%{_kde5_libdir}/qml/org/kde/plasma/networkmanagement/libplasmanetworkmanagementplugins.so
%{_kde5_libdir}/qml/org/kde/plasma/networkmanagement/qmldir
%dir %{_kde5_datadir}/plasma/plasmoids/org.kde.plasma.networkmanagement/
%{_kde5_datadir}/plasma/plasmoids/org.kde.plasma.networkmanagement/contents
%{_kde5_datadir}/plasma/plasmoids/org.kde.plasma.networkmanagement/metadata.desktop
%{_kde5_datadir}/kde5/services/plasma-applet-org.kde.plasma.networkmanagement.desktop
%{_kde5_libdir}/plugins/kf5/plugins/designer/libplasmanetworkmanagementwidgets.so
#%{_kde5_appsdir}/desktoptheme/default/icons/plasma-networkmanagement2.svgz
%{_kde5_iconsdir}/oxygen/*/*/*
%{_kde5_appsdir}/plasma/updates/*.js
# plasma-nm notifications
#%{_kde5_datadir}/kde5/services/networkmanagement_notifications.desktop
#%{_kde5_libdir}/plugins/kf5/networkmanagement_notifications.so
%{_kde5_datadir}/networkmanagement/networkmanagement.notifyrc
# plasma-nm kded
%{_kde5_libdir}/plugins/kf5/kded_networkmanagement.so
%{_kde5_datadir}/kde5/services/kded/networkmanagement.desktop
# plasma-nm other
%{_kde5_libdir}/libplasmanetworkmanagement-internal.so
%{_kde5_datadir}/kde5/servicetypes/plasma-networkmanagement-vpnuiplugin.desktop


%files mobile

%if 0%{?fedora} || 0%{?epel}
#%files openvpn -f plasmanetworkmanagement_openvpnui.lang
%files openvpn
%{_kde5_libdir}/plugins/kf5/plasmanetworkmanagement/vpnuiplugin/libplasmanetworkmanagement_openvpnui.so
%{_kde5_datadir}/kde5/services/plasmanetworkmanagement_openvpnui.desktop

#%files vpnc -f plasmanetworkmanagement_vpncui.lang
%files vpnc
%{_kde5_libdir}/plugins/kf5/plasmanetworkmanagement/vpnuiplugin/libplasmanetworkmanagement_vpncui.so
%{_kde5_datadir}/kde5/services/plasmanetworkmanagement_vpncui.desktop

#%files openconnect -f plasmanetworkmanagement_openconnectui.lang
%files openconnect
%{_kde5_libdir}/plugins/kf5/plasmanetworkmanagement/vpnuiplugin/libplasmanetworkmanagement_openconnectui.so
%{_kde5_datadir}/kde5/services/plasmanetworkmanagement_openconnectui.desktop

#%files openswan -f plasmanetworkmanagement_openswanui.lang
%files openswan
%{_kde5_libdir}/plugins/kf5/plasmanetworkmanagement/vpnuiplugin/libplasmanetworkmanagement_openswanui.so
%{_kde5_datadir}/kde5/services/plasmanetworkmanagement_openswanui.desktop

#%files strongswan -f plasmanetworkmanagement_strongswanui.lang
%files strongswan
%{_kde5_libdir}/plugins/kf5/plasmanetworkmanagement/vpnuiplugin/libplasmanetworkmanagement_strongswanui.so
%{_kde5_datadir}/kde5/services/plasmanetworkmanagement_strongswanui.desktop

#%files l2tp -f plasmanetworkmanagement_l2tpui.lang
%files l2tp
%{_kde5_libdir}/plugins/kf5/plasmanetworkmanagement/vpnuiplugin/libplasmanetworkmanagement_l2tpui.so
%{_kde5_datadir}/kde5/services/plasmanetworkmanagement_l2tpui.desktop

#%files pptp -f plasmanetworkmanagement_pptpui.lang
%files pptp
%{_kde5_libdir}/plugins/kf5/plasmanetworkmanagement/vpnuiplugin/libplasmanetworkmanagement_pptpui.so
%{_kde5_datadir}/kde5/services/plasmanetworkmanagement_pptpui.desktop
%endif

%changelog
* Thu Apr 03 2014 Daniel Vrátil <dvratil@redhat.com> - 0.9.3.3-1
- fork into kde5-plasma-nm

* Mon Mar 10 2014 Jan Grulich <jgrulich@redhat.com> - 0.9.3.3-3
- fix connection status for mobile connections

* Fri Mar 07 2014 Jan Grulich <jgrulich@redhat.com> - 0.9.3.3-2
- fix build with openconnect

* Wed Feb 26 2014 Jan Grulich <jgrulich@redhat.com> - 0.9.3.3-1
- Update to 0.9.3.3

* Thu Feb 13 2014 Rex Dieter <rdieter@fedoraproject.org> - 0.9.3.2-4
- add icon scriptlets

* Fri Jan 03 2014 Jan Grulich <jgrulich@redhat.com> - 0.9.3.2-3
- More upstream fixes

* Thu Jan 02 2014 Jan Grulich <jgrulich@redhat.com> - 0.9.3.2-2
- Pickup some upstream fixes

* Thu Nov 21 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.2-1
- Update to 0.9.3.2

* Wed Oct 30 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.1-6
- add some upstream fixes and changes

* Wed Oct 23 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.1-5
- pickup some upstream fixes

* Mon Oct 14 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.1-4
- Update to 0.9.3.1

* Mon Oct 14 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.1-3.20131009git82dab6e
- Fix obsoletes

* Thu Oct 10 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.1-2.20131009git82dab6e
- Add obsoletes for kde-plasma-networkmanagement
- Add rename script

* Wed Oct 9 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.1-1.20131009git82dab6e
- Update to current git snapshot

* Tue Oct 1 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.0-7
- Make ModemManager as runtime dependency installed with -mobile subpkg
- Resolves #1013838

* Wed Sep 11 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.0-6
- Update to first official release (0.9.3.0)

* Tue Aug 20 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.0-5.20130812git707b2b
- add javascript to automatically add plasma-nm to the systray

* Mon Aug 12 2013 Lukas Tinkl <ltinkl@redhat.com> - 0.9.3.0-4.20130812git707b2b
- Update to current git snapshots
- simplified applet based on usability study from Akademy

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3.0-3.20130613git6a4c385
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.0-2.20130613git6a4c385
- Update to the current git snapshot
- Add Openswan, Openconnect, L2TP, PPTP VPN plugins

* Tue Jun 4 2013 Jan Grulich <jgrulich@redhat.com> - 0.9.3.0-1.20130604git649e5f4
- Initial package
- Based on git snapshot 649e5f4b3e5b4f30df19aa0f908234355912eea7
