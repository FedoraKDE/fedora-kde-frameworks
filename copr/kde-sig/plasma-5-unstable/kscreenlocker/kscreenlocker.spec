Name:           kscreenlocker
Version:        5.4.90
Release:        1%{?dist}
Summary:        Library and components for secure lock screen architecture.

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/kscreenlocker

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-kidletime-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kglobalaccel-devel

BuildRequires:  kf5-kwayland-devel

BuildRequires:  libX11-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  libwayland-client-devel
BuildRequires:  libwayland-server-devel

Requires:       kf5-filesystem

%description
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%build

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
%license COPYING
%doc README


%changelog
* Sun Nov 08 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.90-1
- Plasma 5.4.90
