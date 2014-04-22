%define snapshot 20140418

Name:           polkit-qt5
Version:        0.103.0
Release:        0.20140422gitbac771e6%{?dist}
Summary:        Qt 5 bindings for PolicyKit

License:        GPLv2+
URL:            https://projects.kde.org/projects/kdesupport/polkit-qt-1

# git archive --format=tar --prefix=%{name}-%{version}-%{snapshot}/ \
#             --remote=git://anongit.kde.org/polkit-qt-1 qt5 | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz
Source0:        polkit-qt5-bac771e6.tar
Source1:        Doxyfile

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
%setup -q -n %{name}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
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
%{_libdir}/libpolkit-qt5-core-1.so.1*
%{_libdir}/libpolkit-qt5-gui-1.so.1*
%{_libdir}/libpolkit-qt5-agent-1.so.1*

%files devel
#%{_kf5_sysconfdir}/rpm/macros.polkit-qt
%{_includedir}/polkit-qt5-1/
%{_libdir}/libpolkit-qt5-core-1.so
%{_libdir}/libpolkit-qt5-gui-1.so
%{_libdir}/libpolkit-qt5-agent-1.so
%{_libdir}/pkgconfig/polkit-qt5-1.pc
%{_libdir}/pkgconfig/polkit-qt5-core-1.pc
%{_libdir}/pkgconfig/polkit-qt5-gui-1.pc
%{_libdir}/pkgconfig/polkit-qt5-agent-1.pc
%{_libdir}/cmake/PolkitQt5-1/

%files doc
%doc html/*


%changelog
* Tue Apr 22 2014 Daniel Vrátil <dvratil@redhat.com> 0.103.0-0.2.20140422git
- Fix install

* Mon Apr 21 2014 Daniel Vrátil <dvratil@redhat.com> - 0.103.0-20140421gitbac771e6
- Bump version, force rebuild

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 0.103.0-20140418gitbac771e6
- Update to git: bac771e6

* Fri Apr 18 2014 Daniel Vrátil <dvratil@redhat.com> 0.103.0-0.1.20140418git
- Update to latest git snapshot
- Drop patch for coinstallibility

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 0.103.0-0.1.20140205git
- Update to latest git snapshot

* Wed Jan 15 2014 Daniel Vrátil <dvratil@redhat.com> 0.103.0-0.1.20140115git
- fork from polkit-qt SPEC
