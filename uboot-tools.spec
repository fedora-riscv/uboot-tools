#global candidate rc1
%if !0%{?rhel}
%bcond_without toolsonly
%else
%bcond_with toolsonly
%endif

# Set it to "opensbi" (stable) or opensbi-unstable (unstable, git)
%global opensbi opensbi-unstable

Name:     uboot-tools
Version:  2022.10
Release:  1%{?candidate:.%{candidate}}.1.riscv64%{?dist}
Summary:  U-Boot utilities
License:  GPLv2+ BSD LGPL-2.1+ LGPL-2.0+
URL:      http://www.denx.de/wiki/U-Boot

ExcludeArch: s390x
Source0:  https://ftp.denx.de/pub/u-boot/u-boot-%{version}%{?candidate:-%{candidate}}.tar.bz2
Source1:  aarch64-boards
Source2:  riscv64-boards

# Fedoraisms patches
# Needed to find DT on boot partition that's not the first partition
Patch1:   uefi-distro-load-FDT-from-any-partition-on-boot-device.patch
Patch2:   smbios-Simplify-reporting-of-unknown-values.patch

# Board fixes and enablement
# RPi - uses RPI firmware device tree for HAT support
Patch3:   rpi-Enable-using-the-DT-provided-by-the-Raspberry-Pi.patch
Patch4:   rpi-fallback-to-max-clock-for-mmc.patch
Patch5:   rpi-bcm2835_sdhost-firmware-managed-clock.patch
Patch6:   rpi-Copy-properties-from-firmware-DT-to-loaded-DT.patch
# Rockchips improvements
Patch7:   rockchip-Add-initial-support-for-the-PinePhone-Pro.patch
Patch8:   0001-Revert-power-pmic-rk8xx-Support-sysreset-shutdown-me.patch

# RISC-V (riscv64) patches
Patch20:  0001-board-sifive-spl-Initialized-the-PWM-setting-in-the-.patch
Patch21:  0002-board-sifive-spl-Set-remote-thermal-of-TMP451-to-85-.patch
Patch22:  0003-Enable-sbi-command-and-SBI-sysreset.patch
Patch23:  1dde977518f13824b847e23275001191139bc384.patch

BuildRequires:  bc
BuildRequires:  bison
BuildRequires:  dtc
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gnutls-devel
BuildRequires:  libuuid-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  perl-interpreter
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-libfdt
BuildRequires:  SDL-devel
BuildRequires:  swig
%ifarch aarch64
BuildRequires:  arm-trusted-firmware-armv8
%endif
Requires:       dtc
%ifarch riscv64
BuildRequires:  %{opensbi}
%endif

%description
This package contains a few U-Boot utilities - mkimage for creating boot images
and fw_printenv/fw_setenv for manipulating the boot environment variables.

%if %{with toolsonly}
%ifarch aarch64
%package     -n uboot-images-armv8
Summary:     U-Boot firmware images for aarch64 boards
BuildArch:   noarch

%description -n uboot-images-armv8
U-Boot firmware binaries for aarch64 boards
%endif

%ifarch riscv64
%package     -n uboot-images-riscv64
Summary:     u-boot bootloader images for riscv64 boards
Requires:    uboot-tools
BuildArch:   noarch

%description -n uboot-images-riscv64
u-boot bootloader binaries for riscv64 boards
%endif
%endif

%prep
%autosetup -p1 -n u-boot-%{version}%{?candidate:-%{candidate}}

cp %SOURCE1 %SOURCE2 .

%build
mkdir builds

%make_build HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" tools-only_defconfig O=builds/
%make_build HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" tools-all O=builds/

%if %{with toolsonly}
%ifarch riscv64
export OPENSBI=%{_datadir}/%{opensbi}/generic/firmware/fw_dynamic.bin
%endif

%ifarch aarch64 riscv64
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
  rk3399=(evb-rk3399 ficus-rk3399 firefly-rk3399 khadas-edge-captain-rk3399 khadas-edge-rk3399 khadas-edge-v-rk3399 leez-rk3399 nanopc-t4-rk3399 nanopi-m4-2gb-rk3399 nanopi-m4b-rk3399 nanopi-m4-rk3399 nanopi-neo4-rk3399 nanopi-r4s-rk3399 orangepi-rk3399 pinebook-pro-rk3399 pinephone-pro-rk3399 puma-rk3399 rock960-rk3399 rock-pi-4c-rk3399 rock-pi-4-rk3399 rock-pi-n10-rk3399pro rockpro64-rk3399 roc-pc-mezzanine-rk3399 roc-pc-rk3399)
  if [[ " ${rk3399[*]} " == *" $board "* ]]; then
    echo "Board: $board using rk3399"
    cp /usr/share/arm-trusted-firmware/rk3399/* builds/$(echo $board)/
  fi
  # End ATF

  make $(echo $board)_defconfig O=builds/$(echo $board)/
  %make_build HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" O=builds/$(echo $board)/

  # build spi images for rockchip boards with SPI flash
  rkspi=(rock64-rk3328)
  if [[ " ${rkspi[*]} " == *" $board "* ]]; then
    echo "Board: $board with SPI flash"
    builds/$(echo $board)/tools/mkimage -n rk3328 -T rkspi -d builds/$(echo $board)/tpl/u-boot-tpl.bin:builds/$(echo $board)/spl/u-boot-spl.bin builds/$(echo $board)/idbloader.spi
  fi
  rkspi=(evb-rk3399 khadas-edge-captain-rk3399 khadas-edge-rk3399 khadas-edge-v-rk3399 nanopc-t4-rk3399 pinebook-pro-rk3399 pinephone-pro-rk3399 rockpro64-rk3399 roc-pc-mezzanine-rk3399 roc-pc-rk3399)
  if [[ " ${rkspi[*]} " == *" $board "* ]]; then
    echo "Board: $board with SPI flash"
    builds/$(echo $board)/tools/mkimage -n rk3399 -T rkspi -d builds/$(echo $board)/tpl/u-boot-tpl.bin:builds/$(echo $board)/spl/u-boot-spl.bin builds/$(echo $board)/idbloader.spi
  fi
done

%endif
%endif

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_datadir}/uboot/

%if %{with toolsonly}
%ifarch aarch64
for board in $(ls builds)
do
 mkdir -p %{buildroot}%{_datadir}/uboot/$(echo $board)/
 for file in u-boot.bin u-boot.dtb u-boot.img u-boot-dtb.img u-boot.itb u-boot-sunxi-with-spl.bin u-boot-rockchip.bin idbloader.img idbloader.spi spl/boot.bin spl/sunxi-spl.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) %{buildroot}%{_datadir}/uboot/$(echo $board)/
  fi
 done
done

# For Apple M1 we also need the nodtb variant
install -p -m 0644 builds/apple_m1/u-boot-nodtb.bin %{buildroot}%{_datadir}/uboot/apple_m1/u-boot-nodtb.bin
%endif

%ifarch riscv64
for board in $(ls builds)
do
mkdir -p %{buildroot}%{_datadir}/uboot/$(echo $board)/
 for file in u-boot.bin u-boot.dtb u-boot.img u-boot-nodtb.bin u-boot-dtb.bin u-boot.itb u-boot-dtb.img u-boot.its spl/u-boot-spl.bin spl/u-boot-spl-nodtb.bin spl/u-boot-spl.dtb spl/u-boot-spl-dtb.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) %{buildroot}%{_datadir}/uboot/$(echo $board)/
  fi
 done
done
%endif

# Bit of a hack to remove binaries we don't use as they're large
%ifarch aarch64
for board in $(ls builds)
do
  rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.dtb
  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot-sunxi-with-spl.bin ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot{,-dtb}.*
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
  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/idbloader.img ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.bin
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot{,-dtb}.img
  fi
done
%endif
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
cp -p board/rockchip/evb_rk3399/README builds/docs/README.evb_rk3399
cp -p board/sunxi/README.sunxi64 builds/docs/README.sunxi64
cp -p board/sunxi/README.nand builds/docs/README.sunxi-nand

%files
%doc README doc/develop/distro.rst doc/README.gpt
%doc doc/README.rockchip doc/develop/uefi doc/uImage.FIT doc/arch/arm64.rst
%doc builds/docs/* doc/board/amlogic/ doc/board/rockchip/
%{_bindir}/*
%{_mandir}/man1/mkimage.1*
%dir %{_datadir}/uboot/

%if %{with toolsonly}
%ifarch aarch64
%files -n uboot-images-armv8
%{_datadir}/uboot/*
%endif

%ifarch riscv64
%files -n uboot-images-riscv64
%{_datadir}/uboot/*
%endif
%endif

%changelog
* Sun Nov 20 2022 David Abdurachmanov <davidlt@rivosinc.com> - 2022.10-1.1.riscv64
- Actually build riscv64 binaries

* Thu Nov 17 2022 David Abdurachmanov <davidlt@rivosinc.com> - 2022.10-1.0.riscv64
- Add support for riscv64

* Mon Oct 10 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.10-1
- Update to 2022.10 GA

* Tue Sep 06 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.10-0.6.rc4
- Update SMBIOS patch

* Tue Sep 06 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.10-0.5.rc4
- Update to 2022.10 RC4
- Fix for booting Rockchip devices from NVME

* Tue Aug 23 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.10-0.4.rc3
- Update to 2022.10 RC3

* Mon Aug 22 2022 Davide Cavalca <dcavalca@fedoraproject.org> - 2022.10-0.3.rc1
- Install nodtb variant for Apple M1 (rhbz#2068958)

* Tue Aug 16 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.10-0.2.rc1
- Fix for DT property propogation via firmware

* Thu Jul 28 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.10-0.1.rc1
- Update to 2022.10 RC1
- Enable LTO for firmware builds

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2022.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 17 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.07-1
- Update to 2022.07 GA

* Mon Jul 04 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.07-0.6.rc6
- Update to 2022.07 RC6

* Mon Jun 20 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.07-0.5.rc5
- Update to 2022.07 RC5

* Sun Jun 12 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.07-0.4.rc4
- Update to 2022.07 RC4
- Some minor Rockchips device fixes

* Wed May 25 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.07-0.3.rc3
- Update to 2022.07 RC3

* Sat May 14 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.07-0.2.rc2
- Update to 2022.07 RC2

* Tue Apr 26 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.07-0.1.rc1
- Update to 2022.07 RC1

* Mon Apr 04 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.04-1
- Update to 2022.04 GA

* Mon Mar 28 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.04-0.4.rc5
- Update to 2022.04 RC5

* Tue Mar 08 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.04-0.3.rc3
- Update to 2022.04 RC3
- Enable new Rockchip devices

* Tue Feb 15 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.04-0.2.rc2
- Update to 2022.04 RC2

* Wed Feb 02 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.04-0.1.rc1
- Update to 2022.04 RC1

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2022.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.01-1
- Update to 2022.01

* Wed Jan 05 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.01-0.3.rc4
- Upstream fixes for PHY and UEFI

* Mon Dec 20 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.01-0.2.rc4
- Update to 2022.01 RC4

* Mon Nov 15 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2022.01-0.1.rc2
- Update to 2022.01 RC2

* Mon Nov 15 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.10-3
- Fixes for rk3399 devices

* Thu Oct 14 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.10-2
- Fix booting from MMC for Rockchip 3399 (rhbz #2014182)
- Enable new rk3399 devices (Leez, NanoPi-M4B, NanoPi-4S, NanoPi-T4) (rhbz #2009126)

* Mon Oct 04 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.10-1
- Update to 2021.10

* Mon Sep 27 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.10-0.7.rc5
- Update to 2021.10 RC5

* Wed Sep 15 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.10-0.6.rc4
- Update to 2021.10 RC4
- Proposed fix for RPi MMC clock issue

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2021.10-0.6.rc3
- Rebuilt with OpenSSL 3.0.0

* Mon Aug 30 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.10-0.5.rc3
- Update to 2021.10 RC3

* Tue Aug 24 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.10-0.4.rc2
- Fix for Raspberry Pi firmware properties

* Mon Aug 23 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.10-0.3.rc2
- Fix for rockchip SPI

* Mon Aug 16 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.10-0.2.rc2
- Update to 2021.10 RC2

* Sun Aug 08 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.10-0.1.rc1
- Update to 2021.10 RC1

* Thu Jul 22 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.07-2
- Fix regression for Rockchip devices running firmware from SPI flash

* Mon Jul 05 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.07-1
- Update to 2021.07 GA

* Mon Jun 28 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.07-0.6.rc5
- Update to 2021.07 RC5
- Build SPI fash images for ROC-PC-RK3399

* Mon Jun 07 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.07-0.5.rc4
- Update to 2021.07 RC4

* Sat Jun 05 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.07-0.4.rc3
- Fix AllWinner devices booting from mSD/MMC

* Tue May 25 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.07-0.3.rc3
- Update to 2021.07 RC3
- Build against ATF 2.5 GA

* Thu May 13 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.07-0.2.rc2
- Build against new ATF 2.5-rc1

* Mon May 10 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.07-0.1.rc2
- Update to 2021.07 RC2

* Wed Apr 28 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.04-3
- Upstream fix for console regression (rhbz 1946278)
- Fix for fallback.efi crash (rhbz 1733817)

* Wed Apr 21 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.04-2
- Revert keyboard console regression change (rhbz 1946278)

* Sun Apr 18 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2021.04-1
- Update to 2021.04 GA
- Fix DTB load check (rhbz 1946278)
- Build Rockchip SPI support as idbloader.spi
- Fixes for Rockchip devices
- Build Turris Omnia for MMC/SPI/UART

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
