%global         git_date 20150305
%global         git_commit 74835c7


Name:           ktp-text-ui
Summary:        Telepathy text chat handler
Version:        0.9.80
Release:        1.%{git_date}git%{git_commit}%{?dist}

# GPLv2+: most code
# (BSD or AFL): data/styles/renkoo.AdiumMessageStyle
# MIT:  data/styles/simkete/, fadomatic javascript code used in Renkoo
License:        GPLv2+ and (BSD or AFL) and MIT
URL:            https://projects.kde.org/projects/extragear/network/telepathy/%{name}

#Source0:        http://download.kde.org/stable/kde-telepathy/%{version}/src/%{name}-%{version}.tar.bz2

# git archive --format=tar.gz --remote=git://anongit.kde.org/%%{name}.git \
#             --prefix=%%{name}-%%{version}/ --output=%%{name}-%%{git_commit}.tar.gz %%{git_commit}
Source0:        %{name}-%{git_commit}.tar.gz


BuildRequires:  desktop-file-utils
BuildRequires:  dos2unix

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtwebkit-devel

BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kemoticons-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-knotifyconfig-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kdewebkit-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kitemviews-devel

BuildRequires:  ktp-common-internals-devel >= %{version}
BuildRequires:  telepathy-logger-qt5-devel


Requires:       ktp-accounts-kcm

Obsoletes:      telepathy-kde-text-ui < 0.3.0
Provides:       telepathy-kde-text-ui = %{version}-%{release}

Obsoletes:      ktp-text-ui-devel < 0.6.80

%description
%{summary}.


%prep
%setup -qn %{name}-%{version}

# looks like someone cat'd several files with different encoding (and line endings)
# into one.  we'll do our best to make it usable
mac2unix data/styles/renkoo.AdiumMessageStyle/Contents/Resources/Renkoo*LICENSE.txt


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

rm -fv %{buildroot}%{_libdir}/libktpchat.so

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/ktp-log-viewer.desktop


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING 
%doc data/styles/renkoo.AdiumMessageStyle/Contents/Resources/Renkoo*LICENSE.txt
%doc data/styles/SimKete.AdiumMessageStyle/Contents/README
%{_bindir}/ktp-log-viewer
%{_datadir}/applications/ktp-log-viewer.desktop
%{_datadir}/ktp-log-viewer/
%{_libdir}/libktpchat.so.*
%{_libdir}/libktpimagesharer.so
%{_kf5_qtplugindir}/kcm_ktp_chat_appearance.so
%{_kf5_qtplugindir}/kcm_ktp_chat_behavior.so
%{_kf5_qtplugindir}/kcm_ktp_chat_messages.so
%{_kf5_qtplugindir}/kcm_ktp_chat_otr.so
%{_kf5_qtplugindir}/kcm_ktp_logviewer_behavior.so
%{_kf5_qtplugindir}/kcm_ktptextui_message_filter_latex.so
%{_kf5_qtplugindir}/ktptextui_message_filter_*.so
%{_libexecdir}/ktp-adiumxtra-protocol-handler
%{_libexecdir}/ktp-text-ui
%{_kf5_datadir}/kservices5/kcm_ktp_chat_appearance.desktop
%{_kf5_datadir}/kservices5/kcm_ktp_chat_behavior.desktop
%{_kf5_datadir}/kservices5/kcm_ktp_chat_messages.desktop
%{_kf5_datadir}/kservices5/kcm_ktp_chat_otr.desktop
%{_kf5_datadir}/kservices5/kcm_ktp_logviewer_behavior.desktop
%{_kf5_datadir}/kservices5/kcm_ktptextui_message_filter_latex.desktop
%{_kf5_datadir}/kservices5/ktptextui_message_filter_*.desktop
%{_kf5_datadir}/kservices5/adiumxtra.protocol
%{_kf5_datadir}/kservicetypes5/ktptxtui_message_filter.desktop
%{_datadir}/ktelepathy/
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.KTp.TextUi.service
%{_datadir}/telepathy/clients/KTp.TextUi.client
%{_kf5_datadir}/kxmlgui5/ktp-text-ui


%changelog
* Thu Mar 05 2015 Daniel Vrátil <dvratil@redhat.com> - 0.9.80-1.20150305git74835c7
- Update to latest git snapshot

* Fri Jan 23 2015 Daniel Vrátil <dvratil@redhat.com> - 0.9.60-1.20150123git5246520
- Update to experimental KF5 version

* Mon Oct 20 2014 Jan Grulich <jgrulich@redhat.com> - 0.9.0-1
- Update to 0.9.0

* Wed Sep 17 2014 Jan Grulich <jgrulich@redhat.com> - 0.8.80-1
- Update to 0.8.80 (beta)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 19 2014 Rex Dieter <rdieter@fedoraproject.org> 0.8.1-3
- BR: kdelibs4-webkit-devel

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Jan Grulich <jgrulich@redhat.com> 0.8.1-1
- 0.8.1

* Thu Mar 13 2014 Jan Grulich <jgrulich@redhat.com> - 0.8.0-2
- fixed version

* Wed Mar 12 2014 Jan Grulich <jgrulich@redhat.com> - 0.8.0-1
- 0.8.0

* Wed Feb 26 2014 Jan Grulich <jgrulich@redhat.com> - 0.7.80-1
- 0.7.80

* Wed Jan 15 2014 Jan Grulich <jgrulich@redhat.com> - 0.7.1-1
- 0.7.1

* Tue Oct 29 2013 Jan Grulich <jgrulich@redhat.com> - 0.7.0-1
- 0.7.0

* Wed Sep 25 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.6.80-1
- 0.6.80

* Tue Aug 06 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.6.3-1
- 0.6.3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 18 2013 Jan Grulich <jgrulich@redhat.com>-  0.6.2-1
- 0.6.2

* Wed Apr 17 2013 Jan Grulich <jgrulich@redhat.com> - 0.6.1-1
- 0.6.1

* Tue Apr 02 2013 Jan Grulich <jgrulich@redhat.com> - 0.6.0-1
- 0.6.0

* Thu Mar 07 2013 Rex Dieter <rdieter@fedoraproject.org> 0.5.80-1
- 0.5.80

* Sun Feb 17 2013 Jan Grulich <jgrulich@redhat.com> - 0.5.3-1
- 0.5.3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Jan Grulich <jgrulich@redhat.com> - 0.5.2-1
- 0.5.2

* Fri Nov 02 2012 Rex Dieter <rdieter@fedoraproject.org> 0.5.1-2
- rebuild (telepathy-logger)

* Fri Oct 05 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.5.1-1
- 0.5.1

* Mon Aug 27 2012 Rex Dieter <rdieter@fedoraproject.org> 0.5.0-1
- 0.5.0

* Thu Jul 26 2012 Jan Grulich <jgrulich@redhat.com> - 0.4.1-1
- 0.4.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 05 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-2
- enable/fix telepathy-logger-qt support

* Mon Jun 11 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-1
- 0.4.0

* Mon Apr 02 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.1-1
- 0.3.1

* Fri Feb 10 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-6
- -devel: fix typo in Requires

* Fri Feb 10 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-5
- -devel: Requires: ktp-common-internals-devel

* Fri Feb 10 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-4
- mac2unix '.../Renkoo LICENSE.txt'

* Fri Feb 10 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-3
- %%doc data/styles/simkete/Contents/README 
- fix %%doc Renkoo\ LICENSE.txt 
- License: clarify MIT for data/styles/simkete too

* Tue Feb 07 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-2
- drop BR: desktop-file-utils telepathy-qt4-devel
- %%post/%%postun ldconfig scriptlets
- License: GPLv2+ and (BSD or AFL) and MIT

* Wed Jan 25 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-1
- 0.3.0

* Fri Nov 25 2011 Rex Dieter <rdieter@fedoraproject.org> 0.2.0-1
- 0.2.0

* Thu Sep 15 2011 Rex Dieter <rdieter@fedoraproject.org> 0.1.0-2
- fix Source0 URL
- fix tabs/spaces

* Fri Aug 12 2011 Rex Dieter <rdieter@fedoraproject.org> 0.1.0-1
- first try


