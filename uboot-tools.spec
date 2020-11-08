#global candidate rc5

Name:     uboot-tools
Version:  2020.10
Release:  3%{?candidate:.%{candidate}}%{?dist}
Summary:  U-Boot utilities
License:  GPLv2+ BSD LGPL-2.1+ LGPL-2.0+
URL:      http://www.denx.de/wiki/U-Boot

Source0:  ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}%{?candidate:-%{candidate}}.tar.bz2
Source1:  arm-boards
Source2:  arm-chromebooks
Source3:  aarch64-boards
Source4:  aarch64-chromebooks
Source5:  10-devicetree.install

# Fedoraisms patches
# Needed to find DT on boot partition that's not the first partition
Patch1:   uefi-distro-load-FDT-from-any-partition-on-boot-device.patch
# Needed due to issues with shim
Patch2:   uefi-use-Fedora-specific-path-name.patch
Patch3:   rockchip-spl-u-boot-itb-offset.patch

# Board fixes and enablement
# RPi - uses RPI firmware device tree for HAT support
Patch5:   rpi-Enable-using-the-DT-provided-by-the-Raspberry-Pi.patch
# Tegra improvements
Patch6:   arm-tegra-define-fdtfile-option-for-distro-boot.patch
Patch7:   arm-add-BOOTENV_EFI_SET_FDTFILE_FALLBACK-for-tegra186-be.patch
# AllWinner improvements
Patch8:   AllWinner-UpstreamSync.patch
Patch9:   AllWinner-PinePhone.patch
Patch10:  AllWinner-PineTab.patch
Patch11:  0001-Fixes-for-AllWinner-ethernet-network-interfaces.patch
# TI fixes
Patch12:  0001-Fix-BeagleAI-detection.patch
# Rockchips improvements
Patch13:  arm-rk3399-enable-rng-on-rock960-and-firefly3399.patch
Patch14:  rk3399-Pinebook-pro-EDP-support.patch
Patch15:  rk3399-reset-display-hack.patch
Patch16:  rockchip-Rock960-Fix-up-USB-support.patch
Patch17:  rockchip-Move-Bob-specific-bits-to-it-s-specific-u-b.patch

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
Requires:       systemd
%ifarch aarch64 %{arm}
Obsoletes:      uboot-images-elf < 2019.07
Provides:       uboot-images-elf < 2019.07
%endif

%description
This package contains a few U-Boot utilities - mkimage for creating boot images
and fw_printenv/fw_setenv for manipulating the boot environment variables.

%ifarch aarch64
%package     -n uboot-images-armv8
Summary:     U-Boot firmware images for aarch64 boards
Requires:    uboot-tools
BuildArch:   noarch

%description -n uboot-images-armv8
U-Boot firmware binaries for aarch64 boards
%endif

%ifarch %{arm}
%package     -n uboot-images-armv7
Summary:     U-Boot firmware images for armv7 boards
Requires:    uboot-tools
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
  sun50h6=(orangepi_lite2 orangepi_one_plus pine_h64)
  if [[ " ${sun50h6[*]} " == *" $board "* ]]; then
    echo "Board: $board using sun50i_h6"
    cp /usr/share/arm-trusted-firmware/sun50i_h6/* builds/$(echo $board)/
  fi
  rk3328=(evb-rk3328 rock64-rk3328 rock-pi-e-rk3328 roc-cc-rk3328)
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
done

%endif

%make_build HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" tools-only_defconfig O=builds/
%make_build HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" tools-all O=builds/

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/

%ifarch aarch64
for board in $(cat %{_arch}-boards)
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
 for file in u-boot.bin u-boot.dtb u-boot.img u-boot-dtb.img u-boot.itb u-boot-sunxi-with-spl.bin u-boot-rockchip.bin idbloader.img spl/boot.bin spl/sunxi-spl.bin
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
 for file in MLO SPL spl/arndale-spl.bin spl/origen-spl.bin spl/*spl.bin u-boot.bin u-boot.dtb u-boot-dtb-tegra.bin u-boot.img u-boot.imx u-boot-spl.kwb u-boot-rockchip.bin u-boot-sunxi-with-spl.bin spl/boot.bin
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

for tool in bmp_logo dumpimage env/fw_printenv fit_check_sign fit_info gdb/gdbcont gdb/gdbsend gen_eth_addr gen_ethaddr_crc img2srec mkenvimage mkimage mksunxiboot ncb proftool sunxi-spl-image-builder ubsha1 xway-swap-bytes
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
%doc README doc/README.kwbimage doc/README.distro doc/README.gpt
%doc doc/README.odroid doc/README.rockchip doc/uefi doc/uImage.FIT doc/arch/arm64.rst
%doc doc/README.chromium builds/docs/*
%doc doc/board/amlogic/ doc/board/rockchip/
%{_bindir}/*
%{_mandir}/man1/mkimage.1*
/lib/kernel/install.d/10-devicetree.install
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
* Sun Nov  8 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2020.10-3
- Fix SPI on Rockchip devices

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
