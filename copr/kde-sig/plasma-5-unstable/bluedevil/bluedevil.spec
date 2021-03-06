Name:           bluedevil
Summary:        Bluetooth stack for KDE
Version: 5.5.95
Release: 1%{?dist}

License:        GPLv2+
URL:            https://projects.kde.org/projects/extragear/base/bluedevil

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel

BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kio-devel
# 5.11 is when kf5-bluez-qt became Framework and changed API
BuildRequires:  kf5-bluez-qt-devel >= 5.11
BuildRequires:  kf5-kded-devel
BuildRequires:  kf5-kwindowsystem-devel

BuildRequires:  shared-mime-info

BuildRequires:  desktop-file-utils

Provides:       dbus-bluez-pin-helper

Obsoletes:      kbluetooth < 0.4.2-3
Obsoletes:      bluedevil-devel < 2.0.0-0.10

Requires:       pulseaudio-module-bluetooth
Requires:       kf5-kded

# When -autostart was removed
Obsoletes:      bluedevil-autostart < 5.2.95

%description
BlueDevil is the bluetooth stack for KDE.


%prep
%setup -q -n %{name}-%{version}

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_flags} -C %{_target_platform}


%install

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang bluedevil5  --with-qt --all-name

%check
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/org.kde.bluedevilsendfile.desktop
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/org.kde.bluedevilwizard.desktop


%post
touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
update-desktop-database -q &> /dev/null
touch --no-create %{_datadir}/mime/packages &> /dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
update-desktop-database -q &> /dev/null
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files -f bluedevil5.lang
%doc README
%{_kf5_bindir}/bluedevil-sendfile
%{_kf5_bindir}/bluedevil-wizard
%{_kf5_qtplugindir}/kcm_*.so
%{_kf5_qtplugindir}/kio_*.so
%{_kf5_plugindir}/kded/*.so
%{_kf5_qtplugindir}/bluetoothfileitemaction.so
%{_kf5_datadir}/remoteview/bluetooth-network.desktop
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservices5/*.protocol
%{_kf5_datadir}/knotifications5/bluedevil.notifyrc
%{_kf5_datadir}/applications/org.kde.bluedevilsendfile.desktop
%{_kf5_datadir}/applications/org.kde.bluedevilwizard.desktop
%{_kf5_datadir}/bluedevilwizard/
%{_kf5_datadir}/plasma/plasmoids/org.kde.plasma.bluetooth
%{_kf5_qmldir}/org/kde/plasma/private/bluetooth/
%{_datadir}/mime/packages/*.xml


%changelog
* Sat Mar 05 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.95-1
- Plasma 5.5.95

* Tue Mar 01 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.5-1
- Plasma 5.5.5

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.4-1
- Plasma 5.5.4

* Thu Jan 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.3-1
- Plasma 5.5.3

* Thu Dec 31 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.5.2-1
- 5.5.2

* Fri Dec 18 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.1-1
- Plasma 5.5.1

* Thu Dec 03 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.0-1
- Plasma 5.5.0

* Wed Nov 25 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.95-1
- Plasma 5.4.95

* Thu Nov 05 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.3-1
- Plasma 5.4.3

* Thu Oct 01 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-1
- 5.4.2

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-1
- 5.4.1

* Fri Aug 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- Plasma 5.4.0

* Thu Aug 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-1
- Plasma 5.3.95

* Thu Jun 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.2-1
- Plasma 5.3.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-2
- Rebuild against kf5-bluez-qt 5.11 (API/ABI break as BluezQt became a proper Framework)

* Tue May 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma 5.3.1

* Sat Apr 25 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-1
- 5.3.0

* Sat Apr 25 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.2.95-2
- drop Provides: -autostart (it's a lie, not included or supported anymore)
- .spec cosmetics

* Wed Apr 22 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-1
- Plasma 5.2.95

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Fri Jan 16 2015 Rex Dieter <rdieter@fedoraproject.org> 2.1-2
- -autostart: Autostart support for non-KDE environments (#1008602)

* Tue Jan 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Tue Dec 23 2014 Rex Dieter <rdieter@fedoraproject.org> 2.1-1
- 2.1

* Sun Dec 14 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-2
- pull in upstream fix for systray icon visibility when offline (kde#341768)

* Sat Dec 13 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-1
- 2.0

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-0.15.36f0438agit20140630
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-0.14.36f0438agit20140630
- update mime scriptlet

* Mon Jun 30 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-0.13.36f0438agit20140630
- 20140630 snapshot (#1114397)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-0.12.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 24 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-0.11.rc1
- bluedevil-2.0-rc1 respin

* Sat Dec 21 2013 Rex Dieter <rdieter@fedoraproject.org> - 2.0.0-0.10.rc1
- bluedevil-2.0-rc1
- fake 2.0.0 version (instead of 2.0) to avoid epoch 
- Obsoletes: bluedevil-devel

* Thu Dec 19 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-0.8.20131219
- 20131219 snapshot

* Thu Dec 19 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-0.7.20131128
- try out crash fixer (kde review 114433)

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 
- 2.0.0-0.6.20131128
- Obsolete dep on obexd (#998218)
- noarch -devel subpkg

* Mon Dec 09 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-0.5.20131128
- 20131128 snapshot

* Tue Oct 15 2013 Lukáš Tinkl <ltinkl@redhat.com> 2.0.0-0.4.20131015git
- updated git snapshot from the bluez5 branch
- translations included

* Fri Sep 20 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-0.3.20130907git
- fresh bluez5 branch snapshot

* Fri Sep 20 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-0.2.20130621
- drop Requires: obex-data-server (deprecated with bluez5)

* Wed Aug 14 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-0.1.20130621
- bluedevil-2.0.0-20130621 bluez5 branch snapshot

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 19 2013 Rex Dieter <rdieter@fedoraproject.org> 1.3-3
- ExcludeArch: s390 s390x (#975736)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 31 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3-1
- 1.3

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-0.6.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3-0.5.rc2
- include translations (copied from -rc1)

* Sun Apr 29 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3-0.4.rc2
- update to 1.3-rc2

* Wed Apr 25 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3-0.3.rc1
- kde daemon crash (kde#284052)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 03 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.3-0.1.rc1
- update to 1.3-rc1

* Mon Oct 10 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.2.2-1
- update to 1.2.2

* Tue Sep 13 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.2-1
- update to 1.2 final

* Mon Sep 05 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.2-0.2.rc2
- update to 1.2-rc2

* Fri Aug 19 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.2-0.1.rc1
- update to 1.2-rc1

* Tue Jul 26 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.1.1-1
- update to 1.1.1

* Mon May 02 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.1-2
- rebuilt for libbluedevil 1.9 snapshot

* Fri Apr 15 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.1-1
- update to 1.1
- add pulseaudio-module-bluetooth req

* Mon Mar 28 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.0.3-1
- update to 1.0.3

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.0.2-2
- Requires: obex-data-server obexd (for file transfers)

* Wed Feb 02 2011 Lukas Tinkl <ltinkl@redhat.com> - 1.0.2-1
- 1.0.2 upstream version, fixes mainly for device pairing and obex crashes

* Tue Feb 01 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-3
- Requires: kdebase-runtime
- add scriptlets

* Sat Jan 29 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.0.1-2
- Provides: dbus-bluez-pin-helper (keeps blueman and hal off the KDE spin)
- fix kbluetooth Obsoletes to match 0.4.2-2.fc* properly

* Fri Jan 14 2011 Jaroslav Reznik <jreznik@redhat.com> 1.0.1-1
- update to 1.0.1

* Tue Nov 30 2010 Jaroslav Reznik <jreznik@redhat.com> 1.0-1
- update to 1.0 final

* Mon Sep 27 2010 Jaroslav Reznik <jreznik@redhat.com> 1.0-0.1.rc4.1
- update to rc4-1

* Thu Aug 19 2010 Jaroslav Reznik <jreznik@redhat.com> 1.0-0.1.rc3
- update to rc3

* Fri Aug 13 2010 Jaroslav Reznik <jreznik@redhat.com> 1.0-0.1.rc2
- initial package
