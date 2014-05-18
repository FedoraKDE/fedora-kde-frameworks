%define git_commit 1b86b1a
%define base_name kmenuedit

Name:           kde5-%{base_name}
Version:        4.96.0
Release:        1.20140524git%{git_commit}%{?dist}
Summary:        KDE menu editor

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
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-kdelibs4support-devel

Requires:       kde5-filesystem

Conflicts:      kde-runtime
Provides:       kmenuedit = %{version}-%{release}

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
%doc COPYING COPYING.DOC
%{_kde5_bindir}/kmenuedit
%{_kde5_libdir}/libkdeinit5_kmenuedit.so
%{_kde5_datadir}/kmenuedit
%{_datadir}/applications/kmenuedit.desktop
%{_datadir}/doc/HTML/en/kmenuedit
%{_datadir}/icons/hicolor/*/actions/kmenuedit.png


%changelog
* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140514git1b86b1a
- Intial snapshot
