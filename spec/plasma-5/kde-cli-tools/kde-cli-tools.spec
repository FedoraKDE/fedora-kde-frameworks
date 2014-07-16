Name:           kde-cli-tools
Version:        5.0.0
Release:        1%{?dist}
Summary:        Tools based on KDE Frameworks 5 to better interact with the system.

License:        GPLv2+
URL:            http://www.kde.org

Source0:        http://download.kde.org/stable/plasma/%{version}/kde-cli-tools-%{version}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kf5-rpm-macros

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kdesu-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kwindowsystem-devel

Requires:       kf5-filesystem

# kde-cli-tools contains utilities that were part of kde-runtime in the past
Obsoletes:      kde-runtime <= 4.60.0-1

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q


%build

# Fix "no rule to make target '../po/XX/PO_FILES', neede by 'po/XX/PO_FILES.gmo'"
sed -e "s/PO_FILES //" -i po/*/CMakeLists.txt

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}
%find_lang kdeclitools_qt --with-qt --all-name

%files -f kdeclitools_qt.lang
%{_bindir}/kcmshell5
%{_bindir}/kde-open5
%{_bindir}/kdecp5
%{_bindir}/kdemv5
%{_bindir}/keditfiletype5
%{_bindir}/kioclient5
%{_bindir}/kmimetypefinder5
%{_bindir}/kstart5
%{_bindir}/ksvgtopng5
%{_bindir}/ktraderclient5
%{_kf5_libdir}/libkdeinit5_kcmshell5.so
%{_kf5_qtplugindir}/kcm_filetypes.so
%{_libexecdir}/kdeeject
%{_libexecdir}/kdesu
%{_datadir}/doc/HTML/en/kdesu
%{_kf5_datadir}/kservices5/filetypes.desktop
%{_mandir}/man1/kdesu.1.gz

%changelog
* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Mon May 19 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1.20140519git60d6c72
- initial version
