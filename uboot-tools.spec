%global candidate rc4

Name:           uboot-tools
Version:        2013.10
Release:        0.5%{?candidate:.%{candidate}}%{?dist}
Summary:        U-Boot utilities

Group:          Development/Tools
License:        GPLv2+
URL:            http://www.denx.de/wiki/U-Boot
Source0:        ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}%{?candidate:-%{candidate}}.tar.bz2
Source1:        uEnv.txt.beagle
Source2:        uEnv.txt.beaglebone
Source3:        uEnv.txt.beagle_xm
Source4:        uEnv.txt.panda
Source5:        uEnv.txt.panda_a4
Source6:        uEnv.txt.panda_es
Source7:        uEnv.txt.uevm
Patch1:         u-boot-fat.patch
Patch3:         mlo-ext.patch
Patch4:         exynos-ext.patch

Patch10:        0001-add-distro-default-commands-and-config-options.patch
Patch11:        0002-add-option-to-include-generic-distro-config.patch
Patch12:        0003-set-omap4-boards-to-use-the-generic-distro-support.patch
Patch13:        0004-set-wandboard-to-use-generic-commands-and-set-needed.patch
Patch14:        0005-set-the-default-wandboard-boot-commands.patch
Patch15:        0006-set-omap4-to-use-extlinux.conf-by-default.patch
Patch16:        0007-enable-CONFIG_CMD_BOOTMENU-for-distro-configs.patch
Patch17:        0008-DISABLE-FIT-image-support-since-it-fails-to-build.patch
Patch18:        0009-add-defualt-DHCP-config-options.patch
Patch19:        0010-remove-USB-from-distro-default-not-all-systems-suppo.patch
Patch20:        0011-set-omap5-up-to-use-generic-distro-configs.patch
Patch21:        0012-setup-omap5-to-load-extlinux.conf.patch
Patch22:        0013-Setup-beagleboard-to-used-generic-distro-configs.patch
Patch23:        0014-setup-beagleboard-to-load-extlinux.conf.patch
Patch24:        0015-setup-address-variables-needed-for-distro-config.patch
Patch25:        0016-setup-am335x_evm-to-load-extlinux.conf.patch

# Panda ES memory timing issue
#Patch50: omap4-panda-memtiming.patch

BuildRequires:  dtc
Requires:       dtc

# build the tool for manipulation with environment only on arm
%ifarch %{arm}
%global with_env 1
%endif

%description
This package contains a few U-Boot utilities - mkimage for creating boot images
and fw_printenv/fw_setenv for manipulating the boot environment variables.

%ifarch %{arm}
%package     -n uboot-arndale
Summary:     u-boot bootloader binaries for arndale board
Requires:    uboot-tools

%description -n uboot-arndale
u-boot bootloader binaries for arndale board

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

%package     -n uboot-highbank
Summary:     u-boot bootloader binaries for calxeda highbank
Requires:    uboot-tools
BuildArch:   noarch

%description -n uboot-highbank
u-boot bootloader binaries for calxeda highbank

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

%package     -n uboot-paz00
Summary:     u-boot bootloader binaries for the paz00 board aka ac100
Requires:    uboot-tools

%description -n uboot-paz00
u-boot bootloader binaries for paz00 board

%package     -n uboot-smdkv310
Summary:     u-boot bootloader binaries for smdk310 board
Requires:    uboot-tools

%description -n uboot-smdkv310
u-boot bootloader binaries for smdk310 board

%package     -n uboot-snow
Summary:     u-boot bootloader binaries for snow board aka chromebook
Requires:    uboot-tools

%description -n uboot-snow
u-boot bootloader binaries for snow board

%package     -n uboot-snowball
Summary:     u-boot bootloader binaries for snowball board
Requires:    uboot-tools

%description -n uboot-snowball
u-boot bootloader binaries for snowball board

%package     -n uboot-trimslice
Summary:     u-boot bootloader binaries for trimslice board
Requires:    uboot-tools

%description -n uboot-trimslice
u-boot bootloader binaries for trimslice board

%package     -n uboot-uevm
Summary:     u-boot bootloader binaries for uevm, omap5 pandaboard
Requires:    uboot-tools

%description -n uboot-uevm
u-boot bootloader binaries for uevm, omap5 pandaboard

%package     -n uboot-wandboard_dl
Summary:     u-boot bootloader binaries for Wandboard i.MX6 Dual Lite
Requires:    uboot-tools

%description -n uboot-wandboard_dl
u-boot bootloader binaries for Wandboard i.MX6 Dual Lite

%package     -n uboot-wandboard_quad
Summary:     u-boot bootloader binaries for Wandboard i.MX6 Quad
Requires:    uboot-tools

%description -n uboot-wandboard_quad
u-boot bootloader binaries for Wandboard i.MX6 Quad

%package     -n uboot-wandboard_solo
Summary:     u-boot bootloader binaries for Wandboard i.MX6 Solo
Requires:    uboot-tools

%description -n uboot-wandboard_solo
u-boot bootloader binaries for Wandboard i.MX6 Solo

%endif

%prep
%setup -q -n u-boot-%{version}%{?candidate:-%{candidate}}
%patch1 -p1
#patch3 -p1
#patch4 -p1

%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
#%patch50 -p1 -b .panda

mkdir builds

%build
%ifarch %{arm}
make CROSS_COMPILE="" am335x_evm_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p MLO builds/MLO.beaglebone
cp -p u-boot.img builds/u-boot.img.beaglebone
make distclean

make CROSS_COMPILE="" omap3_beagle_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p MLO builds/MLO.beagle
cp -p u-boot.img builds/u-boot.img.beagle
make distclean

make CROSS_COMPILE="" arndale_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p spl/arndale-spl.bin builds/arndale-spl.bin.arndale
cp -p u-boot-dtb.bin builds/u-boot-dtb.bin.arndale
make distclean

make CROSS_COMPILE="" highbank_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p u-boot.bin builds/u-boot.bin.highbank
make distclean

make CROSS_COMPILE="" omap4_panda_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p MLO builds/MLO.panda
cp -p u-boot.img builds/u-boot.img.panda
make distclean

make CROSS_COMPILE="" origen_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p spl/origen-spl.bin builds/origen-spl.bin.origen
cp -p u-boot.bin builds/u-boot.bin.origen
make distclean

make CROSS_COMPILE="" paz00_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p u-boot-dtb-tegra.bin builds/u-boot-dtb-tegra.bin.paz00
cp -p u-boot-nodtb-tegra.bin builds/u-boot-nodtb-tegra.bin.paz00
cp -p u-boot.map builds/u-boot.map.paz00
make distclean

make CROSS_COMPILE="" smdkv310_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p spl/smdkv310-spl.bin builds/smdkv310-spl.bin.smdkv310
cp -p u-boot.bin builds/u-boot.bin.smdkv310
make distclean

make CROSS_COMPILE="" snow_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p u-boot-dtb.bin builds/u-boot-dtb.bin.snow
make distclean

make CROSS_COMPILE="" snowball_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p u-boot.bin builds/u-boot.bin.snowball
make distclean

make CROSS_COMPILE="" trimslice_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p u-boot-dtb-tegra.bin builds/u-boot-dtb-tegra.bin.trimslice
cp -p u-boot-nodtb-tegra.bin builds/u-boot-nodtb-tegra.bin.trimslice
cp -p u-boot.map builds/u-boot.map.trimslice
make distclean

make CROSS_COMPILE="" wandboard_dl_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p u-boot.imx builds/u-boot.imx.dl
make distclean

make CROSS_COMPILE="" wandboard_quad_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p u-boot.imx builds/u-boot.imx.quad
make distclean

make CROSS_COMPILE="" wandboard_solo_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p u-boot.imx builds/u-boot.imx.solo
make distclean

make CROSS_COMPILE="" omap5_uevm_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""
cp -p MLO builds/MLO.uevm
cp -p u-boot.img builds/u-boot.img.uevm
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
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-arndale/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-beagle/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-beaglebone/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-highbank/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-origen/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-panda/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-paz00/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-snow/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-snowball/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-smdkv310/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-trimslice/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-imx6dl/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-imx6quad/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-imx6solo/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-uevm/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot-vexpress/

for board in beaglebone beagle panda uevm
do
install -p -m 0644 builds/u-boot.img.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot-$(echo $board)/u-boot.img
install -p -m 0644 builds/MLO.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot-$(echo $board)/MLO
done

for board in paz00 trimslice
do
install -p -m 0644 builds/u-boot-nodtb-tegra.bin.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot-$(echo $board)/u-boot-nodtb-tegra.bin
install -p -m 0644 builds/u-boot-dtb-tegra.bin.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot-$(echo $board)/u-boot-dtb-tegra.bin
install -p -m 0644 builds/u-boot.map.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot-$(echo $board)/u-boot.map
done

install -p -m 0644 builds/arndale-spl.bin.arndale $RPM_BUILD_ROOT%{_datadir}/uboot-origen/arndale-spl.bin
install -p -m 0644 builds/u-boot-dtb.bin.arndale $RPM_BUILD_ROOT%{_datadir}/uboot-arndale/u-boot-dtb.bin

install -p -m 0644 builds/u-boot.bin.highbank $RPM_BUILD_ROOT%{_datadir}/uboot-highbank/u-boot.bin

install -p -m 0644 builds/origen-spl.bin.origen $RPM_BUILD_ROOT%{_datadir}/uboot-origen/origen-spl.bin
install -p -m 0644 builds/u-boot.bin.origen $RPM_BUILD_ROOT%{_datadir}/uboot-origen/u-boot.bin

install -p -m 0644 builds/smdkv310-spl.bin.smdkv310 $RPM_BUILD_ROOT%{_datadir}/uboot-smdkv310/smdkv310-spl.bin
install -p -m 0644 builds/u-boot.bin.smdkv310 $RPM_BUILD_ROOT%{_datadir}/uboot-smdkv310/u-boot.bin

install -p -m 0644 builds/u-boot-dtb.bin.snow $RPM_BUILD_ROOT%{_datadir}/uboot-snow/u-boot-dtb.bin
install -p -m 0644 builds/u-boot.bin.snowball $RPM_BUILD_ROOT%{_datadir}/uboot-snowball/u-boot.bin

install -p -m 0644 builds/u-boot.imx.dl $RPM_BUILD_ROOT%{_datadir}/uboot-imx6dl/u-boot.imx
install -p -m 0644 builds/u-boot.imx.quad $RPM_BUILD_ROOT%{_datadir}/uboot-imx6quad/u-boot.imx
install -p -m 0644 builds/u-boot.imx.solo $RPM_BUILD_ROOT%{_datadir}/uboot-imx6solo/u-boot.imx

install -p -m 0644 %{SOURCE1}  $RPM_BUILD_ROOT%{_datadir}/uboot-beagle/uEnv.txt.beagle
install -p -m 0644 %{SOURCE2}  $RPM_BUILD_ROOT%{_datadir}/uboot-beaglebone/uEnv.txt.beaglebone
install -p -m 0644 %{SOURCE3}  $RPM_BUILD_ROOT%{_datadir}/uboot-beagle/uEnv.txt.beagle_xm
install -p -m 0644 %{SOURCE4}  $RPM_BUILD_ROOT%{_datadir}/uboot-panda/uEnv.txt.panda
install -p -m 0644 %{SOURCE5}  $RPM_BUILD_ROOT%{_datadir}/uboot-panda/uEnv.txt.panda_a4
install -p -m 0644 %{SOURCE6}  $RPM_BUILD_ROOT%{_datadir}/uboot-panda/uEnv.txt.panda_es
install -p -m 0644 %{SOURCE7}  $RPM_BUILD_ROOT%{_datadir}/uboot-uevm/uEnv.txt.uevm
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
%doc README doc/README.imximage doc/README.kwbimage doc/uImage.FIT
%{_bindir}/mkimage
%{_mandir}/man1/mkimage.1*
%if 0%{?with_env}
%{_bindir}/fw_printenv
%{_bindir}/fw_setenv
%config(noreplace) %{_sysconfdir}/fw_env.config
%endif
%ifarch %{arm}
%files -n uboot-arndale
%defattr(-,root,root,-)
%{_datadir}/uboot-arndale/

%files -n uboot-beaglebone
%defattr(-,root,root,-)
%{_datadir}/uboot-beaglebone/

%files -n uboot-beagle
%defattr(-,root,root,-)
%{_datadir}/uboot-beagle/

%files -n uboot-highbank
%defattr(-,root,root,-)
%{_datadir}/uboot-highbank/

%files -n uboot-panda
%defattr(-,root,root,-)
%{_datadir}/uboot-panda/

%files -n uboot-paz00
%defattr(-,root,root,-)
%{_datadir}/uboot-paz00/

%files -n uboot-origen
%defattr(-,root,root,-)
%{_datadir}/uboot-origen/

%files -n uboot-snow
%defattr(-,root,root,-)
%{_datadir}/uboot-snow/

%files -n uboot-snowball
%defattr(-,root,root,-)
%{_datadir}/uboot-snowball/

%files -n uboot-smdkv310
%defattr(-,root,root,-)
%{_datadir}/uboot-smdkv310/

%files -n uboot-trimslice
%defattr(-,root,root,-)
%{_datadir}/uboot-trimslice/

%files -n uboot-wandboard_dl
%defattr(-,root,root,-)
%{_datadir}/uboot-imx6dl/

%files -n uboot-wandboard_quad
%defattr(-,root,root,-)
%{_datadir}/uboot-imx6quad/

%files -n uboot-wandboard_solo
%defattr(-,root,root,-)
%{_datadir}/uboot-imx6solo/

%files -n uboot-uevm
%defattr(-,root,root,-)
%{_datadir}/uboot-uevm/
%endif

%changelog
* Fri Oct 04 2013 Dennis Gilmore <dennis@ausil.us> - 2013.10-0.5.rc4
- update to 2013.10-rc4

* Fri Sep 20 2013 Dennis Gilmore <dennis@ausil.us> - 2013.10-0.4.rc3
- install u-boot.map for trimslice and paz00

* Fri Sep 20 2013 Dennis Gilmore <dennis@ausil.us> - 2013.10-0.3.rc3
- install trimslice u-boot correctly

* Fri Sep 20 2013 Dennis Gilmore <dennis@ausil.us> - 2013.10-0.2.rc3
- enable arndale, paz00, snow, snowball and trimslice builds

* Thu Sep 19 2013 Dennis Gilmore <dennis@ausil.us> - 2013.10-0.1.rc3
- update to 2013.10-rc3
- disable panda timing patch for now

* Mon Sep 02 2013 Dennis Gilmore <dennis@ausil.us> - 2013.10-0.1.rc2
- update  to 2013.10-rc2
- enable extlinux.conf support on most boards
- add distro generic configuration options

* Sun Sep  1 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2013.07-2
- Add patch for Panda ES memory type issue

* Fri Jul 26 2013 Dennis Gilmore <dennis@ausil.us> - 2013.07-1
- update to 2013.07 final 

* Thu Jul 18 2013 Dennis Gilmore <dennis@ausil.us> - 2013.07-0.2.rc3
- update to 2013.07 rc3
- set wandboard to use extlinux.conf by default

* Thu Jul 04 2013 Dennis Gilmore <dennis@ausil.us> - 2013.07-0.1.rc2
- update beaglebone patches 
- update wandboard quad patch
- upstream 2013.07-rc2 update

* Wed Jun 05 2013 Dennis Gilmore <dennis@ausil.us> - 2013.04-5
- add patches to support ext filesystems in exynos and omap SPL's
- drop bringing in arm-boot-config on arm systems
- build a highbank u-boot (intention is to use in qemu)
- add wandboard quad u-boot

* Wed May 22 2013 Dennis Gilmore <dennis@ausil.us> - 2013.04-4
- build vexpress image
- add uEnv.txt files for various supported omap systems

* Sat May 18 2013 Dennis Gilmore <dennis@ausil.us> - 2013.04-3
- add uevm, the omap5 based pandaboard
- Require arm-boot-config on arm arches 

* Mon May 13 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2013.04-2
- Add patches for initial support for the Beagle Bone Black

* Sun Apr 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2013.04-1
- Update to 2013.04 release
- Build i.MX6 Wandboard Dual Lite and Solo Boards

* Sun Mar 31 2013 Dennis Gilmore <dennis@ausil.us> - 2013.04-0.1.rc1
- update to 2013.04-rc2

* Fri Mar 01 2013 Dennis Gilmore <dennis@ausil.us> - 2013.01.01-1
- update to 2013.01.01 for bug#907139

* Thu Jan 24 2013 Dennis Gilmore <dennis@ausil.us> - 2013.01-1
- update to 2013.01 release

* Wed Oct 17 2012 Dennis Gilmore <dennis@ausil.us> - 2012.10-1
- update to final 2012.10 release

* Thu Oct 11 2012 Mauro Carvalho Chehab <mchehab@redhat.com>
- Also generate uboot for SMDK310

* Tue Oct 09 2012 Dennis Gilmore <dennis@ausil.us> - 2012.10-0.1.rc3
- update to 2010.10 rc3

* Fri Aug 24 2012 Dennis Gilmore <dennis@ausil.us> - 2012.01-1
- update to 2012.07 release

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.07-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Dennis Gilmore <dennis@ausil.us> - 2012.07-0.1.rc1
- update to rc1 of 2012.07 release

* Sat Jul 07 2012 Dennis Gilmore <dennis@ausil.us> - 2012.04.01-4
- still build the beagleboard image

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
