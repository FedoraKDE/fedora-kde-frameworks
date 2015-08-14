%global fontname oxygen
%global fontconf 61-%{fontname}

Name:           %{fontname}-fonts
Version:        5.3.95
Release:        1%{?dist}
Summary:        Oxygen fonts created by the KDE Community

# See LICENSE-GPL+FE for details about the exception
License:        OFL or GPLv3 with exceptions
URL:            http://www.kde.org
Source0:        http://download.kde.org/stable/plasma/%{version}/%{name}-%{version}.tar.xz
Source1:        %{fontconf}-sans.conf
Source2:        %{fontconf}-mono.conf

# essentially a noarch pkg here, no real -debuginfo needed (#1192729)
%define debug_package   %{nil}

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  fontforge
BuildRequires:  fontpackages-devel
Requires:       fontpackages-filesystem

# main (meta)package, largely for upgrade path
Requires: %{fontname}-mono-fonts = %{version}-%{release}
Requires: %{fontname}-sans-fonts = %{version}-%{release}

%description
Oxygen fonts created by the KDE Community.

%package common
Summary:        Common files for Oxygen font
Requires:       fontpackages-filesystem
BuildArch:      noarch
%description    common
%{summary}.

%package -n %{fontname}-mono-fonts
Summary:        Oxygen Monospaced Font
Requires:       %{name}-common = %{version}-%{release}
BuildArch:      noarch
%description    -n %{fontname}-mono-fonts
%{summary}.

%package -n %{fontname}-sans-fonts
Summary:        Oxygen Sans-Serif Font
Requires:       %{name}-common = %{version}-%{release}
BuildArch:      noarch
%description    -n %{fontname}-sans-fonts
%{summary}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake} .. %{?fontforge} -DOXYGEN_FONT_INSTALL_DIR=%{_fontdir}
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-sans.conf
install -m 0644 -p %{SOURCE2} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-mono.conf

ln -s %{_fontconfig_templatedir}/%{fontconf}-sans.conf \
      %{buildroot}/%{_fontconfig_confdir}/%{fontconf}-sans.conf
ln -s %{_fontconfig_templatedir}/%{fontconf}-mono.conf \
      %{buildroot}/%{_fontconfig_confdir}/%{fontconf}-mono.conf

%_font_pkg -n sans -f %{fontconf}-sans.conf Oxygen-Sans*.ttf
%_font_pkg -n mono -f %{fontconf}-mono.conf OxygenMono*.ttf

%files
# empty metapackage

%files common
%doc COPYING-GPL+FE.txt COPYING-OFL GPL.txt README.md

%files devel
%{_libdir}/cmake/OxygenFont/

%changelog
* Thu Aug 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-1
- Plasma 5.3.95

* Thu Jun 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.2-1
- Plasma 5.3.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma 5.3.1

* Mon Apr 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- Plasma 5.3.0

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Mon Mar 09 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Sat Feb 14 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-3
- oxygen-fonts-debuginfo-5.2.0-2 is empty (#1192729)

* Fri Feb 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-2
- Fix noarch bug: -devel installs into %{_libdir}, which is arch-dependent

* Thu Jan 29 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- oxygen-font 5.2.0, remove the fontforge rawhide workaround

* Mon Oct 20 2014 Rex Dieter <rdieter@fedoraproject.org> 5.1.0-2
- provide oxygen-fonts (meta)package, fixes upgrade path (#1154369)

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- oxygen-font 5.1.0

* Tue Sep 30 2014 Daniel Vrátil <dvratil@redhat.com> - 0.4.2-5
- Fix incorrect use of macros in Requires

* Mon Sep 29 2014 Parag Nemade <pnemade@redhat.com> - 0.4.2-4
- Use correct typefaces

* Thu Sep 25 2014 Daniel Vrátil <dvratil@redhat.com> - 0.4.2-3
- Fix fontconfig.files (RHBZ#1146505)
- Create subpackages for sans and mono fonts

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 0.4.2-2
- oxygen-fonts 0.4.2

* Wed Aug 20 2014 Daniel Vrátil <dvratil@redhat.com> - 0.4.0-2
- drop dependency on KF5

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 0.4.0-1
- oxygen-fonts 0.4.0

* Sun Jun 29 2014 Daniel Vrátil <dvratil@redhat.com> - 0.3.95-2
- fix license
- fix rpmlint warnings

* Thu Apr 03 2014 Daniel Vrátil <dvratil@redhat.com> - 0.3.95-1
- Initial vrsion
