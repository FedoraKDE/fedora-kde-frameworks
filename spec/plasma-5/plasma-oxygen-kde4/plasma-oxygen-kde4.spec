%global         base_name oxygen

Name:           plasma-%{base_name}-kde4
Version:        5.1.0.1
Release:        1%{?dist}
Summary:        KDE 4 version of Plasma 5 Oxgen
License:        GPLv2+
URL:            http://www.kde.org
Source0:        http://download.kde.org/stable/plasma/%{version}/%{base_name}-%{version}.tar.xz

BuildRequires:  kdelibs4-devel
BuildRequires:  kde-workspace-devel
BuildRequires:  libxcb-devel
Requires:       plasma-%{base_name}-common = %{version}-%{release}

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{base_name}-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} -DUSE_KDE4=TRUE ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_kde4_libdir}/liboxygenstyle.so.*
%{_kde4_libdir}/liboxygenstyleconfig.so.*
%{_kde4_libdir}/kde4/kstyle_oxygen_config.so
%{_kde4_libdir}/kde4/plugins/styles/oxygen.so
%{_kde4_appsdir}/kstyle/themes/oxygen.themerc
%{_kde4_appsdir}/kwin/oxygenclient.desktop
%{_kde4_bindir}/oxygen-demo

%files devel
%{_kde4_libdir}/*.so
%{_kde4_libdir}/kde4/*.so

%changelog
* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

