#global candidate rc3

Name:      uboot-tools
Version:   2016.05
Release:   2%{?candidate:.%{candidate}}%{?dist}
Summary:   U-Boot utilities

Group:     Development/Tools
License:   GPLv2+ BSD LGPL-2.1+ LGPL-2.0+
URL:       http://www.denx.de/wiki/U-Boot
Source0:   ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}%{?candidate:-%{candidate}}.tar.bz2
Source1:   armv7-boards
Source2:   armv8-boards

Patch1:    0001-Copy-gcc5-over-to-compiler-gcc6.h-as-a-beginning-of-.patch
Patch2:    0004-Add-BOOTENV_INIT_COMMAND-for-commands-that-may-be-ne.patch
Patch3:    0005-port-utilite-to-distro-generic-boot-commands.patch
Patch4:    mvebu-enable-generic-distro-boot-config.patch
Patch5:    U-Boot-video-ipu_common-fix-build-error.patch
Patch6:    0001-clearfog-needs-HUSH-parser-for-distro-boot.patch

Patch11:   U-Boot-2-6-Revert-sunxi-Reserve-ATF-memory-space-on-A64.patch
Patch12:   U-Boot-3-6-arm64-sunxi-reserve-space-for-boot0-header.patch
Patch13:   U-Boot-4-6-arm64-sunxi-adjust-default-load-addresses.patch
Patch14:   U-Boot-5-6-arm64-Pine64-update-FDT-files.patch
Patch15:   U-Boot-6-6-Pine64-rename-defconfig.patch
Patch16:   U-Boot-efi_loader-Clean-up-system-table-on-exit.patch
Patch17:   U-Boot-efi_loader-gop-Don-t-expose-fb-address.patch


BuildRequires:  bc
BuildRequires:  dtc
BuildRequires:  fedora-logos
BuildRequires:  git
BuildRequires:  netpbm-progs
BuildRequires:  openssl-devel
BuildRequires:  SDL-devel
Requires:       dtc

%description
This package contains a few U-Boot utilities - mkimage for creating boot images
and fw_printenv/fw_setenv for manipulating the boot environment variables.

%ifarch aarch64
%package     -n uboot-images-armv8
Summary:     u-boot bootloader images for armv8 boards
Requires:    uboot-tools
BuildArch:   noarch

%description -n uboot-images-armv8
u-boot bootloader binaries for the aarch64 vexpress_aemv8a

%endif

%ifarch %{arm}
%package     -n uboot-images-armv7
Summary:     u-boot bootloader images for armv7 boards
Requires:    uboot-tools
BuildArch:   noarch

%description -n uboot-images-armv7
u-boot bootloader binaries for armv7 boards

%endif

%prep
%setup -q -n u-boot-%{version}%{?candidate:-%{candidate}}

git init
git config --global gc.auto 0
git config user.email "noone@example.com" 
git config user.name "no one" 
git add . 
git commit -a -q -m "%{version} baseline" 
git am %{patches} </dev/null 
git config --unset user.email 
git config --unset user.name 
rm -rf .git

%build
mkdir builds
# convert fedora logo to bmp for use in u-boot
# pngtopnm /usr/share/pixmaps/fedora-logo.png | ppmquant 256 | ppmtobmp -bpp 8 >fedora.bmp

#replace the logos with fedora's
#for bmp in tools/logos/*bmp
#do
#cp fedora.bmp $bmp
#done

%ifarch aarch64
for board in $(cat %SOURCE2)
do
make $(echo $board)_defconfig O=builds/$(echo $board)/
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1 O=builds/$(echo $board)/
done

%endif

%ifarch %{arm}
for board in $(cat %SOURCE1)
do
make $(echo $board)_defconfig V=1 O=builds/$(echo $board)/
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1 O=builds/$(echo $board)/
done

%endif

make HOSTCC="gcc $RPM_OPT_FLAGS" %{?_smp_mflags} CROSS_COMPILE="" defconfig V=1 O=builds/
make HOSTCC="gcc $RPM_OPT_FLAGS" %{?_smp_mflags} CROSS_COMPILE="" tools-all V=1 O=builds/

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/

%ifarch aarch64
for board in $(cat %SOURCE2)
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
 for file in MLO SPL spl/arndale-spl.bin spl/origen-spl.bin spl/smdkv310-spl.bin u-boot.bin u-boot.dtb u-boot-dtb-tegra.bin u-boot.img u-boot.imx u-boot-nodtb-tegra.bin u-boot-spl.kwb u-boot-sunxi-with-spl.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
  fi
 done
done
%endif

%ifarch %{arm}
for board in $(cat %SOURCE1)
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
 for file in MLO SPL spl/arndale-spl.bin spl/origen-spl.bin spl/smdkv310-spl.bin u-boot.bin u-boot.dtb u-boot-dtb-tegra.bin u-boot.img u-boot.imx u-boot-nodtb-tegra.bin u-boot-spl.kwb u-boot-sunxi-with-spl.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
  fi
 done
done

# Bit of a hack to remove binaries we don't use as they're large
for board in $(cat %SOURCE1)
do
  if [ -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot-sunxi-with-spl.bin ]; then
    rm -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.*
  fi
  if [ -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/MLO ]; then
    rm -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi
  if [ -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/SPL ]; then
    rm -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi
  if [ -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.imx ]; then
    rm -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi
done
%endif

%ifarch aarch64
for board in $(cat %SOURCE2)
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
 for file in MLO SPL spl/arndale-spl.bin spl/origen-spl.bin spl/smdkv310-spl.bin u-boot.bin u-boot.dtb u-boot-dtb-tegra.bin u-boot.img u-boot.imx u-boot-nodtb-tegra.bin u-boot-spl.kwb u-boot-sunxi-with-spl.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
  fi
 done
done
%endif

for tool in bmp_logo dumpimage easylogo/easylogo env/fw_printenv fit_check_sign fit_info gdb/gdbcont gdb/gdbsend gen_eth_addr img2srec mkenvimage mkimage ncb proftool ubsha1 xway-swap-bytes
do
install -p -m 0755 builds/tools/$tool $RPM_BUILD_ROOT%{_bindir}
done
install -p -m 0644 doc/mkimage.1 $RPM_BUILD_ROOT%{_mandir}/man1

install -p -m 0755 builds/tools/env/fw_printenv $RPM_BUILD_ROOT%{_bindir}
( cd $RPM_BUILD_ROOT%{_bindir}; ln -sf fw_printenv fw_setenv )

install -p -m 0644 tools/env/fw_env.config $RPM_BUILD_ROOT%{_sysconfdir}


%files
%doc README doc/README.imximage doc/README.kwbimage doc/README.imximage
%doc doc/README.distro doc/README.gpt doc/README.efi doc/uImage.FIT
%doc doc/README.odroid doc/README.rockchip
%{_bindir}/*
%{_mandir}/man1/mkimage.1*
%dir %{_datadir}/uboot/
%config(noreplace) %{_sysconfdir}/fw_env.config

%ifarch aarch64
%files -n uboot-images-armv8
%{_datadir}/uboot/*
%endif

%ifarch %{arm}
%files -n uboot-images-armv7
%{_datadir}/uboot/*
%endif

%changelog
* Thu May 19 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.05-2
- Fix distro boot on clearfog
- arm64 EFI boot fixes

* Mon May 16 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.05-1
- Update to 2016.05 GA

* Thu May 12 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.05-0.5rc3
- Add USB storage support to CHIP
- Enhanced PINE64 support

* Thu Apr 28 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.05-0.4rc3
- Upstream fix for i.MX6 breakage
- Rebase mvebu distro boot patch

* Wed Apr 27 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.05-0.3rc3
- Add work around for imx6 and renable devices

* Tue Apr 26 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.05-0.2rc3
- 2016.05 RC3
- Add some useful device READMEs that contain locations of needed firmware blobs etc
- Enable Jetson TX1
- i.MX6 still disabled

* Thu Apr 21 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.05-0.1rc1
- 2016.05 RC1
- Build aarch64 u-boot for HiKey, DragonBoard, PINE64
- Build new ARMv7 devices
- Temp disable some i.MX6 devices as build broken

* Tue Apr 19 2016 Dennis Gilmore <dennis@ausil.us> - 2016.03-6
- drop using the fedora logos for now rhbz#1328505

* Sat Apr  9 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.03-5
- Add upstream fix for ARMv7 cache issues preventing some devices from booting

* Tue Mar 22 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.03-4
- Add a better fix for network issue which caused follow on issues

* Mon Mar 21 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.03-3
- Add a work around for ggc6 issue on some ARMv7 devices
- Add fixes for AllWinner USB and some fixes for OrangePi devices

* Fri Mar 18 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.03-2
- Add upstream patches to fix some issues on some AllWinner devices

* Mon Mar 14 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.03-1
- Update to 2016.03 GA

* Sun Mar  6 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.03-0.4rc3
- Minor cleanups and new devices

* Tue Mar  1 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.03-0.3rc3
- Update to 2016.03 RC3

* Tue Feb 16 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.03-0.2rc2
- Update to 2016.03 RC2
- Enable SolidRun Clearfog

* Wed Feb  3 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.03-0.1rc1
- Update to 2016.03 RC1

* Wed Jan 20 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.01-3
- Fix PXE boot on Wandboard (rhbz #1299957)

* Tue Jan 19 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.01-2
- Add patch to fix PCI-e on Jetson TK1
- Add patch fo serial junk on BeagleBone

* Tue Jan 12 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.01-1
- Update to 2016.01 GA

* Sun Jan 10 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.01-0.4rc4
- Update to 2016.01 RC4

* Tue Dec 22 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2016.01-0.3rc3
- Update to 2016.01 RC3
- Enable Lamobo_R1

* Tue Dec  8 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2016.01-0.2rc2
- Update to 2016.01 RC2
- Enable Orange Pi (original, mini, PC, plus)

* Tue Nov 17 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2016.01-0.1rc1
- Update to 2016.01 RC1

* Sat Nov 14 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.10-3
- Use upstream Wanboard distro boot patch
- Add support for BeagleBone Green
- Add initial support for C.H.I.P.
- Enable Rockchips: Firefly, Jerry devices
- Enable Exynos: Peach Pit/Pi, Sprint devices

* Tue Nov  3 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.10-2
- Fix boot on some devices

* Tue Oct 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.10-1
- Update to 2015.10 GA
- Enable BeagleBoard X-15
- Enable new AllWinner devices

* Mon Oct 12 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.10-0.4rc5
- Update to 2015.10 RC5

* Tue Sep 29 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.10-0.3rc4
- Update to 2015.10 RC4

* Fri Sep 11 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.10-0.2rc3
- Update to 2015.10 RC3

* Tue Aug  4 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.10-0.1rc1
- Update to 2015.10 RC1

* Mon Aug  3 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.07-3
- Drop some unused u-boot binaries
- Minor cleanups

* Thu Jul 16 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.07-2
- Disable boot splash on Utilite (cm_fx6)

* Wed Jul 15 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.07-1
- Update to 2015.07 GA

* Thu Jul  2 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.07-0.4rc3
- Update to 2015.07rc3
- Some fixes for omap4/am33xx/imx6 devices

* Mon Jun 22 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.07-0.3rc2
- Initial rebase of BBB/panda/wandboard generic distro boot support

* Tue Jun 16 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.07-0.2rc2
- Enable i.MX6 marsboard and warp
- Use upstream build fix
- Add patch to fix Raspberry Pi timer speed

* Tue Jun  9 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.07-0.1rc2
- Initial rebase to 2015.07rc2
- Enable mx6cuboxi, 32 bit vexpress
- Update builds for name changes, merges etc

* Wed May 27 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.04-3
- Enable Zynq microzed, zed and zybo

* Sun May 10 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.04-2
- Build nyan-big

* Fri Apr 17 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.04-1
- Update to 2015.04 GA
- Build Raspberry Pi 2 config

* Tue Apr 07 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 2015.04-0.6.rc5
- Build U-Boot for Juno and Foundation model instead of removed board

* Thu Apr  2 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.04-0.5.rc5
- Update to 2015.04 rc5

* Mon Mar 30 2015 Dennis Gilmore <dennis@ausil.us> - 2015.04-0.4.rc4
- add patch to fix booting on omap4 devices
- refeactor spec file
- add all sunxi boards
- add odroid and odroid-xu3

* Sat Mar 21 2015 Dennis Gilmore <dennis@ausil.us> - 2015.04-0.3.rc4
- fix up bbb and wandboard to autoboot again

* Fri Mar 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.04-0.2.rc4
- Update to 2015.04 rc4

* Fri Mar  6 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.04-0.1.rc3
- Update to 2015.04 rc3
- Enable AllWinner: OLinuXino-Lime2 Mele_M3 Bananapro
- Enable i.MX6: novena hummingboard
- Build ext support into omap3 SPL

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2015.01-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Feb 07 2015 Hans de Goede <hdegoede@redhat.com> - 2015.01-3
- fix build with gcc5

* Mon Feb 02 2015 Dennis Gilmore <dennis@ausil.us> - 2015.01-2
- enable db-mv784mp-gp

* Tue Jan 13 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.01-1
- update to 2015.01

* Fri Dec 12 2014 Dennis Gilmore <dennis@ausil.us> - 2015.01-0.2.rc3
- update to 2015.01 rc3


* Wed Nov 26 2014 Dennis Gilmore <dennis@ausil.us> - 2015.01-0.1.rc2
- update to 2015.01 rc2

* Tue Nov 11 2014 Dennis Gilmore <dennis@ausil.us> - 2014.10-5
- switch the target used for beaglebone rhbz#1161619

* Mon Oct 27 2014 Dennis Gilmore <dennis@ausil.us> - 2014.10-4
- port panda board to upstreamed geneic boot commands
- append the console line automatically again

* Fri Oct 24 2014 Dennis Gilmore <dennis@ausil.us> - 2014.10-3
- scan both the first and second partitions for boot configs on beaglebone

* Thu Oct 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2014.10-2
- Add upstream patch to fix Tegra Jetson K1 pci-e (for network)

* Wed Oct 15 2014 Dennis Gilmore <dennis@ausil.us> - 2014.10-1
- update to 2014.10 final release

* Tue Oct 14 2014 Dennis Gilmore <dennis@ausil.us> - 2014.10-0.7.rc3
- refacter making directories for images
- make cm_fx6 image for utilite

* Wed Oct  8 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2014.10-0.6.rc3
- Update to 2014.10 rc3
- Add proposed distro patches from Debian
- Add BBone with distro support

* Fri Oct  3 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2014.10-0.5.rc2
- Enable some more AllWinner devices

* Mon Sep 29 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2014.10-0.4.rc2
- Add generic distro support to RIoT board
- Add patch to stabilise BananaPi network
- Spec cleanups

* Fri Sep 19 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2014.10-0.3.rc2
- Add Jetson K1, RIoT Board
- Minor spec cleanups
- use git to apply patches

* Thu Sep 18 2014 Dennis Gilmore <dennis@ausil.us> - 2014.10-0.2.rc2
- Add Cubieboard, Cubieboard2, Banana Pi, Mele_A1000 and Mele_A1000G images

* Thu Sep 18 2014 Dennis Gilmore <dennis@ausil.us> - 2014.10-0.1.rc2
- Update to 2014.10-rc2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.04-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.04-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Apr 27 2014 Dennis Gilmore <dennis@ausil.us> - 2014.04-5
- fix up aarch64 image package naming
- drop need for cross compiler to build tools

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
