Name:           grub2-breeze-theme
Version:        5.6.2
Release:        1%{?dist}
Summary:        Breeze theme for GRUB
BuildArch:      noarch

License:        GPLv3
URL:            https://projects.kde.org/projects/kde/workspace/breeze-grub

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
%global _grubthemedir /boot/grub2/themes
mkdir -p %{buildroot}%{_grubthemedir}
cp -r breeze %{buildroot}%{_grubthemedir}


%files
%license COPYING
%{_grubthemedir}/breeze


%changelog
* Tue Apr 05 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.6.2-1
- Update to 5.6.2
- Fix license

* Sun Mar 20 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.6.0-1
- Plasma 5.6.0

* Sun Mar 06 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.95-3
- Fix install
- disable incompatible theme options

* Sat Mar 05 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.95-1
- Initial version

