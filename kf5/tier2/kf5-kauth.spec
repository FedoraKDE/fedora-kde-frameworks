%define snapshot  20140104

Name:           kf5-kauth
Version:        5.0.0
Release:        0.1.%{snapshot}git
Summary:        KDE Frameworks tier 2 integration module to perform actions as privileged user

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{snapshot}/ \
#             --remote=git://anongit.kde.org/%{name}.git master | \
# gzip -c > %{name}-%{snapshot}.tar.gz
Source0:        %{name}-%{snapshot}.tar.gz

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  kf5-kcoreaddons-devel


%description
KAuth is a framework to let applications perform actions as a privileged user.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} DESTDIR=%{buildroot} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING.LIB README.md
%{_kf5_libdir}/*.so.*
%{_kf5_sysconfdir}/dbus-1/system.d/*
%{_kf5_libdir}/plugins/kf5/plugins/kauth/
%{_kf5_datadir}/kauth/


%files devel
%doc
%{_kf5_includedir}/*
%{_kf5_libdir}/*.so
%{_kf5_libdir}/cmake/KF5Auth


%changelog
* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
