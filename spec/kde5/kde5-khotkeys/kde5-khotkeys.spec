%define git_commit e1c386a
%define base_name khotkeys

Name:           kde5-%{base_name}
Version:        4.96.0
Release:        1.20140524git%{git_commit}%{?dist}
Summary:        Application to show KDE Application's documentation

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git frameworks | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        %{base_name}-%{git_commit}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kde5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-umbrella
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kdoctools-devel

BuildRequires:  kde5-plasma-workspace-devel

BuildRequires:  libX11-devel

BuildRequires:  chrpath

Requires:       kde5-filesystem

Conflicts:      kde-runtime
Provides:       khotkeys = %{version}-%{release}

%description
An advanced editor component which is used in numerous KDE applications
requiring a text editing component.

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
%{cmake_kde5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

chrpath --delete %{buildroot}/%{_kde5_plugindir}/kded_khotkeys.so
chrpath --delete %{buildroot}/%{_kde5_plugindir}/kcm_hotkeys.so
chrpath --delete %{buildroot}/%{_kde5_libdir}/libkhotkeysprivate.so.4.96.0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_kde5_libdir}/libkhotkeysprivate.so.*
%{_kde5_plugindir}/*.so
%{_kde5_datadir}/khotkeys
%{_datadir}/kservices5/kded/*.desktop
%{_datadir}/kservices5/khotkeys.desktop
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/doc/HTML/en/kcontrol/khotkeys

%files devel
%{_libdir}/cmake/KHotKeysDBusInterface

%changelog
* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140514gite1c386a
- Intial snapshot
