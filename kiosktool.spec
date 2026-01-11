%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg kiosktool
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		1.0
Release:		%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:		Tool to configure the TDE kiosk framework
Group:			Applications/Multimedia
URL:			http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/settings/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DWITH_ALL_OPTIONS=ON
BuildOption:    -DBUILD_ALL=ON
BuildOption:    -DBUILD_DOC=ON
BuildOption:    -DBUILD_TRANSLATIONS=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	gettext

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig

# ACL support
BuildRequires:  pkgconfig(libacl)

# IDN support
BuildRequires:	pkgconfig(libidn)

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


%description
A Point&Click tool for system administrators to enable 
TDE's KIOSK features or otherwise preconfigure TDE for 
groups of users.


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"


%install -a
%find_lang %{tde_pkg}

%__mkdir_p "%{?buildroot}%{_sysconfdir}/trinity"
cat <<EOF >"%{?buildroot}%{_sysconfdir}/trinity/kiosktoolrc"
[General]
GroupBlacklist=bin,daemon,sys,tty,disk,lp,www,kmem,wheel,mail,news,uucp,shadow,utmp,at,xok,named,ftp,postfix,maildrop,man,sshd,distcc,nobody,nogroup
EOF

# Updates applications categories for openSUSE
echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_prefix}/share/applications/tde/%{tde_pkg}.desktop"
%if 0%{?suse_version}
%suse_update_desktop_file "%{?buildroot}%{tde_prefix}/share/applications/tde/%{tde_pkg}.desktop" System SystemSetup
%endif


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc ChangeLog COPYING README.md TODO
%{tde_prefix}/bin/kiosktool
%{tde_prefix}/bin/kiosktool-tdedirs
%{tde_prefix}/share/applications/tde/kiosktool.desktop
%{tde_prefix}/share/apps/kiosktool/
%lang(da) %{tde_prefix}/share/doc/tde/HTML/da/kiosktool/
%lang(en) %{tde_prefix}/share/doc/tde/HTML/en/kiosktool/
%lang(it) %{tde_prefix}/share/doc/tde/HTML/it/kiosktool/
%lang(nl) %{tde_prefix}/share/doc/tde/HTML/nl/kiosktool/
%lang(pt) %{tde_prefix}/share/doc/tde/HTML/pt/kiosktool/
%lang(sv) %{tde_prefix}/share/doc/tde/HTML/sv/kiosktool/
%{tde_prefix}/share/icons/crystalsvg/*/apps/kiosktool.png
%config(noreplace) %{_sysconfdir}/trinity/kiosktoolrc
%{tde_prefix}/share/man/man1/*.1*

