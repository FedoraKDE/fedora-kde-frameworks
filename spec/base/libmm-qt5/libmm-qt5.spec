%global         git_commit d257bb2
Name:           libmm-qt5
Version:        1.0.1
Release:        1.20140403git%{git_commit}%{?dist}
Epoch:          1
Summary:        Qt 5 wrapper for ModemManager DBus API

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://projects.kde.org/projects/extragear/libs/libmm-qt

#Source0:        http://download.kde.org/unstable/modemmanager-qt/%{version}/src/%{name}-%{version}.tar.xz
# Package from git snapshots using releaseme scripts
Source0:        %{name}-%{version}-git%{git_commit}.tar.xz

BuildRequires:  cmake >= 2.6
BuildRequires:  qt5-qtbase-devel
BuildRequires:  ModemManager-devel >= 1.0.0

%description
Qt library for ModemManager

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
%description devel
Qt libraries and header files for developing applications that use ModemManager

%prep
%setup -qn libmm-qt-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/libModemManagerQt5.so.*


%files devel
%{_libdir}/pkgconfig/ModemManagerQt5.pc
%{_includedir}/ModemManagerQt5/
%{_libdir}/libModemManagerQt5.so

%changelog
* Thu Apr 03 2014 Daniel Vrátil <dvratil@redhat.com> - 1:1.0.1-1.20140403gitd257bb2
- Qt 5 fork of libmm-qt

* Tue Feb 25 2014 Jan Grulich <jgrulich@redhat.com> - 1:1.0.1-1
- Update to 1.0.1
- Remove ModemManager as dependency (#1063378)

* Thu Nov 21 2013 Jan Grulich <jgrulich@redhat.com> - 1:1.0.0-2
- Update to 1.0.0 (stable release)

* Wed Oct 9 2013 Jan Grulich <jgrulich@redhat.com> - 1:1.0.0-1.20131009git1496e4d
- Update to current git snapshot

* Mon Sep 16 2013 Jan Grulich <jgrulich@redhat.com> - 1:0.5.1-1
- Update to 0.5.1

* Tue Sep 10 2013 Jan Grulich <jgrulich@redhat.com - 1:0.5.0-1
- First stable release (0.5.0)

* Mon Aug 12 2013 Lukas Tinkl <ltinkl@redhat.com> - 0.6.0-4.20130812gitd84301
- Update to current git snapshot

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-3.20130613gitc5920e0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Jan Grulich <jgrulich@redhat.com> - 0.6.0-2.20130613gitc5920e0
- Update to the current git snapshot

* Fri May 31 2013 Jan Grulich <jgrulich@redhat.com> - 0.6.0-1.20130422git657646b
- Initial package
- Based on git snapshot 657646bdc1eb9913e07a8307afd2b47b6225209b
