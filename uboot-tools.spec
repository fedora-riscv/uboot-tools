%global candidate rc2

Name:      uboot-tools
Version:   2017.07
Release:   0.2%{?candidate:.%{candidate}}%{?dist}
Summary:   U-Boot utilities
License:   GPLv2+ BSD LGPL-2.1+ LGPL-2.0+
URL:       http://www.denx.de/wiki/U-Boot

Source0:   ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}%{?candidate:-%{candidate}}.tar.bz2
Source1:   arm-boards
Source2:   arm-chromebooks
Source3:   aarch64-boards
Source4:   aarch64-chromebooks

Patch1:    add-BOOTENV_INIT_COMMAND-for-commands-that-may-be-ne.patch
Patch3:    mx6cuboxi-Add-support-for-sata.patch
Patch4:    mx6-Initial-Hummingboard-2-support.patch
# Patch5:    sti-STiH410-B2260-support.patch
# Patch6:    AW64-add-spl-atf-support.patch
Patch7:    use-Fedora-specific-EFI-path-name.patch
# Patch9:    arm-tegra-nyan-chromebook.patch

# Patch19:    0001-arm-mvebu-enable-generic-distro-boot-config.patch

BuildRequires:  bc
BuildRequires:  dtc
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  openssl-devel
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-libfdt
BuildRequires:  swig
%ifarch %{arm} aarch64
BuildRequires:  vboot-utils
%endif
%ifarch aarch64
BuildRequires:  arm-trusted-firmware-armv8
%endif

Requires:       dtc

%description
This package contains a few U-Boot utilities - mkimage for creating boot images
and fw_printenv/fw_setenv for manipulating the boot environment variables.

%ifarch aarch64
%package     -n uboot-images-armv8
Summary:     u-boot bootloader images for aarch64 boards
Requires:    uboot-tools
BuildArch:   noarch

%description -n uboot-images-armv8
u-boot bootloader binaries for aarch64 boards
%endif

%ifarch %{arm}
%package     -n uboot-images-armv7
Summary:     u-boot bootloader images for armv7 boards
Requires:    uboot-tools
BuildArch:   noarch

%description -n uboot-images-armv7
u-boot bootloader binaries for armv7 boards
%endif

%ifarch %{arm} aarch64
%package     -n uboot-images-elf
Summary:     u-boot bootloader images for armv7 boards
Requires:    uboot-tools
Obsoletes:   uboot-images-qemu
Provides:    uboot-images-qemu

%description -n uboot-images-elf
u-boot bootloader ELF binaries for use with qemu and other platforms
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

cp %SOURCE1 %SOURCE2 %SOURCE3 %SOURCE4 .

%build
mkdir builds

%ifarch aarch64 %{arm}
for board in $(cat %{_arch}-boards)
do
  echo "Building board: $board"
  mkdir builds/$(echo $board)/
  # ATF selection, needs improving, suggestions of ATF SoC to Board matrix welcome
  sun50i=(pine64_plus bananapi_m64 nanopi_neo2 orangepi_pc2 orangepi_prime orangepi_win orangepi_zero_plus2 sopine_baseboard)
  if [[ " ${sun50i[*]} " == *" $board "* ]]; then
    echo "Board: $board using sun50iw1p1"
    cp /usr/share/arm-trusted-firmware/sun50iw1p1/bl31.bin builds/$(echo $board)/
  fi
  rk3338=(geekbox sheep-rk3368)
  if [[ " ${rk3338[*]} " == *" $board "* ]]; then
    echo "Board: $board using rk3338"
    cp /usr/share/arm-trusted-firmware/rk3368/bl31.bin builds/$(echo $board)/
  fi
  rk3399=(evb-rk3399 firefly-rk3399 puma-rk3399)
  if [[ " ${rk3399[*]} " == *" $board "* ]]; then
    echo "Board: $board using rk3399"
    cp /usr/share/arm-trusted-firmware/rk3399/bl31.bin builds/$(echo $board)/
  fi
  # End ATF
  make $(echo $board)_defconfig O=builds/$(echo $board)/
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
for board in $(cat %{_arch}-boards)
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
 for file in spl/*spl.bin u-boot.bin u-boot.dtb u-boot-dtb.img u-boot.img u-boot.itb spl/sunxi-spl.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
  fi
 done
done
%endif

%ifarch %{arm}
for board in $(cat %{_arch}-boards)
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
 for file in MLO SPL spl/arndale-spl.bin spl/origen-spl.bin spl/smdkv310-spl.bin spl/*spl.bin u-boot.bin u-boot.dtb u-boot-dtb-tegra.bin u-boot.img u-boot.imx u-boot-nodtb-tegra.bin u-boot-spl.kwb u-boot-sunxi-with-spl.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
  fi
 done

done

# Bit of a hack to remove binaries we don't use as they're large
for board in $(cat %{_arch}-boards)
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
for board in $(cat %{_arch}-boards)
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

# ELF binaries
%ifarch %{arm}
for board in vexpress_ca15_tc2 vexpress_ca9x4
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/elf/$(echo $board)/
 for file in u-boot
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) $RPM_BUILD_ROOT%{_datadir}/uboot/elf/$(echo $board)/
  fi
 done
done
%endif

%ifarch aarch64
for board in $(cat %{_arch}-boards)
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/elf/$(echo $board)/
 for file in u-boot
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) $RPM_BUILD_ROOT%{_datadir}/uboot/elf/$(echo $board)/
  fi
 done
done
%endif

for tool in bmp_logo dumpimage easylogo/easylogo env/fw_printenv fit_check_sign fit_info gdb/gdbcont gdb/gdbsend gen_eth_addr gen_ethaddr_crc img2srec mkenvimage mkimage mksunxiboot ncb proftool sunxi-spl-image-builder ubsha1 xway-swap-bytes
do
install -p -m 0755 builds/tools/$tool $RPM_BUILD_ROOT%{_bindir}
done
install -p -m 0644 doc/mkimage.1 $RPM_BUILD_ROOT%{_mandir}/man1

install -p -m 0755 builds/tools/env/fw_printenv $RPM_BUILD_ROOT%{_bindir}
( cd $RPM_BUILD_ROOT%{_bindir}; ln -sf fw_printenv fw_setenv )

install -p -m 0644 tools/env/fw_env.config $RPM_BUILD_ROOT%{_sysconfdir}

# Copy sone useful docs over
mkdir -p builds/docs
cp -p board/amlogic/odroid-c2/README builds/docs/README.odroid-c2
cp -p board/hisilicon/hikey/README builds/docs/README.hikey
cp -p board/hisilicon/hikey/README builds/docs/README.hikey
cp -p board/Marvell/db-88f6820-gp/README builds/docs/README.mvebu-db-88f6820
cp -p board/rockchip/evb_rk3399/README builds/docs/README.evb_rk3399
cp -p board/solidrun/clearfog/README builds/docs/README.clearfog
cp -p board/solidrun/mx6cuboxi/README builds/docs/README.mx6cuboxi
cp -p board/sunxi/README.sunxi64 builds/docs/README.sunxi64
cp -p board/sunxi/README.nand builds/docs/README.sunxi-nand
cp -p board/ti/am335x/README builds/docs/README.am335x
cp -p board/ti/omap5_uevm/README builds/docs/README.omap5_uevm
cp -p board/udoo/README builds/docs/README.udoo
cp -p board/wandboard/README builds/docs/README.wandboard
cp -p board/warp/README builds/docs/README.warp
cp -p board/warp7/README builds/docs/README.warp7

%files
%doc README doc/README.imximage doc/README.kwbimage doc/README.distro doc/README.gpt
%doc doc/README.odroid doc/README.rockchip doc/README.efi doc/uImage.FIT doc/README.arm64
%doc doc/README.chromium builds/docs/*
%{_bindir}/*
%{_mandir}/man1/mkimage.1*
%dir %{_datadir}/uboot/
%config(noreplace) %{_sysconfdir}/fw_env.config

%ifarch aarch64
%files -n uboot-images-armv8
%{_datadir}/uboot/*
%exclude %{_datadir}/uboot/elf
%endif

%ifarch %{arm}
%files -n uboot-images-armv7
%{_datadir}/uboot/*
%exclude %{_datadir}/uboot/elf
%endif

%ifarch %{arm} aarch64
%files -n uboot-images-elf
%{_datadir}/uboot/elf
%endif

%changelog
* Tue Jun 20 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.07-0.2.rc2
- 2017.07 RC2
- Enable AllWinner: NanoPi M1+, NanoPi Neo2, SoPine baseboard, OrangePi Zero+2, OrangePi Win
- Enable Rockchips: GeekBox, Sheep

* Tue Jun  6 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.07-0.1.rc1
- 2017.07 RC1
- Build BananaPi m64, OrangePi pc2, OrangePi Prime with ATF

* Mon May 29 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-02
- Add distro-boot support for ClearFog
- Add support for building a chained u-boot for nyan-big

* Tue May  9 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-01
- 2017.05

* Wed May  3 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-0.7.rc7
- 2017.05 RC3

* Mon Apr 24 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-0.6.rc2
- Add SPL/ATF support for AllWinner A64 SoCs
- Ship u-boot elf binaries for all aarch64 devices
- Cleanups and spec updates
- Add some more docs/tools

* Mon Apr 17 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-0.5.rc2
- Ship the elf u-boot binaries for aarch64

* Mon Apr 17 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-0.4.rc2
- 2017.05 RC2

* Tue Apr 11 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-0.3.rc1
- Add support for STi STiH410

* Wed Apr  5 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-0.2.rc1
- Build am335x_evm

* Wed Apr  5 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-0.1.rc1
- 2017.05 RC1
- Enable TinkerBoard and MacchiatoBIN

* Mon Mar 20 2017 Jon Disnard <parasense@fedoraproject.org> 2017.03-2
- Pass --no-dynamic-linker for linkers newer than 2.26 
- Add build dependency on gcc

* Mon Mar 13 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.03-1
- 2017.03

* Mon Mar  6 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.03-0.7.rc3
- Add support for SATA on Cubox-i and Hummingboard
- Add initial Hummingboard 2 (Gate/Edge) support
- Add initial Marvell ESPRESSOBin board support

* Tue Feb 28 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.03-0.6.rc3
- 2017.03 RC3

* Wed Feb 15 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.03-0.5.rc2
- Rebase OpenSSL 1.1 patches

* Mon Feb 13 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.03-0.4.rc2
- 2017.03 RC2
- Temporarily drop OpenSSL 1.1 patches (need rebase)
- Add fix for UDOO Neo distro boot

* Mon Feb 13 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.03-0.3.rc1
- Add patches to fix build against OpenSSL 1.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.03-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.03-0.1.rc1
- 2017.03 RC1

* Tue Jan 10 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.01-1
- 2017.01

* Tue Jan  3 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.01-0.4.rc3
- Enable new devices

* Tue Jan  3 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.01-0.3.rc3
- 2017.01 RC3

* Tue Dec 20 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2017.01-0.2.rc2
- 2017.01 RC2

* Wed Dec  7 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2017.01-0.1.rc1
- 2017.01 RC1

* Tue Nov 29 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.11-2
- Add upstream patch to support UDOO Neo

* Mon Nov 14 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.11-1
- Update to 2016.11 GA

* Mon Oct 31 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.11-0.3.rc3
- 2016.11 RC3

* Tue Oct 18 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.11-0.2.rc2
- 2016.11 RC2

* Sat Oct  8 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.11-0.1.rc1
- 2016.11 RC1

* Tue Sep 20 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.09.01-1
- Update to 2016.09.01 GA

* Mon Sep 12 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.09-3
- Update to 2016.09 GA
- Add qemu elf binaries to new subpackage

* Tue Aug 23 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.09-2rc2
- 2016.09 RC2

* Wed Jul 27 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.09-1rc1
- 2016.09 RC1

* Tue Jul 12 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.07-1
- Update to 2016.07 GA

* Thu Jul  7 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.07-0.4rc3
- Minor updates and cleanups

* Tue Jul  5 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.07-0.3rc3
- 2016.07 RC3

* Tue Jun 21 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.07-0.2rc2
- 2016.07 RC2

* Tue Jun  7 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.07-0.1rc1
- 2016.07 RC1
- Build new aarch64 devices: odroid-c2
- Build new ARMv7 devices: chromebook-jerry

* Mon May 23 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2016.05-3
- Ship SPL for rockchips devices

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
