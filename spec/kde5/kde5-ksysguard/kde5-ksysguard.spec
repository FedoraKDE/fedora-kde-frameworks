%define git_commit f7a2bbe
%define base_name ksysguard

Name:           kde5-%{base_name}
Version:        4.96.0
Release:        1.20140515git%{git_commit}%{?_dist}
Summary:        KDE Process Management application

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git frameworks | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        %{base_name}-%{git_commit}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel

BuildRequires:  kde5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-umbrella
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-knewstuff-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-ksysguard-devel

BuildRequires:  lm_sensors-devel

Requires:       kde5-filesystem

Conflicts:      kde-runtime
Provides:       ksysgaurd = %{version}-%{release}

%description
%{summary}.

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

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING COPYING.DOC README
%{_kde5_bindir}/ksysguard
%{_kde5_bindir}/ksysguardd
%{_kde5_libdir}/libkdeinit5_ksysguard.so
%{_kde5_datadir}/ksysguard
%{_kde5_sysconfdir}/xdg/ksysguard.knsrc
%{_kde5_sysconfdir}/ksysguarddrc
%{_datadir}/applications/ksysguard.desktop
%{_datadir}/doc/HTML/en/ksysguard
%{_datadir}/icons/oxygen/*/actions/*.png
%{_datadir}/knotifications5/ksysguard.notifyrc

%changelog
* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140515gitf7a2bbe
- Intial snapshot
