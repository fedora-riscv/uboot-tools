#global candidate

Name:           uboot-tools
Version:        2014.04
Release:        4%{?candidate:.%{candidate}}%{?dist}
Summary:        U-Boot utilities

Group:          Development/Tools
License:        GPLv2+ BSD LGPL-2.1+ LGPL-2.0+
URL:            http://www.denx.de/wiki/U-Boot
Source0:        ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}%{?candidate:-%{candidate}}.tar.bz2
Source1:        uEnv.txt
Patch1:         u-boot-fat.patch

Patch10:        0001-TI-Add-use-a-DEFAULT_LINUX_BOOT_ENV-environment-stri.patch
Patch11:        0002-am335x_evm-Update-the-ramdisk-args-we-pass-things-in.patch
Patch12:        0003-am43xx_evm-Update-the-ramdisk-args-we-pass-things-in.patch
Patch13:        0004-pxe-additionaly-check-for-fdt_file-env-variable.patch
Patch14:        0005-convert-snowball-to-distro-generic-config.patch
Patch15:        0006-move-wandboard-over-to-use-the-generic-distro-config.patch
Patch16:        0007-move-udoo-over-to-use-the-generic-distro-configuatio.patch
Patch17:        0008-move-pandaboard-over-to-use-the-generic-distro-confi.patch
Patch18:        0009-move-beaglebone-over-to-use-the-generic-distro-confi.patch
Patch19:        0010-add-header-with-a-generic-set-of-boot-commands-defin.patch
Patch20:        0011-add-README.distro-file.patch
Patch21:        0012-cleanup-duplicate-options-in-paz00-config.patch
Patch22:        0013-add-hackish-utilite-build-based-on-wandboard.patch
Patch23:        0014-add-to-ti_armv7_common.h-generic-distro-environment-.patch
Patch24:        0015-omap4-buildfixes.patch
Patch25:        0016-automatically-add-console-to-bootline-when-not-exist.patch
Patch26:        0017-make-bootdelay-match-the-generic-distro-default.patch
Patch27:        0018-sunxi-add-sun7i-clocks-and-timer-support.patch
Patch28:        0019-sunxi-add-sun7i-pinmux-and-gpio-support.patch
Patch29:        0020-sunxi-add-sun7i-dram-setup-support.patch
Patch30:        0021-sunxi-add-sun7i-cpu-board-and-start-of-day-support.patch
Patch31:        0022-sunxi-add-support-for-Cubietruck-booting-in-FEL-mode.patch
Patch32:        0023-sunxi-add-gmac-Ethernet-support.patch
Patch33:        0024-sunxi-mmc-support.patch
Patch34:        0025-sunxi-non-FEL-SPL-boot-support-for-sun7i.patch
Patch35:        0026-port-over-to-generic-bootcommands.patch
Patch36:        0027-ARM-HYP-non-sec-move-switch-to-non-sec-to-the-last-b.patch
Patch37:        0028-ARM-HYP-non-sec-add-a-barrier-after-setting-SCR.NS-1.patch
Patch38:        0029-ARM-non-sec-reset-CNTVOFF-to-zero.patch
Patch39:        0030-ARM-add-missing-HYP-mode-constant.patch
Patch40:        0031-ARM-HYP-non-sec-add-separate-section-for-secure-code.patch
Patch41:        0032-ARM-HYP-non-sec-allow-relocation-to-secure-RAM.patch
Patch42:        0033-ARM-HYP-non-sec-add-generic-ARMv7-PSCI-code.patch
Patch43:        0034-ARM-HYP-non-sec-add-the-option-for-a-second-stage-mo.patch
Patch44:        0035-ARM-convert-arch_fixup_memory_node-to-a-generic-FDT-.patch
Patch45:        0036-ARM-HYP-non-sec-PSCI-emit-DT-nodes.patch
Patch46:        0037-PXE-syslinux-implenets-some-keywords-found-in-config.patch
Patch47:        0038-PXE-distros-implementing-syslinux-will-be-using-raw-.patch
Patch48:        0039-sunxi-fix-SRAM_B-SRAM_D-memory-map.patch
Patch49:        0040-sunxi-add-hyp-support-on-sun7i.patch

%ifnarch %{arm}
BuildRequires:  gcc-arm-linux-gnu
%endif
BuildRequires:  dtc
BuildRequires:  fedora-logos, netpbm-progs
Requires:       dtc

%description
This package contains a few U-Boot utilities - mkimage for creating boot images
and fw_printenv/fw_setenv for manipulating the boot environment variables.

%ifarch aarch64
%package     -n uboot-vexpress_aemv8a
Summary:     u-boot bootloader binaries for the aarch64 vexpress_aemv8a
Requires:    uboot-tools

%description -n uboot-vexpress_aemv8a
u-boot bootloader binaries for the aarch64 vexpress_aemv8a
%endif

%ifarch %{arm}
%package     -n uboot-images-armv7
Summary:     u-boot bootloader binaries for armv7 boards
Requires:    uboot-tools

Obsoletes: uboot-arndale < %{version}-%{release}
Provides:  uboot-arndale = %{version}-%{release}
Obsoletes: uboot-beagle < %{version}-%{release}
Provides:  uboot-beagle = %{version}-%{release}
Obsoletes: uboot-beaglebone < %{version}-%{release}
Provides:  uboot-beaglebone = %{version}-%{release}
Obsoletes: uboot-highbank < %{version}-%{release}
Provides:  uboot-highbank = %{version}-%{release}
Obsoletes: uboot-panda < %{version}-%{release}
Provides:  uboot-panda = %{version}-%{release}
Obsoletes: uboot-origen < %{version}-%{release}
Provides:  uboot-origen = %{version}-%{release}
Obsoletes: uboot-paz00 < %{version}-%{release}
Provides:  uboot-paz00 = %{version}-%{release}
Obsoletes: uboot-smdkv310 < %{version}-%{release}
Provides:  uboot-smdkv310 = %{version}-%{release}
Obsoletes: uboot-snow < %{version}-%{release}
Provides:  uboot-snow = %{version}-%{release}
Obsoletes: uboot-snowball < %{version}-%{release}
Provides:  uboot-snowball = %{version}-%{release}
Obsoletes: uboot-trimslice < %{version}-%{release}
Provides:  uboot-trimslice = %{version}-%{release}
Obsoletes: uboot-uevm < %{version}-%{release}
Provides:  uboot-uevm = %{version}-%{release}
Obsoletes: uboot-wandboard_dl < %{version}-%{release}
Provides:  uboot-wandboard_dl = %{version}-%{release}
Obsoletes: uboot-wandboard_quad < %{version}-%{release}
Provides:  uboot-wandboard_quad = %{version}-%{release}
Obsoletes: uboot-wandboard_solo < %{version}-%{release}
Provides:  uboot-wandboard_solo = %{version}-%{release}

%description -n uboot-images-armv7
u-boot bootloader binaries for armv7 boards

%endif

%prep
%setup -q -n u-boot-%{version}%{?candidate:-%{candidate}}
%patch1 -p1

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
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1

mkdir builds
# convert fedora logo to bmp for use in u-boot
pngtopnm /usr/share/pixmaps/fedora-logo.png | ppmquant 256 | ppmtobmp -bpp 8 >fedora.bmp

#replace the logos with fedora's
for bmp in tools/logos/*bmp
do
cp fedora.bmp $bmp
done

%build
%ifarch aarch64
make vexpress_aemv8a_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p u-boot.bin builds/u-boot.bin.vexpress_aemv8a
make mrproper

%endif

%ifarch %{arm}
make am335x_evm_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p MLO builds/MLO.beaglebone
cp -p u-boot.img builds/u-boot.img.beaglebone
make mrproper

make omap3_beagle_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p MLO builds/MLO.beagle
cp -p u-boot.img builds/u-boot.img.beagle
make mrproper

make arndale_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p spl/arndale-spl.bin builds/arndale-spl.bin.arndale
cp -p u-boot-dtb.bin builds/u-boot-dtb.bin.arndale
make mrproper

make Cubietruck_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.Cubietruck
make mrproper

make highbank_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p u-boot.bin builds/u-boot.bin.highbank
make mrproper

make omap4_panda_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p MLO builds/MLO.panda
cp -p u-boot.img builds/u-boot.img.panda
make mrproper

make origen_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p spl/origen-spl.bin builds/origen-spl.bin.origen
cp -p u-boot.bin builds/u-boot.bin.origen
make mrproper

make paz00_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p u-boot-dtb-tegra.bin builds/u-boot-dtb-tegra.bin.paz00
cp -p u-boot-nodtb-tegra.bin builds/u-boot-nodtb-tegra.bin.paz00
cp -p u-boot.map builds/u-boot.map.paz00
cp -p u-boot.dtb builds/u-boot.dtb.paz00
make mrproper

make smdkv310_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p spl/smdkv310-spl.bin builds/smdkv310-spl.bin.smdkv310
cp -p u-boot.bin builds/u-boot.bin.smdkv310
make mrproper

make snow_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p u-boot-dtb.bin builds/u-boot-dtb.bin.snow
make mrproper

make snowball_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p u-boot.bin builds/u-boot.bin.snowball
make mrproper

make trimslice_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p u-boot-dtb-tegra.bin builds/u-boot-dtb-tegra.bin.trimslice
cp -p u-boot-nodtb-tegra.bin builds/u-boot-nodtb-tegra.bin.trimslice
cp -p u-boot.map builds/u-boot.map.trimslice
cp -p u-boot.dtb builds/u-boot.dtb.trimslice
make mrproper

make wandboard_dl_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p u-boot.imx builds/u-boot.imx.wbdl
make mrproper

make wandboard_quad_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p u-boot.imx builds/u-boot.imx.wbquad
make mrproper

make udoo_quad_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p u-boot.imx builds/u-boot.imx.udoo_quad
make mrproper

make wandboard_solo_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p u-boot.imx builds/u-boot.imx.wbsolo
make mrproper

make omap5_uevm_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags}
cp -p MLO builds/MLO.uevm
cp -p u-boot.img builds/u-boot.img.uevm
make mrproper

%endif
%ifnarch %{arm}
make HOSTCC="gcc $RPM_OPT_FLAGS" %{?_smp_mflags} CROSS_COMPILE=arm-linux-gnu- sheevaplug_config
make HOSTCC="gcc $RPM_OPT_FLAGS" %{?_smp_mflags} CROSS_COMPILE=arm-linux-gnu- tools
%endif

%ifarch %{arm}
make HOSTCC="gcc $RPM_OPT_FLAGS" %{?_smp_mflags} CROSS_COMPILE="" sheevaplug_config
make HOSTCC="gcc $RPM_OPT_FLAGS" %{?_smp_mflags} CROSS_COMPILE="" tools
make HOSTCC="gcc $RPM_OPT_FLAGS" %{?_smp_mflags} CROSS_COMPILE="" env
%endif

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1

%ifarch aarch64
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/vexpress_aemv8a/

install -p -m 0644 builds/u-boot.bin.vexpress_aemv8a $RPM_BUILD_ROOT%{_datadir}/uboot/vexpress_aemv8a/u-boot.bin
%endif

%ifarch %{arm}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/arndale/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/beagle/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/beaglebone/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/Cubietruck/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/highbank/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/origen/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/panda/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/paz00/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/snow/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/snowball/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/smdkv310/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/trimslice/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/wandboard_dl/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/wandboard_quad/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/wandboard_solo/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/udoo_quad/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/uevm/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/vexpress/

for board in beaglebone beagle panda uevm
do
install -p -m 0644 builds/u-boot.img.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.img
install -p -m 0644 builds/MLO.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/MLO
done

for board in paz00 trimslice
do
install -p -m 0644 builds/u-boot-nodtb-tegra.bin.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot-nodtb-tegra.bin
install -p -m 0644 builds/u-boot-dtb-tegra.bin.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot-dtb-tegra.bin
install -p -m 0644 builds/u-boot.map.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.map
install -p -m 0644 builds/u-boot.dtb.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.dtb
done

install -p -m 0644 builds/arndale-spl.bin.arndale $RPM_BUILD_ROOT%{_datadir}/uboot/arndale/arndale-spl.bin
install -p -m 0644 builds/u-boot-dtb.bin.arndale $RPM_BUILD_ROOT%{_datadir}/uboot/arndale/u-boot-dtb.bin

install -p -m 0644 builds/u-boot-sunxi-with-spl.bin.Cubietruck $RPM_BUILD_ROOT%{_datadir}/uboot/Cubietruck/u-boot-sunxi-with-spl.bin

install -p -m 0644 builds/u-boot.bin.highbank $RPM_BUILD_ROOT%{_datadir}/uboot/highbank/u-boot.bin

install -p -m 0644 builds/origen-spl.bin.origen $RPM_BUILD_ROOT%{_datadir}/uboot/origen/origen-spl.bin
install -p -m 0644 builds/u-boot.bin.origen $RPM_BUILD_ROOT%{_datadir}/uboot/origen/u-boot.bin

install -p -m 0644 builds/smdkv310-spl.bin.smdkv310 $RPM_BUILD_ROOT%{_datadir}/uboot/smdkv310/smdkv310-spl.bin
install -p -m 0644 builds/u-boot.bin.smdkv310 $RPM_BUILD_ROOT%{_datadir}/uboot/smdkv310/u-boot.bin

install -p -m 0644 builds/u-boot-dtb.bin.snow $RPM_BUILD_ROOT%{_datadir}/uboot/snow/u-boot-dtb.bin
install -p -m 0644 builds/u-boot.bin.snowball $RPM_BUILD_ROOT%{_datadir}/uboot/snowball/u-boot.bin

install -p -m 0644 builds/u-boot.imx.udoo_quad $RPM_BUILD_ROOT%{_datadir}/uboot/udoo_quad/u-boot.imx

install -p -m 0644 builds/u-boot.imx.wbdl $RPM_BUILD_ROOT%{_datadir}/uboot/wandboard_dl/u-boot.imx
install -p -m 0644 builds/u-boot.imx.wbquad $RPM_BUILD_ROOT%{_datadir}/uboot/wandboard_quad/u-boot.imx
install -p -m 0644 builds/u-boot.imx.wbsolo $RPM_BUILD_ROOT%{_datadir}/uboot/wandboard_solo/u-boot.imx
%endif

install -p -m 0755 tools/mkimage $RPM_BUILD_ROOT%{_bindir}
install -p -m 0644 doc/mkimage.1 $RPM_BUILD_ROOT%{_mandir}/man1

%ifarch %{arm}
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
%ifarch %{arm}
%dir %{_datadir}/uboot/
%{_bindir}/fw_printenv
%{_bindir}/fw_setenv
%config(noreplace) %{_sysconfdir}/fw_env.config
%endif

%ifarch aarch64
%files -n uboot-images-armv8
%defattr(-,root,root,-)
%{_datadir}/uboot/vexpress_aemv8a/
%endif

%ifarch %{arm}
%files -n uboot-images-armv7
%defattr(-,root,root,-)
%{_datadir}/uboot/arndale/
%{_datadir}/uboot/beaglebone/
%{_datadir}/uboot/beagle/
%{_datadir}/uboot/Cubietruck/
%{_datadir}/uboot/highbank/
%{_datadir}/uboot/panda/
%{_datadir}/uboot/paz00/
%{_datadir}/uboot/origen/
%{_datadir}/uboot/snow/
%{_datadir}/uboot/snowball/
%{_datadir}/uboot/smdkv310/
%{_datadir}/uboot/trimslice/
%{_datadir}/uboot/wandboard_dl/
%{_datadir}/uboot/wandboard_quad/
%{_datadir}/uboot/wandboard_solo/
%{_datadir}/uboot/udoo_quad/
%{_datadir}/uboot/uevm/
%endif

%changelog
* Sat Apr 26 2014 Dennis Gilmore <dennis@ausil.us> - 2014.04-4
- add hyp support to cubietruck image
- enables kvm support

* Thu Apr 24 2014 Dennis Gilmore <dennis@ausil.us> - 2014.04-3
- add cubietruck u-boot image

* Wed Apr 23 2014 Dennis Gilmore <dennis@ausil.us> - 2014.04-2
- automatically add console line from u-boot environment to bootargs
- when there is no console argument in the extlinux.conf file

* Mon Apr 21 2014 Dennis Gilmore <dennis@ausil.us> - 2014.04-1
- update to final 2014.04
- put all images into a single rpm
- add udoo image

* Wed Mar 19 2014 Dennis Gilmore <dennis@ausil.us> - 2014.04-0.4.rc2
- apply fixes for panda and beaglebone

* Sat Mar 15 2014 Dennis Gilmore <dennis@ausil.us> - 2014.04-0.3.rc2
- Add missing header
- pull in patches on their way upstream to fix some issues with ti
- systems.
- refactor beaglebone and pandaboard patches

* Thu Mar 13 2014 Dennis Gilmore <dennis@ausil.us> - 2014.04-0.2.rc2
- actually apply patches

* Wed Mar 12 2014 Dennis Gilmore <dennis@ausil.us> - 2014.04-0.1.rc2
- update to 2014.04-rc2 
- add patches to convert some boards to generic distro configs

* Sun Oct 20 2013 Dennis Gilmore <dennis@ausil.us> - 2013.10-3
- fix ftbfs for wandboard
- use _smp_mflags

* Sat Oct 19 2013 Dennis Gilmore <dennis@ausil.us> - 2013.10-2
- use ext2load for dtb loading
- cleanup duplicate defines

* Thu Oct 17 2013 Dennis Gilmore <dennis@ausil.us> - 2013.10-1
- update to 2013.10 final
- refactor where u-boot binaries are stored

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
