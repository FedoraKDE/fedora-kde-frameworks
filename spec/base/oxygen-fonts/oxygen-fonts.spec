%global fontname oxygen
%global fontconf oxygen-fontconfig.conf

Name:           oxygen-fonts
Version:        0.3.95
Release:        2%{?dist}
Summary:        Oxygen fonts created by the KDE Community

# See LICENSE-GPL+FE for details about the exception
License:        OFL or GPLv3 with exceptions
URL:            http://www.kde.org
Source0:        http://download.kde.org/unstable/plasma/4.95.0/%{name}-%{version}.tar.xz
Source1:        %{fontname}-fontconfig.conf

BuildArch:      noarch
BuildRequires:  cmake
BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  fontforge
BuildRequires:  fontpackages-devel
Requires:       fontpackages-filesystem

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} .. -DOXYGEN_FONT_INSTALL_DIR=%{_fontdir}
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}
install -m 0644 -p %{SOURCE1} \
         %{buildroot}%{_fontconfig_templatedir}/%{fontconf}
ln -s %{_fontconfig_templatedir}/%{fontconf} \
      %{buildroot}%{_fontconfig_confdir}/%{fontconf}

%clean
rm -fr %{buildroot}

%_font_pkg -f %{fontconf} *.ttf
%doc COPYING-GPL+FE.txt COPYING-OFL GPL.txt README.md

%files devel
%{_kf5_libdir}/cmake/OxygenFont

%changelog
* Sun Jun 29 2014 Daniel Vrátil <dvratil@redhat.com> - 0.3.95-2
- fix license
- fix rpmlint warnings

* Thu Apr 03 2014 Daniel Vrátil <dvratil@redhat.com> - 0.3.95-1
- Initial vrsion
