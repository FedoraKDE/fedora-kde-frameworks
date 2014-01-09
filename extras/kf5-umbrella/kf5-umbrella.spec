%define snapshot  20140109

Name:           kf5-umbrella
Version:        5.0.0
Release:        0.1.%{snapshot}git
Summary:        CMake configuration for KDE Frameworks 5

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{snapshot}/ \
#             --remote=git://anongit.kde.org/kf5umbrella.git master | \
# gzip -c > %{name}-%{snapshot}.tar.gz
Source0:        %{name}-%{snapshot}.tar.gz

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

%description
Provides CMake configuration file for KDE Frameworks 5


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

%files
%doc README.md
%{_kf5_libdir}/cmake/KF5


%changelog
* Thu Jan  9 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version

