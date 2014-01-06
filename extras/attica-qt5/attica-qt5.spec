%define snapshot  20140106

Name:           attica-qt5
Version:        1.0.0
Release:        0.1.%{snapshot}git
Summary:        Implementation of the Open Collaboration Services API built against Qt 5

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/attica.git master | \
# gzip -c > %{name}-%{version}-%{snapshot}.tar.gz
Source0:        attica-qt5-1.0.0-%{snapshot}.tar.gz

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

%description
Attica is a Qt library that implements the Open Collaboration Services
API version 1.4. This package is built against Qt 5

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
%{summary}.


%prep
%setup -q


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} \
  -DQT4_BUILD:BOOL=FALSE \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%check
# verify pkg-config sanitry/version
export PKG_CONFIG_PATH=%{buildroot}%{_kf5_libdir}/pkgconfig
test "$(pkg-config --modversion libattica)" = "%{version}"


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README
%doc ChangeLog
%{_kf5_libdir}/libattica.so.1.*

%files devel
%{_kf5_includedir}/attica/
%{_kf5_libdir}/libattica.so
%{_kf5_libdir}/pkgconfig/libattica.pc
%{_kf5_libdir}/cmake/LibAttica/


%changelog
* Mon Jan 06 2014 Daniel Vrátil <dvratil@redhat.com> 0.4.2-1
- attica-qt5 1.0.0 - fork attica to attica-qt5

* Sat Jun 15 2013 Rex Dieter <rdieter@fedoraproject.org> 0.4.2-1
- 0.4.2

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 07 2013 Rex Dieter <rdieter@fedoraproject.org> 0.4.1-1
- 0.4.1

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-1
- 0.4.0

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 31 2011 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-2
- update %%files for non-standard soname

* Fri Dec 30 2011 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-1
- 0.3.0

* Tue Nov 15 2011 Rex Dieter <rdieter@fedoraproject.org> 0.2.9-1
- 0.2.9

* Sat Feb 26 2011 Rex Dieter <rdieter@fedoraproject.org> 0.2.0-1
- attica-0.2.0

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 20 2010 Rex Dieter <rdieter@fedoraproject.org> -  0.1.91-1
- attica-0.1.91

* Tue May 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.1.4-1
- attica-0.1.4

* Wed Apr 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.1.3-1
- attica-0.1.3

* Thu Jan 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.1.2-1
- attica-0.1.2
- patch Version in libattica.pc
- %%build: %%_cmake_skip_rpath 

* Fri Dec 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.1.1-1
- attica-0.1.1

* Wed Dec  9 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.1.0-3
- upstream tarball
- %files: tighten up a bit, track sonames

* Mon Dec  7 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 0.1.0-2
- Out of sourcetree build
- Use make install/fast

* Sat Dec 5 2009 lvillani <lvillani@enterprise.binaryhelix.net> 0.1.0-1
- Initial release

