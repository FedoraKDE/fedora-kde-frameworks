%define framework umbrella

Name:           kf5-%{framework}
Version:        4.95.0
Release:        1%{?dist}
Summary:        CMake configuration for KDE Frameworks 5

License:        GPLv2+
URL:            http://www.kde.org
Source0:        http://download.kde.org/unstable/frameworks/%{version}/kf5umbrella-%{version}.tar.xz

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

%description
Provides CMake configuration file for KDE Frameworks 5


%prep
%setup -q -n kf5umbrella-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} DESTDIR=%{buildroot} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%files
%doc README.md
%{_kf5_libdir}/cmake/KF5


%changelog
* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Thu Jan  9 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version

