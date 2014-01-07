%define snapshot  20140104

Name:           kf5-kjsembed
Version:        5.0.0
Release:        0.1.%{snapshot}git
Summary:        KDE Frameworks tier 3 addon with JS scripting engine

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{snapshot}/ \
#             --remote=git://anongit.kde.org/%{name}-framework.git master | \
# gzip -c > %{name}-framework-%{snapshot}.tar.gz
Source0:        %{name}-%{snapshot}.tar.gz

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qttools-static
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kdoctools-devel

%description
KDE Frameworks tier 3 addon with JS scripting engine


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
%{_kf5_bindir}/kjscmd
%{_kf5_bindir}/kjsconsole
%{_kf5_libdir}/*.so.*
%{_kf5_datadir}/man/man1/kjscmd.1


%files devel
%doc
%{_kf5_libdir}/*.so
%{_kf5_libdir}/cmake/KF5JsEmbed


%changelog
* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
