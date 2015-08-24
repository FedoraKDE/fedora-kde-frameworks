%global framework akonadi

Name:           kf5-%{framework}
Version:        15.08.0
Release:        1%{?dist}
Summary:        The Akonadi client libraries

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/kdepimlibs

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/applications/%{version}/src/%{framework}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qttools-static

BuildRequires:  boost-devel
BuildRequires:  cyrus-sasl-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel

BuildRequires:  kf5-kitemviews-devel >= 5.12
BuildRequires:  kf5-kio-devel >= 5.12
BuildRequires:  kf5-kconfig-devel >= 5.12
BuildRequires:  kf5-solid-devel >= 5.12
BuildRequires:  kf5-kdelibs4support-devel >= 5.12
BuildRequires:  kf5-kcompletion-devel >= 5.12
BuildRequires:  kf5-kcodecs-devel >= 5.12
BuildRequires:  kf5-ki18n-devel >= 5.12
BuildRequires:  kf5-kdoctools-devel >= 5.12
BuildRequires:  phonon-qt5-devel

BuildRequires:  kf5-akonadi-server-devel >= 15.08

BuildRequires:  kf5-kcontacts-devel >= 15.08
BuildRequires:  kf5-kcalendarcore-devel >= 15.08
BuildRequires:  kf5-kmime-devel >= 15.08
BuildRequires:  kf5-kldap-devel >= 15.08
BuildRequires:  kf5-kmbox-devel >= 15.08

# There is a hardcoded strict version dependency between server and client
# libraries with runtime check
Requires:       kf5-akonadi-server = %{version}

Obsoletes:      kdepimlibs%{?_isa} < 15.08.0
Conflicts:      kdepimlibs%{?_isa} < 15.08.0
Conflicts:      akonadi%{?_isa} < 15.08.0

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel
Requires:       kf5-kcompletion-devel
Requires:       kf5-kjobwidgets-devel
Requires:       kf5-kservice-devel
Requires:       kf5-solid-devel
Requires:       kf5-kxmlgui-devel
Requires:       kf5-kitemmodels-devel
Requires:       kf5-kdelibs4support-devel
Requires:       kf5-akonadi-server-devel
Requires:       boost-devel
Obsoletes:      kdepimlibs-devel%{?_isa} < 15.08.0
Conflicts:      kdepimlibs-devel%{?_isa} < 15.08.0
Conflicts:      akonadi-devel%{?_isa} < 15.08.0
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        contact
Summary:        The Akonadi Contact Library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      kdepimlibs%{?_isa} < 15.08.0
Conflicts:      kdepimlibs%{?_isa} < 15.08.0
%description    contact
%{summary}.

%package        contact-devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-contact%{?_isa} = %{version}-%{release}
Requires:       kf5-akonadi-devel
Requires:       kf5-kcontacts-devel
Requires:       kf5-kcalendarcore-devel
Obsoletes:      kdepimlibs-devel%{?_isa} < 15.08.0
Conflicts:      kdepimlibs-devel%{?_isa} < 15.08.0
Conflicts:      akonadi-devel%{?_isa} < 15.08.0
%description    contact-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        mime
Summary:        The Akonadi Mime Library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      kdepimlibs%{?_isa} < 15.08.0
Conflicts:      kdepimlibs%{?_isa} < 15.08.0
%description    mime
%{summary}.

%package        mime-devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-contact%{?_isa} = %{version}-%{release}
Requires:       kf5-akonadi-devel
Obsoletes:      kdepimlibs-devel%{?_isa} < 15.08.0
Conflicts:      kdepimlibs-devel%{?_isa} < 15.08.0
Conflicts:      akonadi-devel%{?_isa} < 15.08.0
%description    mime-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        notes
Summary:        The Akonadi Notes Library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      kdepimlibs%{?_isa} < 15.08.0
Conflicts:      kdepimlibs%{?_isa} < 15.08.0
%description    notes
%{summary}.

%package        notes-devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-contact%{?_isa} = %{version}-%{release}
Requires:       kf5-akonadi-devel
Requires:       kf5-kdelibs4support-devel
Requires:       kf5-kmime-devel
Obsoletes:      kdepimlibs-devel%{?_isa} < 15.08.0
Conflicts:      kdepimlibs-devel%{?_isa} < 15.08.0
Conflicts:      akonadi-devel%{?_isa} < 15.08.0
%description    notes-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        socialutils
Summary:        The Akonadi Social Utils Library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      kdepimlibs%{?_isa} < 15.08.0
Conflicts:      kdepimlibs%{?_isa} < 15.08.0
%description    socialutils
%{summary}.

%package        socialutils-devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-contact%{?_isa} = %{version}-%{release}
Requires:       kf5-akonadi-devel
Obsoletes:      kdepimlibs-devel%{?_isa} < 15.08.0
Conflicts:      kdepimlibs-devel%{?_isa} < 15.08.0
Conflicts:      akonadi-devel%{?_isa} < 15.08.0
%description    socialutils-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%{_kf5_bindir}/akonadiselftest
%{_kf5_libdir}/libKF5AkonadiCore.so.*
%{_kf5_libdir}/libKF5AkonadiAgentBase.so.*
%{_kf5_libdir}/libKF5AkonadiWidgets.so.*
%{_kf5_libdir}/libKF5AkonadiXml.so.*
%{_kf5_datadir}/config.kcfg/*.kcfg
%{_kf5_datadir}/kf5/akonadi/akonadi-xml.xsd
%{_kf5_datadir}/kf5/akonadi/kcfg2dbus.xsl

%{_sysconfdir}/xdg/kdepimlibs-kioslave.categories
%{_kf5_plugindir}/kio/*.so
%{_kf5_datadir}/kservices5/*.protocol

%{_kf5_datadir}/doc/HTML/en/kioslave5/*

%files devel
%{_kf5_bindir}/akonadi2xml

%{_kf5_includedir}/akonadi_version.h
%{_kf5_libdir}/cmake/KF5Akonadi

%{_kf5_libdir}/libKF5AkonadiCore.so
%{_kf5_archdatadir}/mkspecs/modules/qt_AkonadiCore.pri
%{_kf5_includedir}/AkonadiCore

%{_kf5_libdir}/libKF5AkonadiAgentBase.so
%{_kf5_archdatadir}/mkspecs/modules/qt_AkonadiAgentBase.pri
%{_kf5_includedir}/AkonadiAgentBase

%{_kf5_libdir}/libKF5AkonadiWidgets.so
%{_kf5_archdatadir}/mkspecs/modules/qt_AkonadiWidgets.pri
%{_kf5_includedir}/AkonadiWidgets
%{_kf5_qtplugindir}/designer/akonadi5widgets.so

%{_kf5_libdir}/libKF5AkonadiXml.so
%{_kf5_archdatadir}/mkspecs/modules/qt_AkonadiXml.pri
%{_kf5_includedir}/AkonadiXml


%post contact -p /sbin/ldconfig
%postun contact -p /sbin/ldconfig

%files contact
%{_kf5_libdir}/libKF5AkonadiContact.so.*
%{_kf5_qtplugindir}/kcm_akonadicontact_actions.so
%{_kf5_datadir}/kservices5/akonadicontact_actions.desktop
%{_kf5_datadir}/kf5/akonadi/contact
%{_kf5_datadir}/icons/oxygen/16x16/apps/*.png
%{_kf5_datadir}/kservices5/akonadi/contact/*.desktop
%{_kf5_datadir}/kservicetypes5/kaddressbookimprotocol.desktop

%files contact-devel
%{_kf5_libdir}/cmake/KF5AkonadiContact
%{_kf5_libdir}/libKF5AkonadiContact.so
%{_kf5_archdatadir}/mkspecs/modules/qt_AkonadiContact.pri
%{_kf5_includedir}/Akonadi/Contact
%{_kf5_includedir}/akonadi/contact
%{_kf5_includedir}/akonadi-contact_version.h

%post mime -p /sbin/ldconfig
%postun mime
/sbin/ldconfig ||:
if [ $1 -eq 0 ] ; then
update-mime-database %{_kf5_datadir}/mime &> /dev/null
fi

%posttrans mime
update-mime-database %{_kf5_datadir}/mime >& /dev/null

%files mime
%{_kf5_libdir}/libKF5AkonadiMime.so.*
# Despite the name, this is provided by the AkonadiMime library
%{_kf5_datadir}/mime/packages/x-vnd.kde.contactgroup.xml

%files mime-devel
%{_kf5_libdir}/cmake/KF5AkonadiMime
%{_kf5_libdir}/libKF5AkonadiMime.so
%{_kf5_archdatadir}/mkspecs/modules/qt_AkonadiMime.pri
%{_kf5_includedir}/Akonadi/KMime
%{_kf5_includedir}/akonadi/kmime
%{_kf5_includedir}/akonadi-mime_version.h

%post notes -p /sbin/ldconfig
%postun notes -p /sbin/ldconfig

%files notes
%{_kf5_libdir}/libKF5AkonadiNotes.so.*

%files notes-devel
%{_kf5_libdir}/cmake/KF5AkonadiNotes
%{_kf5_libdir}/libKF5AkonadiNotes.so
%{_kf5_archdatadir}/mkspecs/modules/qt_AkonadiNotes.pri
%{_kf5_includedir}/Akonadi/Notes
%{_kf5_includedir}/akonadi/notes
%{_kf5_includedir}/akonadi-notes_version.h

%post socialutils -p /sbin/ldconfig
%postun socialutils
/sbin/ldconfig ||:
if [ $1 -eq 0 ] ; then
update-mime-database %{_kf5_datadir}/mime &> /dev/null
fi

%posttrans socialutils
update-mime-database %{_kf5_datadir}/mime >& /dev/null

%files socialutils
%{_kf5_libdir}/libKF5AkonadiSocialUtils.so.*
%{_kf5_qtplugindir}/akonadi_serializer_socialfeeditem.so
%{_kf5_datadir}/akonadi/plugins/serializer/akonadi_serializer_socialfeeditem.desktop
%{_kf5_datadir}/mime/packages/x-vnd.akonadi5.socialfeeditem.xml

%files socialutils-devel
%{_kf5_libdir}/cmake/KF5AkonadiSocialUtils
%{_kf5_libdir}/libKF5AkonadiSocialUtils.so
%{_kf5_archdatadir}/mkspecs/modules/qt_AkonadiSocialUtils.pri
%{_kf5_includedir}/Akonadi/SocialUtils
%{_kf5_includedir}/akonadi/socialutils
%{_kf5_includedir}/akonadi-socialutils_version.h


%changelog
* Mon Aug 24 2015 Daniel Vrátil <dvratil@redhat.com> - 15.08.0-1
- Initial version
