%define snapshot 20140104

Name:           kf5-filesystem
Version:        5.0.0
Release:        0.2.%{snapshot}
Summary:        Filesystem and RPM macros for KDE Frameworks 5
BuildArch:      noarch

License:        BSD
URL:            http://www.kde.org

Source0:        macros.kf5

%description
Filesystem and RPM macros for KDE Frameworks 5

%install
mkdir -p %{buildroot}/opt/kf5/{,bin,share,doc,include,%{_lib},libexec,qt5/plugins,etc}
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d/
cp %{_sourcedir}/macros.kf5 %{buildroot}%{_rpmconfigdir}/macros.d

%files
%{_rpmconfigdir}/macros.d/macros.kf5
/opt/kf5

%changelog
* Mon Jan  6 2014 Daniel Vrátil <dvratil@redhat.com>
- alter XDG_DATA_DIRS in cmake_kf5 RPM macro

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version

