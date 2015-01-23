%global     git_version 7ee83eb
%global     git_date    20150122

Name:       telepathy-logger-qt5
Version:    0.9.0
Release:    1.%{git_date}git%{git_version}%{?dist}
Summary:    Telepathy Logging for Qt 5

License:    LGPLv2+
URL:        https://projects.kde.org/projects/extragear/network/telepathy/telepathy-logger-qt

#Source0:    http://download.kde.org/stable/%{name}/%{version}/src/%{name}-%{version}.tar.bz2
# git archive --format=tar.gz --remote=git://anongit.kde.org/telepathy-logger-qt.git \
#             --prefix=%{name}-%{version}/ --output=%{name}-%{git_version}.tar.gz qt5
Source0:    telepathy-logger-qt-%{git_version}.tar.gz

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  telepathy-qt5-devel >= 0.9
BuildRequires:  python2-devel
BuildRequires:  glib2-devel
BuildRequires:  dbus-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  libxml2-devel
BuildRequires:  telepathy-glib-devel
BuildRequires:  telepathy-logger-devel

%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
# for parent include dir ownership (mostly)
Requires: telepathy-logger-devel%{?_isa}
%description devel
%{summary}.


%prep
%setup -q -n telepathy-logger-qt-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING
%{_libdir}/libtelepathy-logger-qt.so.*

%files devel
%{_includedir}/TelepathyLoggerQt/
%{_libdir}/libtelepathy-logger-qt.so
%{_libdir}/cmake/TelepathyLoggerQt/


%changelog
* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 0.9.0-1.20150122git7ee83eb
- Fork telepathy-logger-qt

