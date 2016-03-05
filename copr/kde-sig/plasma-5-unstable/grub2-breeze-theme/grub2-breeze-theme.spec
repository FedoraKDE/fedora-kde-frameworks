Name:           grub2-breeze-theme
Version:        5.5.95
Release:        1%{?dist}
Summary:        Breeze theme for GRUB
BuildArch:      noarch

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/%{name}

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/breeze-grub-%{version}.tar.xz

Requires:       grub2

%description
%{summary}.

%prep
%autosetup -n breeze-grub-%{version} -p1

%build

%install
install -d breeze %{buildroot}/boot/grub2/themes/breeze

%files
%license COPYING
/boot/grub2/themes/breeze/

%changelog
* Sat Mar 05 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.95-1
- Initial version

