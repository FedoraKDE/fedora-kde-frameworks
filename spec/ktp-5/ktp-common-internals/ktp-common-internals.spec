%global         git_date 20150305
%global         git_commit d85e200

Name:           ktp-common-internals
Summary:        Common internals for KDE Telepathy
Version:        0.9.80
Release:        1.%{git_date}git%{git_commit}%{?dist}

License:        LGPLv2+
URL:            https://projects.kde.org/projects/extragear/network/telepathy/%{name}
#Source0: http://download.kde.org/stable/kde-telepathy/%{version}/src/%{name}-%{version}.tar.bz2

# git archive --format=tar.gz --remote=git://anongit.kde.org/%%{name}.git \
#             --prefix=%%{name}-%%{version}/ --output=%%{name}-%%{git_commit}.tar.gz %%{git_commit}
Source0:        %{name}-%{git_commit}.tar.gz


## upstreamable patches

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel

BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-knotifyconfig-devel
BuildRequires:  kf5-ktexteditor-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-kconfig-devel

BuildRequires:  telepathy-qt5-devel
BuildRequires:  telepathy-logger-qt5-devel
BuildRequires:  kf5-kpeople-devel
BuildRequires:  kaccounts-devel
BuildRequires:  libaccounts-qt5-devel

BuildRequires:  libotr-devel
BuildRequires:  libgcrypt-devel

Requires:       kaccounts-providers

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       telepathy-qt5-devel
Requires:       kf5-kwallet-devel
Requires:       telepathy-logger-qt5-devel
%description devel
%{summary}.


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


%post
/sbin/ldconfig
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
fi

%files
%doc COPYING
%{_bindir}/ktp-debugger
%{_libexecdir}/ktp-proxy
%{_kf5_qtplugindir}/*.so
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservicetypes5/ktp_logger_plugin.desktop
%{_kf5_qtplugindir}/kaccounts/daemonplugins/*.so
%{_libdir}/libKTpCommonInternals.so.*
%{_libdir}/libKTpModels.so.*
%{_libdir}/libKTpWidgets.so.*
%{_libdir}/libKTpLogger.so.*
%{_libdir}/libKTpOTR.so.*
%{_kf5_qmldir}/org/kde/telepathy
%{_kf5_datadir}/katepart5/syntax/ktpdebugoutput.xml
%{_kf5_datadir}/knotifications5/*.notifyrc
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/config.kcfg/ktp-proxy-config.kcfg
%{_datadir}/dbus-1/services/*.service
%{_datadir}/telepathy/clients/KTp.Proxy.client

%files devel
%{_libdir}/cmake/KTp
%{_libdir}/libKTpCommonInternals.so
%{_libdir}/libKTpModels.so
%{_libdir}/libKTpWidgets.so
%{_libdir}/libKTpLogger.so
%{_libdir}/libKTpOTR.so
%{_includedir}/KTp



%changelog
* Thu Mar 05 2015 Daniel Vrátil <dvratil@redhat.com> - 0.9.80-1.20150305gitd85e200
- Update to latest git snapshot

* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 0.9.50-1.20150122git49d1abe
- Update to experimental KF5 version

* Mon Oct 20 2014 Jan Grulich <jgrulich@redhat.com> - 0.9.0-1
- Update to 0.9.0

* Wed Sep 17 2014 Jan Grulich <jgrulich@redhat.com> - 0.8.80-1
- Update to 0.8.80 (beta)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Jan Grulich <jgrulich@redhat.com> 0.8.1-1
- 0.8.1

* Wed Mar 12 2014 Jan  Grulich <jgrulich@redhat.com> 0.8.0-1
- 0.8.0

* Tue Feb 25 2014 Jan Grulich <jgrulich@redhat.com> 0.7.80-1
- 0.7.80

* Wed Jan 15 2014 Jan Grulich <jgrulich@redhat.com> 0.7.1-1
- 0.7.1

* Tue Oct 29 2013 Jan Grulich <jgrulich@redhat.com> 0.7.0-1
- 0.7.0

* Wed Sep 25 2013 Rex Dieter <rdieter@fedoraproject.org> 0.6.80-2
- enable libkpeople support

* Tue Sep 24 2013 Rex Dieter <rdieter@math.unl.edu> - 0.6.80-1
- 0.6.80

* Tue Aug 06 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.6.3-1
- 0.6.3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 20 2013 Jan Grulich <jgrulich@redhat.com> 0.6.2-1
- 0.6.2

* Wed Apr 17 2013 Jan Grulich <jgrulich@redhat.com> 0.6.1-1
- 0.6.1

* Tue Apr 02 2013 Jan Grulich <jgrulich@redhat.com> 0.6.0-1
- 0.6.0

* Mon Mar 11 2013 Rex Dieter <rdieter@fedoraproject.org> 0.5.80-2
- -devel: Requires: pkgconfig(TelepathyLoggerQt4)

* Thu Mar 07 2013 Rex Dieter <rdieter@fedoraproject.org> 0.5.80-1
- 0.5.80

* Sun Feb 17 2013 Jan Grulich <jgrulich@redhat.com> - 0.5.3-1
- 0.5.3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Jan Grulich <jgrulich@redhat.com> - 0.5.2-1
- 0.5.2

* Fri Oct 05 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.5.1-1
- 0.5.1

* Mon Aug 27 2012 Rex Dieter <rdieter@fedoraproject.org> 0.5.0-1
- 0.5.0

* Thu Jul 26 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.1-1
- 0.4.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-1
- 0.4.0

* Mon Apr 02 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.1-1
- 0.3.1

* Tue Jan 24 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-1
- ktp-common-internals-0.3.0
