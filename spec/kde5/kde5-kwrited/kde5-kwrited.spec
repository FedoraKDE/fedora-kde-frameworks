%define git_commit 11b832c
%define base_name kwrited

Name:           kde5-%{base_name}
Version:        4.96.0
Release:        1.20140515git%{git_commit}%{?dist}
Summary:        KDE's kwrited daemon

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
BuildRequires:  kf5-kpty-devel
BuildRequires:  kf5-kdelibs4support-devel

Requires:       kde5-filesystem

Conflicts:      kde-runtime
Provides:       kwrited = %{version}-%{release}

%description
An advanced editor component which is used in numerous KDE applications
requiring a text editing component.

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
%doc COPYING
%{_kde5_bindir}/kwrited
%{_kde5_sysconfdir}/xdg/autostart/kwrited-autostart.desktop
%{_datadir}/knotifications5/kwrited.notifyrc


%changelog
* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140515gitc11b832c
- Intial snapshot
