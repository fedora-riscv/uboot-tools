#global candidate rc4

Name:      uboot-tools
Version:   2019.04
Release:   2%{?candidate:.%{candidate}}.0.riscv64%{?dist}
Summary:   U-Boot utilities
License:   GPLv2+ BSD LGPL-2.1+ LGPL-2.0+
URL:       http://www.denx.de/wiki/U-Boot

Source0:   ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}%{?candidate:-%{candidate}}.tar.bz2
Source1:   arm-boards
Source2:   arm-chromebooks
Source3:   aarch64-boards
Source4:   aarch64-chromebooks
Source5:   10-devicetree.install
Source6:   riscv64-boards

# Fedoraisms patches
Patch1:    uefi-use-Fedora-specific-path-name.patch

# general fixes
Patch2:    usb-kbd-fixes.patch
Patch3:    uefi-distro-load-FDT-from-any-partition-on-boot-device.patch
Patch4:    uefi-fix-memory-calculation-overflow-on-32-bit-systems.patch
Patch5:    uefi-Change-FDT-memory-type-from-runtime-data-to-boot-services-data.patch

# Board fixes and enablement
Patch10:   rpi-Enable-using-the-DT-provided-by-the-Raspberry-Pi.patch
Patch11:   dragonboard-fixes.patch
Patch12:   ARM-tegra-Add-support-for-framebuffer-carveouts.patch
Patch13:   ARM-tegra-Miscellaneous-improvements.patch
Patch15:   net-eth-uclass-Write-MAC-address-to-hardware-after-probe.patch
Patch16:   net-rtl8169-Implement---hwaddr_write-callback.patch
Patch17:   arm-tegra-defaine-fdtfile-for-all-devices.patch

# RISC-V (riscv64)
Patch30:   u-boot-2019.04-rc4-riscv.patch
# See: https://lists.denx.de/pipermail/u-boot/2019-April/364281.html
Patch31:   uboot-riscv-apr8-smp.patch

BuildRequires:  bc
BuildRequires:  dtc
BuildRequires:  make
# Added for .el7 rebuild, so newer gcc is used
%if 0%{?rhel} == 7
BuildRequires:  devtoolset-7-build
BuildRequires:  devtoolset-7-binutils
BuildRequires:  devtoolset-7-gcc
%else
BuildRequires:  gcc
%endif
BuildRequires:  flex bison
BuildRequires:  openssl-devel
%if 0%{?fedora}
BuildRequires:  python-unversioned-command
%endif
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-libfdt
%if 0%{?rhel} == 7
BuildRequires:  python-pyelftools
%else
BuildRequires:  python2-pyelftools
%endif
BuildRequires:  SDL-devel
BuildRequires:  swig
%ifarch %{arm} aarch64
BuildRequires:  vboot-utils
%endif
%ifarch aarch64
BuildRequires:  arm-trusted-firmware-armv8
%endif

Requires:       dtc
Requires:       systemd

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

%ifarch riscv64
%package     -n uboot-images-riscv64
Summary:     u-boot bootloader images for riscv64 boards
Requires:    uboot-tools
BuildArch:   noarch

%description -n uboot-images-riscv64
u-boot bootloader binaries for riscv64 boards
%endif


%ifarch %{arm} aarch64 riscv64
%package     -n uboot-images-elf
Summary:     u-boot bootloader images for armv7 boards
Requires:    uboot-tools
Obsoletes:   uboot-images-qemu
Provides:    uboot-images-qemu

%description -n uboot-images-elf
u-boot bootloader ELF binaries for use with qemu and other platforms
%endif

%prep
%autosetup -p1 -n u-boot-%{version}%{?candidate:-%{candidate}}

cp %SOURCE1 %SOURCE2 %SOURCE3 %SOURCE4 %SOURCE6 .

%build
mkdir builds

%if 0%{?rhel} == 7
#Enabling DTS for .el7
%{?enable_devtoolset7:%{enable_devtoolset7}}
%endif

%ifarch aarch64 %{arm} riscv64
for board in $(cat %{_arch}-boards)
do
  echo "Building board: $board"
  mkdir builds/$(echo $board)/
  # ATF selection, needs improving, suggestions of ATF SoC to Board matrix welcome
  sun50i=(a64-olinuxino amarula_a64_relic bananapi_m2_plus_h5 bananapi_m64 nanopi_a64 orangepi_win pine64-lts pine64_plus pinebook sopine_baseboard libretech_all_h3_cc_h5 nanopi_neo2 nanopi_neo_plus2 orangepi_pc2 orangepi_prime orangepi_zero_plus2 orangepi_zero_plus)
  if [[ " ${sun50i[*]} " == *" $board "* ]]; then
    echo "Board: $board using sun50i_a64"
    cp /usr/share/arm-trusted-firmware/sun50i_a64/* builds/$(echo $board)/
  fi
  sun50h6=(orangepi_lite2 orangepi_one_plus pine_h64)
  if [[ " ${sun50h6[*]} " == *" $board "* ]]; then
    echo "Board: $board using sun50i_h6"
    cp /usr/share/arm-trusted-firmware/sun50i_h6/* builds/$(echo $board)/
  fi
  rk3399=(evb-rk3399 ficus-rk3399 firefly-rk3399 puma-rk3399 rock960-rk3399)
  if [[ " ${rk3399[*]} " == *" $board "* ]]; then
    echo "Board: $board using rk3399"
    cp /usr/share/arm-trusted-firmware/rk3399/* builds/$(echo $board)/
  fi
  # End ATF
  make $(echo $board)_defconfig O=builds/$(echo $board)/
  make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1 O=builds/$(echo $board)/
  rk33xx=(evb-rk3399 ficus-rk3399 firefly-rk3399 puma-rk3399 rock960-rk3399)
  if [[ " ${rk33xx[*]} " == *" $board "* ]]; then
    echo "Board: $board using rk33xx"
    make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" u-boot.itb V=1 O=builds/$(echo $board)/
    builds/$(echo $board)/tools/mkimage -n rk3399 -T rksd  -d builds/$(echo $board)/spl/u-boot-spl.bin builds/$(echo $board)/spl_sd.img
    builds/$(echo $board)/tools/mkimage -n rk3399 -T rkspi -d builds/$(echo $board)/spl/u-boot-spl.bin builds/$(echo $board)/spl_spi.img
  fi
done

%endif

make HOSTCC="gcc $RPM_OPT_FLAGS" %{?_smp_mflags} CROSS_COMPILE="" tools-only_defconfig V=1 O=builds/
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

%ifarch riscv64
for board in $(cat %{_arch}-boards)
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
 for file in u-boot.bin u-boot-nodtb.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
  fi
 done
done
%endif

%ifarch aarch64
for board in $(cat %{_arch}-boards)
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
 for file in MLO SPL spl/arndale-spl.bin spl/origen-spl.bin spl/smdkv310-spl.bin u-boot.bin u-boot.dtb u-boot-dtb-tegra.bin u-boot.img u-boot.imx u-boot-nodtb-tegra.bin u-boot-spl.kwb u-boot-sunxi-with-spl.bin spl_sd.img spl_spi.img
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

%ifarch riscv64
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

# systemd kernel-install script for device tree
mkdir -p $RPM_BUILD_ROOT/lib/kernel/install.d/
install -p -m 0755 %{SOURCE5} $RPM_BUILD_ROOT/lib/kernel/install.d/

# Copy sone useful docs over
mkdir -p builds/docs
cp -p board/amlogic/odroid-c2/README.odroid-c2 builds/docs/README.odroid-c2
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
%doc README doc/imx doc/README.kwbimage doc/README.distro doc/README.gpt
%doc doc/README.odroid doc/README.rockchip doc/README.uefi doc/uImage.FIT doc/README.arm64
%doc doc/README.chromium builds/docs/*
%doc doc/README.qemu-riscv doc/README.sifive-fu540 doc/README.ae350
%{_bindir}/*
%{_mandir}/man1/mkimage.1*
/lib/kernel/install.d/10-devicetree.install
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

%ifarch riscv64
%files -n uboot-images-riscv64
%{_datadir}/uboot/*
%exclude %{_datadir}/uboot/elf
%endif

%ifarch %{arm} aarch64 riscv64
%files -n uboot-images-elf
%{_datadir}/uboot/elf
%endif

%changelog
* Sun May 05 2019 David Abdurachmanov <david.abdurachmanov@gmail.com> 2019.04-2.0.riscv64
- Apply pull request which incl. SMP support
  See: https://lists.denx.de/pipermail/u-boot/2019-April/364281.html
- Set CONFIG_SYS_BOOTM_LEN to SZ_64M for qemu-riscv
- Add CONFIG_PREBOOT for qemu-riscv to set fdt_addr for extlinux boot
- Add support for RISC-V (riscv64)

* Sat May  4 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2019.04-2
- Build and ship pre built SD/SPI SPL bits for all rk3399 boards

* Sun Apr 14 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2019.04-1
- 2019.04
- Fixes for AllWinner and NVIDIA Jetson devices

* Thu Apr  4 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2019.04-0.9-rc4
- Latest Tegra patch revision

* Sun Mar 31 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2019.04-0.8-rc4
- Add ability to make creation of boot/dtb symlink configurable

* Sun Mar 24 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2019.04-0.7-rc4
- Minor UEFI fixes, Tegra Jetson TX series rebase

* Wed Mar 20 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2019.04-0.6-rc4
- Tegra Jetson TX-series improvements

* Tue Mar 19 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2019.04-0.5-rc4
- 2019.04 RC4

* Tue Mar  5 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2019.04-0.4-rc3
- 2019.04 RC3

* Tue Feb 19 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2019.04-0.3-rc2
- 2019.04 RC2

* Sat Feb  9 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2019.04-0.2-rc1
- Build against new ATF snapshot

* Fri Feb  8 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2019.04-0.1-rc1
- 2019.04 RC1

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2019.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2019.01-1
- 2019.01

* Tue Jan  8 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2019.01-0.4-rc3
- 2019.01 RC3

* Tue Dec 18 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2019.01-0.3-rc2
- 2019.01 RC2

* Wed Dec 12 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2019.01-0.2-rc1
- ATF tweaks and fixes
- Enable amarula_a64_relic, nanopi_a64, puma-rk3399

* Tue Dec  4 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2019.01-0.1-rc1
- 2019.01 RC1
- Enable new devices

* Tue Dec  4 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.11-1
- 2018.11
- Build with ATF 2.0
- Fix Hummingboard and CuBox-i devices

* Tue Oct 30 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.11-0.1.rc3
- 2018.11 RC3

* Sun Sep 30 2018 Pablo Greco <pablo@fliagreco.com.ar>
- Added conditional to enable devtoolset-7-gcc for .el7 build (Arrfab)
- Added conditional BR, python2-pyelftools is python-pyelftools in .el7 (Arrfab)

* Sun Sep 23 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Update Rock960 patches, enable Rock960 Enterprise Edition (ficus)

* Mon Sep 10 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.09-1
- 2018.09

* Tue Sep  4 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.09-0.4.rc3
- 2018.09 RC3
- Enable nanopi_neo_plus2, pine_h64, rock960-rk3399, a64-olinuxino
- Build against new upstream AllWinner ATF support
- Use firmware provided DT on Raspberry Pi
- Support for Pine64-LTS

* Tue Aug 14 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.09-0.2.rc2
- 2018.09 RC2
- Improve Jetson TX1 support
- Enable OrangePi 1+ and Avnet Ultra96

* Tue Jul 31 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.09-0.1.rc1
- 2018.09 RC1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2018.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul  9 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.07-1
- 2018.07

* Tue Jul  3 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.07-0.4.rc3
- 2018.07 RC3

* Wed Jun 20 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.07-0.3.rc2
- 2018.07 RC2
- Enable Helios4

* Fri Jun  8 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.07-0.2.rc1
- Update sunxi MMC patch series, Tegra Nyan patch, SolidRun i.MX6 SoM rev 1.5 patch

* Tue Jun  5 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.07-0.1.rc1
- 2018.07 RC1
- Enable Turris Mox, BananaPi m2 Berry, some Libretech boards

* Mon May  7 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.05-1
- 2018.05 GA

* Wed May  2 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.05-0.5.rc3
- Build Xilnix ZynqMP zcu100 (96boards Ultra96)

* Tue May  1 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.05-0.4.rc3
- 2018.05 RC3

* Thu Apr 26 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.05-0.3.rc2
- uEFI improvements
- Fixes for Rockchips rk33xx 64 bit devices
- Build AllWinner 64 bit devices against new ATF

* Tue Apr 17 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.05-0.2.rc2
- 2018.05 RC2
- Enable Raspberry Pi option to use firmware DT

* Sun Apr  8 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.05-0.1.rc1
- 2018.05 RC1

* Fri Apr  6 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.03-4
- Improvements for Raspberry Pi, AllWinner MMC perf, mvebu devices

* Tue Mar 20 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.03-3
- Fix issue with certain MMC cards on Raspberry Pi

* Fri Mar 16 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.03-2
- Add support for Raspberry Pi 3+

* Tue Mar 13 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.03-1
- 2018.03 GA

* Fri Mar  9 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.03-0.11.rc4
- Enable support for Jetson TX2

* Thu Mar  8 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.03-0.10.rc4
- Fix for Raspberry Pi 2 boot

* Wed Mar  7 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.03-0.9.rc4
- 2018.03 RC4
- Fixes for Raspberry Pi 3 boot
- Minor kernel install fixes
- Enable am335x_evm_usbspl for Beagle Pocket
- DragonBoard patch rebase

* Sun Mar  4 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.03-0.8.rc3
- Add support for SoM rev 1.5 to mx6cuboxi
- Rebuild for new ATF 1.5 rc0 release

* Sun Feb 25 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.03-0.7.rc3
- Build 64 bit Rockchips FIT images with ARM Trusted Firmware

* Tue Feb 20 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.03-0.6.rc3
- 2018.03 RC3

* Fri Feb 16 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.03-0.5.rc2
- A few upstream fixes

* Thu Feb 15 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.03-0.4.rc2
- Fix for GBps network on some AllWinner devices

* Tue Feb 13 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.03-0.3.rc2
- 2018.03 RC2

* Wed Feb  7 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.03-0.2.rc1
- Update uEFI patches

* Tue Jan 30 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.03-0.1.rc1
- 2018.03 RC1

* Tue Jan  9 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.01-1
- 2018.01
