Name:           uboot-tools
Version:        2010.03
Release:        2%{?dist}
Summary:        U-Boot utilities

Group:          Development/Tools
License:        GPLv2+
URL:            http://www.denx.de/wiki/U-Boot
Source0:        ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}.tar.bz2
Patch0:         u-boot-2010.03-env-makefile.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
This package contains a few U-Boot utilities - mkimage for creating boot images
and fw_printenv/fw_setenv for manipulating the boot environment variables.


%prep
%setup -q -n u-boot-%{version}
%patch0 -p1


%build
make sheevaplug_config

# create files normally created by cross-compiler
touch include/autoconf.mk
touch include/autoconf.mk.dep
touch {cpu/arm926ejs,examples/standalone,tools,tools/env}/.depend

make tools HOSTCC="gcc $RPM_OPT_FLAGS" HOSTSTRIP=/bin/true CROSS_COMPILE=""
make env CC="gcc $RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}

install -p -m 0755 tools/mkimage $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 tools/env/fw_printenv $RPM_BUILD_ROOT%{_bindir}
( cd $RPM_BUILD_ROOT%{_bindir}; ln -sf fw_printenv fw_setenv )

install -p -m 0644 tools/env/fw_env.config $RPM_BUILD_ROOT%{_sysconfdir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README doc/uImage.FIT
%{_bindir}/mkimage
%{_bindir}/fw_printenv
%{_bindir}/fw_setenv
%config(noreplace) %{_sysconfdir}/fw_env.config


%changelog
* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2010.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu May 27 2010 Dan Horák <dan[at]danny.cz> 2010.03-1
- updated to to 2010.03
- applied review feedback - added docs and expanded description
- pass proper CFLAGS to the compiler

* Sat Nov 14 2009 Dan Horák <dan[at]danny.cz> 2009.08-1
- initial Fedora version
