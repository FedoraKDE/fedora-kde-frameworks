%define git_commit 6bfae0d
%define base_name khelpcenter

Name:           kde5-%{base_name}
Version:        4.90.1
Release:        1.20140524git%{git_commit}%{?dist}
Summary:        Application to show KDE Application's documentation

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git frameworks | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        %{base_name}-%{git_commit}.tar.xz

Patch0:         khelpcenter-fix-build.patch

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel

BuildRequires:  kde5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-umbrella
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kinit-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-khtml-devel
BuildRequires:  kf5-kdelibs4support-devel

Requires:       kde5-filesystem

Conflicts:      kde-runtime
Provides:       khelpcenter = %{version}-%{release}

%description
An advanced editor component which is used in numerous KDE applications
requiring a text editing component.

%prep
%setup -q -n %{base_name}-%{version}

%patch0 -p1 -b .build

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
%doc README.htdig README.metadata COPYING
%{_kde5_bindir}/khelpcenter
%{_kde5_libexecdir}/khc_indexbuilder
%{_kde5_libexecdir}/khc_htdig.pl
%{_kde5_libexecdir}/khc_htsearch.pl
%{_kde5_libexecdir}/khc_mansearch.pl
%{_kde5_libexecdir}/khc_docbookdig.pl
%{_kde5_libdir}/libkdeinit5_khelpcenter.so
%{_kde5_datadir}/khelpcenter
%{_datadir}/applications/Help.desktop
%{_datadir}/config.kcfg/khelpcenter.kcfg
%{_datadir}/kservices5/khelpcenter.desktop
%{_datadir}/dbus-1/interfaces/org.kde.khelpcenter.kcmhelpcenter.xml
%{_datadir}/doc/HTML/en/khelpcenter
%{_datadir}/doc/HTML/en/fundamentals
%{_datadir}/doc/HTML/en/onlinehelp

%changelog
* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140514git6bfae0d
- Intial snapshot
