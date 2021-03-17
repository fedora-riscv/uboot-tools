%global candidate rc4

Name:     uboot-tools
Version:  2021.04
Release:  0.6%{?candidate:.%{candidate}}%{?dist}
Summary:  U-Boot utilities
License:  GPLv2+ BSD LGPL-2.1+ LGPL-2.0+
URL:      http://www.denx.de/wiki/U-Boot

Source0:  ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}%{?candidate:-%{candidate}}.tar.bz2
Source1:  arm-boards
Source2:  arm-chromebooks
Source3:  aarch64-boards
Source4:  aarch64-chromebooks

# Fedoraisms patches
# Needed to find DT on boot partition that's not the first partition
Patch1:   uefi-distro-load-FDT-from-any-partition-on-boot-device.patch
# Needed due to issues with shim
Patch2:   uefi-use-Fedora-specific-path-name.patch
# RPi - uses RPI firmware device tree for HAT support
Patch3:   rpi-Enable-using-the-DT-provided-by-the-Raspberry-Pi.patch

# Board fixes and enablement
Patch9:   0001-efi_loader-fix-memory-type-for-memory-reservation-bl.patch
# AllWinner improvements
Patch10:  AllWinner-PineTab.patch
# TI fixes
Patch11:  0001-Fix-BeagleAI-detection.patch
# Rockchips improvements
Patch12:  rk3399-Pinebook-pro-EDP-support.patch
# Fixes for Allwinner network issues
Patch13:  0001-arm-dts-allwinner-sync-from-linux-for-RGMII-RX-TX-de.patch
Patch14:  sunxi-support-asymmetric-dual-rank-DRAM-on-A64.patch

BuildRequires:  bc
BuildRequires:  dtc
BuildRequires:  make
# Requirements for building on el7
%if 0%{?rhel} == 7
BuildRequires:  devtoolset-7-build
BuildRequires:  devtoolset-7-binutils
BuildRequires:  devtoolset-7-gcc
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-libfdt
%else
BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-libfdt
%endif
BuildRequires:  flex bison
BuildRequires:  openssl-devel
BuildRequires:  SDL-devel
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
Summary:     U-Boot firmware images for aarch64 boards
BuildArch:   noarch

%description -n uboot-images-armv8
U-Boot firmware binaries for aarch64 boards
%endif

%ifarch %{arm}
%package     -n uboot-images-armv7
Summary:     U-Boot firmware images for armv7 boards
BuildArch:   noarch

%description -n uboot-images-armv7
U-Boot firmware binaries for armv7 boards
%endif

%prep
%autosetup -p1 -n u-boot-%{version}%{?candidate:-%{candidate}}

cp %SOURCE1 %SOURCE2 %SOURCE3 %SOURCE4 .

%build
mkdir builds

%if 0%{?rhel} == 7
#Enabling DTS for .el7
%{?enable_devtoolset7:%{enable_devtoolset7}}
%endif

%ifarch aarch64 %{arm}
for board in $(cat %{_arch}-boards)
do
  echo "Building board: $board"
  mkdir builds/$(echo $board)/
  # ATF selection, needs improving, suggestions of ATF SoC to Board matrix welcome
  sun50i=(a64-olinuxino amarula_a64_relic bananapi_m2_plus_h5 bananapi_m64 libretech_all_h3_cc_h5 nanopi_a64 nanopi_neo2 nanopi_neo_plus2 orangepi_pc2 orangepi_prime orangepi_win orangepi_zero_plus orangepi_zero_plus2 pine64-lts pine64_plus pinebook pinephone pinetab sopine_baseboard teres_i)
  if [[ " ${sun50i[*]} " == *" $board "* ]]; then
    echo "Board: $board using sun50i_a64"
    cp /usr/share/arm-trusted-firmware/sun50i_a64/* builds/$(echo $board)/
  fi
  sun50h6=(beelink_gs1 orangepi_3 orangepi_lite2 orangepi_one_plus orangepi_zero2 pine_h64 tanix_tx6)
  if [[ " ${sun50h6[*]} " == *" $board "* ]]; then
    echo "Board: $board using sun50i_h6"
    cp /usr/share/arm-trusted-firmware/sun50i_h6/* builds/$(echo $board)/
  fi
  rk3328=(evb-rk3328 nanopi-r2s-rk3328 rock64-rk3328 rock-pi-e-rk3328 roc-cc-rk3328)
  if [[ " ${rk3328[*]} " == *" $board "* ]]; then
    echo "Board: $board using rk3328"
    cp /usr/share/arm-trusted-firmware/rk3328/* builds/$(echo $board)/
  fi
  rk3399=(evb-rk3399 ficus-rk3399 firefly-rk3399 khadas-edge-captain-rk3399 khadas-edge-rk3399 khadas-edge-v-rk3399 nanopc-t4-rk3399 nanopi-m4-2gb-rk3399 nanopi-m4-rk3399 nanopi-neo4-rk3399 orangepi-rk3399 pinebook-pro-rk3399 puma-rk3399 rock960-rk3399 rock-pi-4c-rk3399 rock-pi-4-rk3399 rock-pi-n10-rk3399pro rockpro64-rk3399 roc-pc-mezzanine-rk3399 roc-pc-rk3399)
  if [[ " ${rk3399[*]} " == *" $board "* ]]; then
    echo "Board: $board using rk3399"
    cp /usr/share/arm-trusted-firmware/rk3399/* builds/$(echo $board)/
  fi
  # End ATF
  make $(echo $board)_defconfig O=builds/$(echo $board)/
  %make_build HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" O=builds/$(echo $board)/
  # build spi, and uart images for mvebu boards
  mvebu=(clearfog helios4)
  if [[ "  ${mvebu[*]} " == *" $board "* ]]; then
    for target in spi uart
    do
      echo "Board: $board Target: $target"
      sed -i -e '/CONFIG_MVEBU_SPL_BOOT_DEVICE_/d' configs/$(echo $board)_defconfig
      echo CONFIG_MVEBU_SPL_BOOT_DEVICE_${target^^}=y >> configs/$(echo $board)_defconfig
      make $(echo $board)_defconfig O=builds/$(echo $board-$target)/
      %make_build HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" O=builds/$(echo $board-$target)/
    done
  fi
done

%endif

%make_build HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" tools-only_defconfig O=builds/
%make_build HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" tools-all O=builds/

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_datadir}/uboot/

%ifarch aarch64
for board in $(ls builds)
do
 mkdir -p %{buildroot}%{_datadir}/uboot/$(echo $board)/
 for file in u-boot.bin u-boot.dtb u-boot.img u-boot-dtb.img u-boot.itb u-boot-sunxi-with-spl.bin u-boot-rockchip.bin idbloader.img spl/boot.bin spl/sunxi-spl.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) %{buildroot}%{_datadir}/uboot/$(echo $board)/
  fi
 done
done
%endif

%ifarch %{arm}
for board in $(ls builds)
do
 mkdir -p %{buildroot}%{_datadir}/uboot/$(echo $board)/
 for file in MLO SPL spl/arndale-spl.bin spl/origen-spl.bin spl/*spl.bin u-boot.bin u-boot.dtb u-boot-dtb-tegra.bin u-boot.img u-boot.imx u-boot-spl.kwb u-boot-rockchip.bin u-boot-sunxi-with-spl.bin spl/boot.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) %{buildroot}%{_datadir}/uboot/$(echo $board)/
  fi
 done

done

# Bit of a hack to remove binaries we don't use as they're large
for board in $(ls builds)
do
  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot-sunxi-with-spl.bin ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.*
  fi
  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/MLO ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi
  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/SPL ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi
  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.imx ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi
  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot-spl.kwb ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.*
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot-spl.bin
  fi
done
%endif

for tool in bmp_logo dumpimage env/fw_printenv fit_check_sign fit_info gdb/gdbcont gdb/gdbsend gen_eth_addr gen_ethaddr_crc img2srec mkenvimage mkimage mksunxiboot ncb proftool sunxi-spl-image-builder ubsha1 xway-swap-bytes kwboot
do
install -p -m 0755 builds/tools/$tool %{buildroot}%{_bindir}
done
install -p -m 0644 doc/mkimage.1 %{buildroot}%{_mandir}/man1

install -p -m 0755 builds/tools/env/fw_printenv %{buildroot}%{_bindir}
( cd %{buildroot}%{_bindir}; ln -sf fw_printenv fw_setenv )

# Copy some useful docs over
mkdir -p builds/docs
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
%doc README doc/README.kwbimage doc/README.distro doc/README.gpt
%doc doc/README.odroid doc/README.rockchip doc/uefi doc/uImage.FIT doc/arch/arm64.rst
%doc doc/README.chromium builds/docs/*
%doc doc/board/amlogic/ doc/board/rockchip/
%{_bindir}/*
%{_mandir}/man1/mkimage.1*
%dir %{_datadir}/uboot/

%ifarch aarch64
%files -n uboot-images-armv8
%{_datadir}/uboot/*
%endif

%ifarch %{arm}
%files -n uboot-images-armv7
%{_datadir}/uboot/*
%endif

%changelog
* Wed Mar 17 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.04-0.6.rc4
- Update to 2021.04 RC4
- Move to upstream fix for SMP on RPi3B and RPi3B+

* Sat Mar 13 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.04-0.5.rc3
- Fix for SMP on RPi3B and RPi3B+
- Initial support for Pinephone 3Gb edition

* Mon Mar 08 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.04-0.4.rc3
- Update to 2021.04 RC3

* Tue Feb 16 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.04-0.3.rc2
- Update to 2021.04 RC2

* Mon Feb 15 2021 Dennis Gilmore <dennis@ausil.us>
- build spi and uart images in addition to mmc for helios4 and clearfog

* Wed Feb 10 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.04-0.2.rc1
- Fixes for network issues on some Allwinner devices

* Mon Feb 01 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.04-0.1.rc1
- Update to 2021.04 RC1
- Add new upstream devices

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2021.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.01-1
- Update to 2021.01 GA
- Updates for Raspberry Pi 4 Series of devices

* Tue Jan  5 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.01-0.5.rc5
- Update to 2021.01 RC5

* Sun Dec 27 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.01-0.4.rc4
- Update to 2021.01 RC4
- Latest RPi-400/CM4 support patch

* Tue Dec 15 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.01-0.3.rc3
- Update to 2021.01 RC3
- Latest RPi-400/CM4 support patch
- Re-enable previously disabled device support

* Mon Dec 14 2020 Javier Martinez Canillas <javierm@redhat.com> - 2021.01-0.2.rc2
- Fix a "scan_dev_for_efi" not defined error

* Sun Nov 22 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.01-0.1.rc2
- Update to 2021.01 RC2
- Latest Pinebook Pro display patches
- Initial RPi-400 support patch
- Update Fedora specific patches

* Sun Nov  8 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.10-3
- Fix SPI on Rockchip devices
- Latest Pinebook Pro display patches
- Fix Keyboard and USB-A ports on Pinebook Pro

* Wed Oct 28 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.10-2
- Fix kernel installs for non EBBR systems
- Fix for wired networks on some Allwinner devices

* Tue Oct 06 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.10-1
- Update to 2020.10

* Sun Sep 27 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.10-0.6.rc5
- Initial support for display output on Pinebook Pro

* Tue Sep 22 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.10-0.5.rc5
- Update to 2020.10 RC5

* Wed Sep 09 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.10-0.4.rc4
- Update to 2020.10 RC4

* Wed Aug 19 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.10-0.3.rc2
- Enable a number of new Rockchip devices

* Mon Aug 10 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.10-0.2.rc2
- Update to 2020.10 RC2

* Tue Jul 28 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.10-0.1.rc1
- 2020.10 RC1

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 2020.07-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Mon Jul 06 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.07-1
- 2020.07 GA

* Tue Jun 23 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.07-0.5.rc5
- 2020.07 RC5

* Thu Jun 18 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.07-0.4.rc4
- Update various patches to latest upstream

* Wed Jun 10 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.07-0.3.rc4
- 2020.07 RC4
- Minor updates and other fixes

* Tue May 12 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.07-0.2.rc2
- 2020.07 RC2
- Minor device updates

* Wed Apr 29 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.07-0.1.rc1
- 2020.07 RC1

* Tue Apr 21 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.04-4
- Initial support for USB on Rasperry Pi 4

* Tue Apr 21 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.04-3
- Ship u-boot-rockchip.bin for SPI flash

* Mon Apr 20 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.04-2
- Fix ATF for new aarch64 devices
- Fix Wandboard board detection (rhbz 1825247)
- Fix mSD card on RockPro64
- Enable (inital) Pinebook Pro

* Tue Apr 14 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.04-1
- 2020.04

* Tue Apr  7 2020 Peter Robinson <pbrobinson@fedoraproject.org> 2020.04-0.7-rc5
- 2020.04 RC5

* Tue Mar 31 2020 Peter Robinson <pbrobinson@fedoraproject.org> 2020.04-0.6-rc4
- 2020.04 RC4
- Updates for NVIDIA Jetson platforms
- Support RNG for random seed for KASLR on some Rockchip devices

* Thu Mar 26 2020 Peter Robinson <pbrobinson@fedoraproject.org> 2020.04-0.5-rc3
- Fix ext4 alignment issue seen on some NXP i.MX devices

* Wed Feb 26 2020 Peter Robinson <pbrobinson@fedoraproject.org> 2020.04-0.4-rc3
- 2020.04 RC3

* Thu Feb 13 2020 Peter Robinson <pbrobinson@fedoraproject.org> 2020.04-0.3-rc2
- 2020.04 RC2

* Sun Feb  2 2020 Peter Robinson <pbrobinson@fedoraproject.org> 2020.04-0.2-rc1
- Update genet NIC driver

* Wed Jan 29 2020 Peter Robinson <pbrobinson@fedoraproject.org> 2020.04-0.1-rc1
- 2020.04 RC1

* Tue Jan  7 2020 Peter Robinson <pbrobinson@fedoraproject.org> 2020.01-1
- 2020.01
