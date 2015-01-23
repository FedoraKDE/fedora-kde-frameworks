Name:           kdecoration
Summary:        A plugin-based library to create window decorations
Version:        5.2.0
Release:        1%{?dist}

License:        LGPLv2
URL:            https://projects.kde.org/projects/kde/workspace/kdecoration

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

Requires:       kf5-filesystem

%description
%{summary}.

%package devel
Summary:        Developer files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}.


%prep
%setup -q -n %{name}-%{version}


%build
# Cleanup includes mess, install everything into %%{_kf5_includedir}/KDecoration2
sed -i "s/set(KDECORATION2_INCLUDEDIR \"\${CMAKE_INSTALL_INCLUDEDIR}\/KDecoration2\")/set(KDECORATION2_INCLUDEDIR \"\${KF5_INCLUDE_INSTALL_DIR}\/KDecoration2\")/" \
    CMakeLists.txt src/CMakeLists.txt src/private/CMakeLists.txt

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING.LIB
%{_kf5_libdir}/libkdecorations2.so.*
%{_kf5_libdir}/libkdecorations2private.so.*

%files devel
%{_kf5_libdir}/libkdecorations2.so
%{_kf5_libdir}/libkdecorations2private.so
%{_kf5_libdir}/cmake/KDecoration2
%{_kf5_includedir}/KDecoration2
%{_kf5_includedir}/kdecoration2_version.h

%changelog
* Tue Jan 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-2.beta
- improved sed macro

* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta
