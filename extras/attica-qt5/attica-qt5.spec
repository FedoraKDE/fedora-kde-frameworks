%define snapshot 20140205


Name:           attica-qt5
Version:        1.0.0
Release:        %{snapshot}git%{?dist}
Summary:        Implementation of the Open Collaboration Services API built against Qt 5

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/attica,git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz
Source0:        attica-qt5-%{version}-%{snapshot}git.tar.bz2

#Source0:        http://download.kde.org/unstable/frameworks/%{version}/attica-%{version}.tar.xz

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
%setup -q -n attica-1.0.0


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


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README
%doc ChangeLog
%{_kf5_libdir}/libKF5Attica.so.1.*

%files devel
%{_kf5_includedir}/attica/
%{_kf5_libdir}/libKF5Attica.so
%{_kf5_libdir}/cmake/KF5Attica/


%changelog
* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 1.0.0-20140205git
- Update snapshot of Attica to current git

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 1.0.0-1
- Update to KDE Frameworks 5 TP1 (4.9.95)

* Mon Jan 06 2014 Daniel Vrátil <dvratil@redhat.com> 0.4.2-1
- Attica-qt5 4.9.95 - fork attica to attica-qt5
