%define snapshot  20140104

Name:           kf5-kxmlgui
Version:        5.0.0
Release:        0.1.%{snapshot}git
Summary:        KDE Frameworks tier 3 solution for generating UI

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{snapshot}/ \
#             --remote=git://anongit.kde.org/%{name}-framework.git master | \
# gzip -c > %{name}-framework-%{snapshot}.tar.gz
Source0:        %{name}-%{snapshot}.tar.gz

BuildRequires:  libX11-devel
BuildRequires:  libattica-devel

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kwindowsystem-devel


%description
KDE Frameworks tier 3 solution for generating UI


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
%doc COPYING COPYING.LIB README.md
%{_kf5_libdir}/*.so.*

%files devel
%doc
%{_kf5_includedir}/*
%{_kf5_libdir}/*.so
%{_kf5_libdir}/cmake/KF5XmlGui


%changelog
* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
