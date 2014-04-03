Name:           kde5-filesystem
Version:        4.90.3
Release:        1
Summary:        Filesystem and RPM macros for KDE 5 and Plasma Workspaces 2
BuildArch:      noarch

License:        BSD
URL:            http://www.kde.org

Source0:        macros.kde5

%description
Filesystem and RPM macros for KDE 5 and Plasma Workspaces 2

%install
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d/
cp %{_sourcedir}/macros.kde5 %{buildroot}%{_rpmconfigdir}/macros.d

%files
%{_rpmconfigdir}/macros.d/macros.kde5

%changelog
* Thu Apr 03 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.3
- install KDE into /usr prefix for live ISO image

* Thu Feb 13 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.2
- initial version (forked from kf5-filesystem which now points to /usr)

