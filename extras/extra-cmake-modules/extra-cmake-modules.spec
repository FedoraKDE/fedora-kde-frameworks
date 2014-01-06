%define snapshot 20140104

Name:           extra-cmake-modules
Version:        5.0.0
Release:        0.2.%{snapshot}
Summary:        Additional modules for CMake build system
BuildArch:      noarch

License:        BSD
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git master | \
# gzip -c > %{name}-%{snapshot}.tar.gz
Source0:        %{name}-%{snapshot}.tar.gz

# https://git.reviewboard.kde.org/r/114888/
Patch0:         ecm-fix-doubleslash-in-generated-headers.patch


BuildRequires:  cmake
BuildRequires:  kf5-filesystem

Requires:       cmake
Requires:       kf5-filesystem

%description
Additional modules for CMake build system needed by KDE Frameworks.


%prep
%setup -q

%patch0 -p 1 -b .doubleslash

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} DESTDIR=%{buildroot} -C %{_target_platform}


%install
%make_install -C %{_target_platform}

%files
%doc README
%{_kf5_datadir}/ECM



%changelog
* Mon Jan  6 2014 Daniel Vrátil <dvraitl@redhat.com>
- Include patch to prevent ECMGenerateHeaders to generate "//" in include paths
  (fixes build of solid and kdnssd frameworks)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
