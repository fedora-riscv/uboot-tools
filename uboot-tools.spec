Name:           uboot-tools
Version:        2011.03
Release:        1%{?dist}
Summary:        U-Boot utilities

Group:          Development/Tools
License:        GPLv2+
URL:            http://www.denx.de/wiki/U-Boot
Source0:        ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# build the tool for manipulation with environment only on arm
%ifarch %{arm}
%global with_env 1
%endif


%description
This package contains a few U-Boot utilities - mkimage for creating boot images
and fw_printenv/fw_setenv for manipulating the boot environment variables.


%prep
%setup -q -n u-boot-%{version}


%build
make sheevaplug_config

# create files normally created by cross-compiler
touch include/autoconf.mk
touch include/autoconf.mk.dep
mkdir include/generated
touch include/generated/generic-asm-offsets.h
touch lib/asm-offsets.s
touch {arch/arm/cpu/arm926ejs,examples/standalone,tools,tools/env}/.depend

make tools HOSTCC="gcc $RPM_OPT_FLAGS" HOSTSTRIP=/bin/true CROSS_COMPILE=""
%if 0%{?with_env}
make env HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
%endif


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1

install -p -m 0755 tools/mkimage $RPM_BUILD_ROOT%{_bindir}
install -p -m 0644 doc/mkimage.1 $RPM_BUILD_ROOT%{_mandir}/man1

%if 0%{?with_env}
install -p -m 0755 tools/env/fw_printenv $RPM_BUILD_ROOT%{_bindir}
( cd $RPM_BUILD_ROOT%{_bindir}; ln -sf fw_printenv fw_setenv )

install -p -m 0644 tools/env/fw_env.config $RPM_BUILD_ROOT%{_sysconfdir}
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README doc/README.imximage doc/README.kwbimage doc/uImage.FIT
%{_bindir}/mkimage
%{_mandir}/man1/mkimage.1*
%if 0%{?with_env}
%{_bindir}/fw_printenv
%{_bindir}/fw_setenv
%config(noreplace) %{_sysconfdir}/fw_env.config
%endif


%changelog
* Thu Apr 14 2011 Dan Horák <dan[at]danny.cz> - 2011.03-1
- updated to to 2011.03
- build the tool for manipulation with environment only on arm

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2010.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu May 27 2010 Dan Horák <dan[at]danny.cz> 2010.03-1
- updated to to 2010.03
- applied review feedback - added docs and expanded description
- pass proper CFLAGS to the compiler

* Sat Nov 14 2009 Dan Horák <dan[at]danny.cz> 2009.08-1
- initial Fedora version
