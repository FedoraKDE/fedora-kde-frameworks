%define git_commit f60a0db
%define base_name plasma-workspace-artwork

Name:           kde5-%{base_name}
Version:        4.90.0
Release:        1.20140519git%{git_commit}%{?dist}
Summary:        Plasma Workspace artwork

License:        LGPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/scratch/mart/plasma-workspace-artwork.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        %{base_name}-%{git_commit}.tar.xz

BuildRequires:  qt5-qtbase-devel

BuildRequires:  kde5-rpm-macros
BuildRequires:  extra-cmake-modules

Requires:       kde5-filesystem

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

%files
%doc LICENSE
%{_datadir}/wallpapers/Next


%changelog
* Mon May 19 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140519gitf60a0db
- Intial snapshot
