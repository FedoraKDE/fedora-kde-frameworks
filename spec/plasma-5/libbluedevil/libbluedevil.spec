Name:           libbluedevil
Summary:        A Qt wrapper for bluez
Version:        5.2.2
Release:        1%{?dist}

License:        LGPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/libbluedevil

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  qt5-qtbase-devel

Requires:       bluez >= 5

%description
%{name} is Qt-based library written handle all Bluetooth functionality.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
Development files for %{name}.


%prep
%setup -q -n %{name}-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/libbluedevil.so.*

%files devel
%doc HACKING
%{_includedir}/bluedevil/
%{_libdir}/libbluedevil.so
%{_libdir}/pkgconfig/bluedevil.pc


%changelog
* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Tue Jan 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Tue Dec 23 2014 Rex Dieter <rdieter@fedoraproject.org> 2.1-1
- 2.1

* Sat Dec 13 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0-1
- 2.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-0.10.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 07 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.9.rc1
- drop upstream commit that causes adapter to be unpowered on every boot (#1114397, kde#337193)

* Mon Jun 30 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.8.rc1
- backport recent upstream commits (#1114397)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-0.7.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 24 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.6.rc1
- libbluedevil-2.0-rc1 respin

* Sat Dec 21 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.5.rc1
- libbluedevil-2.0-rc1

* Fri Dec 20 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.4.20131220
- libbluedevil-2.0 20131220 bluez5 branch snapshot

* Thu Dec 19 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.3.20131219
- libbluedevil-2.0 20131219 bluez5 branch snapshot

* Mon Dec 09 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.2.20131113
- libbluedevil-2.0 20131113 bluez5 branch snapshot

* Wed Aug 14 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.1.20130323
- libbluedevil-2.0-20130323 bluez5 branch snapshot

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 19 2013 Rex Dieter <rdieter@fedoraproject.org> 1.9.2-4
- ExcludeArch: s390 s390x (#975736)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 29 2012 Rex Dieter <rdieter@fedoraproject.org> 1.9.2-1
- 1.9.2

* Fri Mar 30 2012 Rex Dieter <rdieter@fedoraproject.org> 1.9.1-1
- 1.9.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-0.2.20110502git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon May 02 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.9-0.1
- update to pre-release snapshot of 1.9

* Mon Mar 28 2011 Jaroslav Reznik <jreznik@redhat.com> - 1.8.1-1
- update to 1.8.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 30 2010 Jaroslav Reznik <jreznik@redhat.com> - 1.8-3
- update to 1.8-1 (respin?)

* Wed Sep 29 2010 jkeating - 1.8-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Jaroslav Reznik <jreznik@redhat.com> - 1.8-1
- update to 1.8

* Fri Aug 13 2010 Jaroslav Reznik <jreznik@redhat.com> - 1.7-1
- initial package
