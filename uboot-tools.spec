Name:           uboot-tools
Version:        2012.04.01
Release:        3%{?dist}
Summary:        U-Boot utilities

Group:          Development/Tools
License:        GPLv2+
URL:            http://www.denx.de/wiki/U-Boot
Source0:        ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}.tar.bz2
Patch0:         0001-enable-bootz-support-for-ti-omap-targets.patch
Patch1:         0001-panda-convert-to-uEnv.txt-bootscript.patch
Patch2:         u-boot-fat.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)



# build the tool for manipulation with environment only on arm
%ifarch %{arm}
%global with_env 1
%endif

%description
This package contains a few U-Boot utilities - mkimage for creating boot images
and fw_printenv/fw_setenv for manipulating the boot environment variables.

%ifarch %{arm}
%package     -n uboot-beagle
Summary:     u-boot bootloader binaries for beagleboard
Requires:    uboot-tools

%description -n uboot-beagle
u-boot bootloader binaries for beagleboard

%package     -n uboot-beaglebone
Summary:     u-boot bootloader binaries for beaglebone
Requires:    uboot-tools

%description -n uboot-beaglebone
u-boot bootloader binaries for beaglebone

%package     -n uboot-panda
Summary:     u-boot bootloader binaries for pandaboard
Requires:    uboot-tools

%description -n uboot-panda
u-boot bootloader binaries for pandaboard

%package     -n uboot-origen
Summary:     u-boot bootloader binaries for origenboard
Requires:    uboot-tools

%description -n uboot-origen
u-boot bootloader binaries for origenboard
%endif

%prep
%setup -q -n u-boot-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
mkdir builds

%build
%ifarch %{arm}
make CROSS_COMPILE="" am335x_evm_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p MLO builds/MLO.beaglebone
cp -p u-boot.img builds/u-boot.img.beaglebone
cp -p u-boot.bin builds/u-boot.bin.beaglebone
make distclean

make CROSS_COMPILE="" omap4_panda_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p MLO builds/MLO.panda
cp -p u-boot.img builds/u-boot.img.panda
cp -p u-boot.bin builds/u-boot.bin.panda
make distclean

make CROSS_COMPILE="" origen_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p spl/origen-spl.bin builds/origen-spl.bin.origen
cp -p u-boot.bin builds/u-boot.bin.origen
make distclean
%endif

make tools HOSTCC="gcc $RPM_OPT_FLAGS" HOSTSTRIP=/bin/true CROSS_COMPILE=""

%if 0%{?with_env}
make CROSS_COMPILE="" sheevaplug_config
make env HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
%endif

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
%ifarch %{arm}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-panda/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-beagle/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-beaglebone/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-origen/

for board in beaglebone beagle panda
do
install -p -m 0644 builds/u-boot.bin.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot-$(echo $board)/u-boot.bin
install -p -m 0644 builds/u-boot.img.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot-$(echo $board)/u-boot.img
done
install -p -m 0644 builds/MLO.beagle $RPM_BUILD_ROOT%{_datadir}/uboot-beagle/MLO
install -p -m 0644 builds/MLO.panda $RPM_BUILD_ROOT%{_datadir}/uboot-panda/MLO
install -p -m 0644 builds/origen-spl.bin.origen $RPM_BUILD_ROOT%{_datadir}/uboot-origen/origen-spl.bin
install -p -m 0644 builds/u-boot.bin.origen $RPM_BUILD_ROOT%{_datadir}/uboot-origen/u-boot.bin

%endif

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
%ifarch %{arm}
%files -n uboot-beaglebone
%defattr(-,root,root,-)
%{_datadir}/uboot-beaglebone/

%files -n uboot-beagle
%defattr(-,root,root,-)
%{_datadir}/uboot-beagle/

%files -n uboot-panda
%defattr(-,root,root,-)
%{_datadir}/uboot-panda/

%files -n uboot-origen
%defattr(-,root,root,-)
%{_datadir}/uboot-origen/
%endif

%changelog
* Sat Jul 07 2012 Dennis Gilmore <dennis@ausil.us> - 2012.04.01-3
- build beaglebone uboot images

* Mon Jun 25 2012 Dennis Gilmore <dennis@ausil.us> - 2012.04.01-2
- add patch so the MLO detects fat16 partitions correctly

* Mon May 07 2012 Dennis Gilmore <dennis@ausil.us> - 2012.04.01-1
- update to 2012.04.01 release
- http://lists.denx.de/pipermail/u-boot/2012-April/123011.html

* Tue Apr 24 2012 Dennis Gilmore <dennis@ausil.us> - 2012.04-1
- update to final 2012.04 release

* Thu Apr 19 2012 Dennis Gilmore <dennis@ausil.us> - 2012.04-0.1.rc3
- update to 2012.04-rc3
- build uboot binaries for beagle, panda and origen boards

* Thu Mar 08 2012 Dennis Gilmore <dennis@ausil.us> - 2011.12-1
- update to 2011.12 release

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

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
