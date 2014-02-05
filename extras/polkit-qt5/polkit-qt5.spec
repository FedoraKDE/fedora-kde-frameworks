%define snapshot 20140205

Name:           polkit-qt5
Version:        0.103.0
Release:        0.1.%{snapshot}git%{?dist}
Summary:        Qt 5 bindings for PolicyKit

License:        GPLv2+
URL:            https://projects.kde.org/projects/kdesupport/polkit-qt-1 

# git archive --format=tar --prefix=%{name}-%{version}-%{snapshot}/ \
#             --remote=git://anongit.kde.org/polkit-qt-1 qt5 | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz
Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2 
Source1:        Doxyfile

Patch0:         polkit-qt5-cmake-config-fix.patch

BuildRequires:  extra-cmake-modules
BuildRequires:  polkit-devel >= 0.98
BuildRequires:  qt5-qtbase-devel
BuildRequires:  doxygen

%description
Polkit-qt5 is a library that lets developers use the PolicyKit API
through a nice Qt-styled API.

%package devel
Summary: Development files for PolicyKit Qt 5 bindings
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package doc
Summary: Doxygen documentation for the PolkitQt API
Group: Documentation
BuildArch: noarch
%description doc
%{summary}.


%prep
%setup -q -n %{name}-%{version}-%{snapshot}

%patch0 -p1 -b .cmakefix

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} \
  -DBUILD_EXAMPLES:BOOL=OFF \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}

doxygen %{SOURCE1}

# Remove installdox file - it is not necessary here
rm -fv html/installdox


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README
%{_kf5_libdir}/libpolkit-qt-core-1.so.1*
%{_kf5_libdir}/libpolkit-qt-gui-1.so.1*
%{_kf5_libdir}/libpolkit-qt-agent-1.so.1*

%files devel
#%{_kf5_sysconfdir}/rpm/macros.polkit-qt
%{_kf5_includedir}/polkit-qt-1/
%{_kf5_libdir}/libpolkit-qt-core-1.so
%{_kf5_libdir}/libpolkit-qt-gui-1.so
%{_kf5_libdir}/libpolkit-qt-agent-1.so
%{_kf5_libdir}/pkgconfig/polkit-qt-1.pc
%{_kf5_libdir}/pkgconfig/polkit-qt-core-1.pc
%{_kf5_libdir}/pkgconfig/polkit-qt-gui-1.pc
%{_kf5_libdir}/pkgconfig/polkit-qt-agent-1.pc
%{_kf5_libdir}/cmake/PolkitQt-1/

%files doc
%doc html/*


%changelog
* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 0.103.0-0.1.20140205git
- Update to latest git snapshot

* Wed Jan 15 2014 Daniel Vrátil <dvratil@redhat.com> 0.103.0-0.1.20140115git
- fork from polkit-qt SPEC
