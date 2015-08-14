%global         base_name polkit-kde-agent-1

Name:           polkit-kde
Summary:        PolicyKit integration for KDE Desktop
Version:        5.3.95
Release:        1%{?dist}

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/polkit-kde-agent-1

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{base_name}-%{version}.tar.xz


BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-knotifications-devel

BuildRequires:  polkit-qt5-1-devel

Provides: PolicyKit-authentication-agent = %{version}-%{release}
Provides: polkit-kde-1 = %{version}-%{release}
Provides: polkit-kde-agent-1 = %{version}-%{release}

Obsoletes: PolicyKit-kde < 4.5

# Add explicit dependency on polkit, since polkit-libs were split out
Requires: polkit

%description
Provides Policy Kit Authentication Agent that nicely fits to KDE.


%prep
%setup -q -n %{base_name}-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang polkit-kde-authentication-agent-1 --with-kde

# Move the agent from libexec to libexec/kf5
sed -i "s/Exec=\/usr\/libexec\//Exec=\/usr\/libexec\/kf5\//" %{buildroot}/%{_sysconfdir}/xdg/autostart/polkit-kde-authentication-agent-1.desktop
mkdir -p %{buildroot}/%{_kf5_libexecdir}/
mv %{buildroot}/%{_libexecdir}/polkit-kde-authentication-agent-1 \
   %{buildroot}/%{_kf5_libexecdir}


%files -f polkit-kde-authentication-agent-1.lang
%doc COPYING
%{_kf5_libexecdir}/polkit-kde-authentication-agent-1
%{_sysconfdir}/xdg/autostart/polkit-kde-authentication-agent-1.desktop
%{_kf5_datadir}/knotifications5/policykit1-kde.notifyrc


%changelog
* Thu Aug 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-1
- Plasma 5.3.95

* Thu Jun 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.2-1
- Plasma 5.3.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma 5.3.1

* Mon Apr 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- Plasma 5.3.0

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

* Sun Jan 25 2015 Rex Dieter <rdieter@fedoraproject.org> 0.99.1-6.20130311git
- Requires: polkit

* Tue Jan 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Wed Oct 22 2014 Daniel Vrátil <dvratil@redhat.com> - 0.99.1-5.20130311git
- Install autostart file to /etc/xdg/autostart so that Plasma 5 picks it up too

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.1-4.20130311git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.1-3.20130311git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.1-2.20130311git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.99.1-1.20130311git
- 0.99.1 git snapshot
- Provides: polkit-kde-agent-1
- .spec cosmetics

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Rex Dieter <rdieter@fedoraproject.org> 0.99.0-3
- patch to bring polkit auth dialog to front
- patch restart polkit-kde on crash 
- patch to remove unimplimented 'remember authorization' checkbox

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.99.0-1
- Update to 0.99.0

* Thu Nov 25 2010 Radek Novacek <rnovacek@redhat.com> 0.98.1-1
- Update to polkit-kde-0.98.1

* Thu Nov 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.95.1-7
- rebuild (polkit-qt) 

* Wed Aug 04 2010 Radek Novacek <rnovacek@redhat.com> - 0.95.1-6
- Fixed FTBFS with GCC-4.5

* Wed Aug 04 2010 Radek Novacek <rnovacek@redhat.com> - 0.95.1-5
- Add patch for showing "password for root" when root user is authenticating
- Related: #618543

* Sun Feb 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.95.1-4
- FTBFS polkit-kde-0.95.1-3.fc13: ImplicitDSOLinking (#564809)

* Wed Jan 06 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.95.1-3
- Again provides PolicyKit-authentication-agent

* Tue Jan 05 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.95.1-2
- Added Gettext BR

* Tue Jan 05 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.95.1-1
- Update to official release
- Provides polkit-kde-1

* Mon Nov 30 2009 Jaroslav Reznik <jreznik@redhat.com> - 0.95-0.2.20091125svn
- Adds desktop file
- Adds obsoletes

* Wed Nov 25 2009 Jaroslav Reznik <jreznik@redhat.com> - 0.95-0.1.20091125svn
- Initial package
