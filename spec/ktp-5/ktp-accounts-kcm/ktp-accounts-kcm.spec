%global         git_date    20150122
%global         git_commit  87c47de

Name:           ktp-accounts-kcm
Summary:        KDE Configuration Module for Telepathy Instant Messaging Accounts
Version:        0.9.60
Release:        1.%{git_date}git%{git_commit}%{?dist}

License:        LGPLv2+
URL:            https://projects.kde.org/projects/extragear/network/telepathy/%{name}
#Source0:        http://download.kde.org/stable/kde-telepathy/%{version}/src/%{name}-%{version}.tar.bz2

# git archive --format=tar.gz --remote=git://anongit.kde.org/%%{name}.git \
#             --prefix=%%{name}-%%{version}/ --output=%%{name}-%%{git_commit}.tar.gz %%{git_commit}
Source0:        %{name}-%{git_commit}.tar.gz

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kitemviews-devel

BuildRequires:  ktp-common-internals-devel

BuildRequires:  telepathy-qt5-devel
BuildRequires:  kaccounts-devel
BuildRequires:  intltool
BuildRequires:  libaccounts-glib-devel

## FIXME: FTBFS on rawhide -- rex
#BuildRequires: pkgconfig(ModemManagerQt)

Obsoletes:      telepathy-kde-accounts-kcm < 0.3.0
Provides:       telepathy-kde-accounts-kcm = %{version}-%{release}

Obsoletes:      telepathy-kde-accounts-kcm-plugins < 0.2.0
Provides:       telepathy-kde-accounts-kcm-plugins = %{version}-%{release}

Obsoletes:      telepathy-kde-accounts-kcm-devel < 0.2.0

# various protocol handlers
## msn (old)
#Requires: telepathy-butterfly
## xmpp/jabber
Requires:       telepathy-gabble
## msn (newer, libpurple)
Requires:       telepathy-haze
## irc
#Requires: telepathy-idle
## audio calls
Requires:       telepathy-rakia >= 0.7.4
## local xmpp
Requires:       telepathy-salut
## gadu/gadu
#Requires: telepathy-sunshine

%description
This is a KControl Module which handles adding/editing/removing Telepathy
Accounts. It interacts with any Telepathy Spec compliant AccountManager
to manipulate the accounts.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       telepathy-qt5-devel
%description devel
%{summary}.


%prep
%setup -q -n %{name}-%{version}


%build
# KAccounts install cmake config already
rm -fv cmake/modules/FindKAccounts.cmake
sed -i "s/\${KACCOUNTS_LIBRARIES}/KAccounts/" plugins/kaccounts/CMakeLists.txt

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

## unpackaged files
rm -fv %{buildroot}%{_kf5_libdir}/libktpaccountskcminternal.so


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING README
%{_kf5_libdir}/libktpaccountskcminternal.so.*
%{_kf5_datadir}/kservicetypes5/ktpaccountskcminternal-accountuiplugin.desktop
%{_datadir}/telepathy/profiles/*.profile
%{_datadir}/accounts/services/*.service
%{_datadir}/accounts/providers/*.provider
%{_kf5_qtplugindir}/*.so
%{_kf5_qtplugindir}/kaccounts/ui/ktpaccountskcm_plugin_kaccounts.so
%{_kf5_datadir}/kservices5/*.desktop

%files devel
%{_includedir}/KCMTelepathyAccounts


%changelog
* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 0.9.60-1.20150122git87c47de
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

* Wed Mar 12 2014 Jan Grulich <jgrulich@redhat.com> 0.8.0-1
- 0.8.0

* Wed Feb 26 2014 Jan Grulich <jgrulich@redhat.com> - 0.7.80-1
- 0.7.80

* Wed Jan 15 2014 Jan Grulich <jgrulich@redhat.com> - 0.7.1-1
- 0.7.1

* Tue Oct 29 2013 Jan Grulich <jgrulich@redhat.com> - 0.7.0-1
- 0.7.0

* Tue Sep 24 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.6.80-1
- 0.6.80

* Tue Aug 06 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.6.3-1
- 0.6.3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 20 2013 Jan Grulich <jgrulich@redhat.com> 0.6.2-1
- 0.6.2

* Wed Apr 17 2013 Jan Grulich <jgrulich@redhat.com> - 0.6.1-1
- 0.6.1

* Tue Apr 02 2013 Jan Grulich <jgrulich@redhat.com> - 0.6.0-1
- 0.6.0

* Mon Mar 11 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.5.80-1
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

* Thu Jul 26 2012 Jan Grulich <jgrulich@redhat.com> - 0.4.1-1
- 0.4.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-2
- (re)enable telepathy-rakia support (#838585)

* Mon Jun 11 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-1
- 0.4.0

* Mon Apr 02 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.1-1
- 0.3.1

* Fri Feb 17 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-4
- drop (unconditionally) butterly, rakia, sunshine
- move Requires: telepathy-mission-control lower in the stack

* Fri Feb 10 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-3
- drop telepathy-sunshine support (f17+)

* Tue Feb 07 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-2
- improve %%description
- drop BR: telepathy-qt4-devel
- omit libktpaccountskcminternal.so

* Tue Jan 24 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-1
- ktp-accounts-kcm-0.3.0

* Fri Nov 25 2011 Rex Dieter <rdieter@fedoraproject.org> 0.2.0-1
- 0.2.0

* Mon Sep 26 2011 Rex Dieter <rdieter@fedoraproject.org> 0.1.0-3
- Requires: telepathy-mission-control

* Wed Sep 14 2011 Rex Dieter <rdieter@fedoraproject.org> 0.1.0-2
- fix Source URL
- fix mixed spaces/tabs

* Fri Aug 12 2011 Rex Dieter <rdieter@fedoraproject.org> 0.1.0-1
- first try


