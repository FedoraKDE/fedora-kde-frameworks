Name:           ksshaskpass
Version:        5.1.95
Release:        1%{?dist}
Summary:        A KDE version of ssh-askpass with KWallet support

Group:          Applications/Internet
License:        GPLv2
URL:            http://projects.kde.org/projects/kde/workspace/ksshaskpass

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

BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kdoctools-devel

BuildRequires:  desktop-file-utils

%description
%{summary}.

%prep
%setup -qn %{name}-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags}  -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot}  -C %{_target_platform}


# Setup environment variables
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/kde/env/
cat > $RPM_BUILD_ROOT%{_sysconfdir}/kde/env/ksshaskpass.sh << EOF
SSH_ASKPASS=%{_bindir}/ksshaskpass
export SSH_ASKPASS
EOF

# Remove *.la files
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/org.kde.ksshaskpass.desktop


%files
%doc ChangeLog COPYING README
%{_bindir}/ksshaskpass
%config(noreplace) %{_sysconfdir}/kde/env/ksshaskpass.*
%{_mandir}/*/*.gz
%{_datadir}/applications/org.kde.ksshaskpass.desktop


%changelog
* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1
- Plasma 5.1.95 Beta

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Nov  3 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.5.3-7
- Point to %%{_pkgdocdir} in %%description where available (#993830).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Mar 14 2010 Aurelien Bompard <abompard@fedoraproject.org> -  0.5.3-1
- version 0.5.3

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 30 2009 Aurelien Bompard <abompard@fedoraproject.org> 0.5.1-3
- fix bug 485009
- install the desktop file with desktop-file-install

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 30 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.5.1-1
- version 0.5.1

* Tue Jun 24 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.4.1-1
- version 0.4.1

* Sun Mar 30 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.4-2
- buildrequires cmake

* Sun Mar 30 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.4-1
- new version

* Tue Mar 11 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.3-5
- BR kdelibs3-devel instead of kdelibs-devel (#433963)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.3-4
- Autorebuild for GCC 4.3

* Sun Aug 26 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.3-3
- fix license tag
- rebuild for BuildID

* Tue Jan 09 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.3-2
- remove useless workaround
- put the environment script in /etc/kde/env

* Sun Jan 07 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.3-1
- initial package
