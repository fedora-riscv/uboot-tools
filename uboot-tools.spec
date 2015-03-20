%global candidate rc4

Name:           uboot-tools
Version:        2015.04
Release:        0.2%{?candidate:.%{candidate}}%{?dist}
Summary:        U-Boot utilities

Group:          Development/Tools
License:        GPLv2+ BSD LGPL-2.1+ LGPL-2.0+
URL:            http://www.denx.de/wiki/U-Boot
Source0:        ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}%{?candidate:-%{candidate}}.tar.bz2

Patch1:   0001-make-sure-that-the-filesystem-is-a-type-of-fat.patch
Patch2:   0002-Add-BOOTENV_POST_COMMAND-which-is-appended-to-the-en.patch
Patch3:   0003-Only-set-CONFIG_BOOTDELAY-if-not-already-set.patch
Patch4:   0004-Switch-am335x_evm.h-to-use-config_distro_defaults-an.patch
Patch5:   0005-add-back-adding-console-to-the-bootargs-if-not-prese.patch
Patch6:   0006-wandboard-port-to-generic-distro-booting.patch
Patch7:   0007-Switch-omap4-boards-to-use-config_distro_defaults-an.patch
Patch8:   0008-port-utilite-to-distro-generic-boot-commands.patch
Patch9:   0009-RiOT-board-set-console-speed.patch
Patch10:  0010-Add-support-for-loading-environment-from-uEnv.txt-in.patch
Patch11:  0011-Add-BOOTENV_INIT_COMMAND-for-commands-that-may-be-ne.patch
Patch12:  0012-beagle-board-use-ext-support-in-the-SPL.patch

BuildRequires:  dtc, openssl-devel
BuildRequires:  fedora-logos, netpbm-progs
BuildRequires:  git
Requires:       dtc

%description
This package contains a few U-Boot utilities - mkimage for creating boot images
and fw_printenv/fw_setenv for manipulating the boot environment variables.

%ifarch aarch64
%package     -n uboot-images-armv8
Summary:     u-boot bootloader images for armv8 boards
Requires:    uboot-tools

%description -n uboot-images-armv8
u-boot bootloader binaries for the aarch64 vexpress_aemv8a
%endif

%ifarch %{arm}
%package     -n uboot-images-armv7
Summary:     u-boot bootloader images for armv7 boards
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

git init 
git config user.email "noone@example.com" 
git config user.name "no one" 
git add . 
git commit -a -q -m "%{version} baseline" 
git am %{patches} </dev/null 
git config --unset user.email 
git config --unset user.name 

rm -rf .git

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
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot.bin builds/u-boot.bin.vexpress_aemv8a
make mrproper

%endif

%ifarch %{arm}
make db-mv784mp-gp_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot.img builds/u-boot.img.db-mv784mp-gp
cp -p u-boot-spl.kwb builds/u-boot-spl.kwb.db-mv784mp-gp
make mrproper

# AllWinner devices
make Bananapi_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.Bananapi
make mrproper

make Bananapro_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.Bananapro
make mrproper

make Cubieboard_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.Cubieboard
make mrproper

make Cubieboard2_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.Cubieboard2
make mrproper

make Cubietruck_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.Cubietruck
make mrproper

make Mele_A1000_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.Mele_A1000
make mrproper

make Mele_M3_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.Mele_M3
make mrproper

make Mini-X_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.Mini-X
make mrproper

make A10-OLinuXino-Lime_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.A10-OLinuXino-Lime
make mrproper

make A20-OLinuXino-Lime_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.A20-OLinuXino-Lime
make mrproper

make A20-OLinuXino-Lime2_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.A20-OLinuXino-Lime2
make mrproper

make A10s-OLinuXino-M_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.A10s-OLinuXino-M
make mrproper

make A13-OLinuXino_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.A13-OLinuXino
make mrproper

make A13-OLinuXinoM_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.A13-OLinuXinoM
make mrproper

make A20-OLinuXino_MICRO_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.A20-OLinuXino_MICRO
make mrproper

# Calxeda
make highbank_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot.bin builds/u-boot.bin.highbank
make mrproper

# Freescale i.MX6
make cm_fx6_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot.img builds/u-boot.img.cm_fx6
cp -p SPL builds/SPL.cm_fx6
make mrproper

make hummingboard_solo_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot.imx builds/u-boot.imx.hummingboard
make mrproper

make novena_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot.img builds/u-boot.imx.novena
make mrproper

make riotboard_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot.imx builds/u-boot.imx.riotboard
make mrproper

make udoo_quad_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot.imx builds/u-boot.imx.udoo_quad
make mrproper

make wandboard_dl_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot.imx builds/u-boot.imx.wandboard_dl
make mrproper

make wandboard_quad_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot.imx builds/u-boot.imx.wandboard_quad
make mrproper

make wandboard_solo_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot.imx builds/u-boot.imx.wandboard_solo
make mrproper

# NVidia Tegra devices
make jetson-tk1_defconfig
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-dtb-tegra.bin builds/u-boot-dtb-tegra.bin.jetson-tk1
cp -p u-boot-nodtb-tegra.bin builds/u-boot-nodtb-tegra.bin.jetson-tk1
cp -p u-boot.map builds/u-boot.map.jetson-tk1
cp -p u-boot.dtb builds/u-boot.dtb.jetson-tk1
make mrproper

make paz00_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-dtb-tegra.bin builds/u-boot-dtb-tegra.bin.paz00
cp -p u-boot-nodtb-tegra.bin builds/u-boot-nodtb-tegra.bin.paz00
cp -p u-boot.map builds/u-boot.map.paz00
cp -p u-boot.dtb builds/u-boot.dtb.paz00
make mrproper

make trimslice_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-dtb-tegra.bin builds/u-boot-dtb-tegra.bin.trimslice
cp -p u-boot-nodtb-tegra.bin builds/u-boot-nodtb-tegra.bin.trimslice
cp -p u-boot.map builds/u-boot.map.trimslice
cp -p u-boot.dtb builds/u-boot.dtb.trimslice
make mrproper

# Samsung Exynos devices
make arndale_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p spl/arndale-spl.bin builds/arndale-spl.bin.arndale
cp -p u-boot-dtb.bin builds/u-boot-dtb.bin.arndale
make mrproper

make origen_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p spl/origen-spl.bin builds/origen-spl.bin.origen
cp -p u-boot.bin builds/u-boot.bin.origen
cp -p u-boot-dtb.bin builds/u-boot-dtb.bin.origen
make mrproper

make smdkv310_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p spl/smdkv310-spl.bin builds/smdkv310-spl.bin.smdkv310
cp -p u-boot.bin builds/u-boot.bin.smdkv310
make mrproper

make snow_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot-dtb.bin builds/u-boot-dtb.bin.snow
make mrproper

# ST Erikson
make snowball_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p u-boot.bin builds/u-boot.bin.snowball
make mrproper

# TI devices
make am335x_boneblack_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p MLO builds/MLO.beaglebone
cp -p u-boot.img builds/u-boot.img.beaglebone
make mrproper

make omap3_beagle_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p MLO builds/MLO.beagle
cp -p u-boot.img builds/u-boot.img.beagle
make mrproper

make omap4_panda_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p MLO builds/MLO.panda
cp -p u-boot.img builds/u-boot.img.panda
make mrproper

make omap5_uevm_config
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1
cp -p MLO builds/MLO.uevm
cp -p u-boot.img builds/u-boot.img.uevm
make mrproper

%endif

make HOSTCC="gcc $RPM_OPT_FLAGS" %{?_smp_mflags} CROSS_COMPILE="" defconfig V=1
make HOSTCC="gcc $RPM_OPT_FLAGS" %{?_smp_mflags} CROSS_COMPILE="" silentoldconfig V=1
make HOSTCC="gcc $RPM_OPT_FLAGS" %{?_smp_mflags} CROSS_COMPILE="" tools-only V=1

%ifarch %{arm}
make HOSTCC="gcc $RPM_OPT_FLAGS" %{?_smp_mflags} CROSS_COMPILE="" sheevaplug_config V=1
make HOSTCC="gcc $RPM_OPT_FLAGS" %{?_smp_mflags} CROSS_COMPILE="" env V=1
%endif

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1

%ifarch aarch64
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/vexpress_aemv8a/

install -p -m 0644 builds/u-boot.bin.vexpress_aemv8a $RPM_BUILD_ROOT%{_datadir}/uboot/vexpress_aemv8a/u-boot.bin
%endif

%ifarch %{arm}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/
for board in A10-OLinuXino-Lime A10s-OLinuXino-M A13-OLinuXino A13-OLinuXinoM A20-OLinuXino_MICRO A20-OLinuXino-Lime A20-OLinuXino-Lime2 arndale Bananapi Bananapro beagle beaglebone cm_fx6 Cubieboard Cubieboard2 Cubietruck highbank jetson-tk1 Mele_A1000 Mele_M3 Mini-X origen panda paz00 riotboard smdkv310 snow snowball trimslice udoo_quad uevm vexpress wandboard_dl wandboard_quad wandboard_solo db-mv784mp-gp
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
done

# AllWinner
for board in Bananapi Bananapro Cubieboard Cubieboard2 Cubietruck Mele_A1000 Mele_M3 Mini-X A10-OLinuXino-Lime A10s-OLinuXino-M A13-OLinuXino A13-OLinuXinoM A20-OLinuXino_MICRO A20-OLinuXino-Lime A20-OLinuXino-Lime2
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
install -p -m 0644 builds/u-boot-sunxi-with-spl.bin.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot-sunxi-with-spl.bin
done

# Calxeda
install -p -m 0644 builds/u-boot.bin.highbank $RPM_BUILD_ROOT%{_datadir}/uboot/highbank/u-boot.bin

# FreeScale
for board in cm_fx6
do
install -p -m 0644 builds/u-boot.img.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.img
install -p -m 0644 builds/SPL.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/SPL
done

for board in hummingboard novena riotboard udoo_quad wandboard_dl wandboard_quad wandboard_solo
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
install -p -m 0644 builds/u-boot.imx.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.imx
done

# NVidia
for board in paz00 trimslice jetson-tk1
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
install -p -m 0644 builds/u-boot-nodtb-tegra.bin.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot-nodtb-tegra.bin
install -p -m 0644 builds/u-boot-dtb-tegra.bin.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot-dtb-tegra.bin
install -p -m 0644 builds/u-boot.map.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.map
install -p -m 0644 builds/u-boot.dtb.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.dtb
done

# Samsung
#without dtb
for board in smdkv310
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
install -p -m 0644 builds/$(echo $board)-spl.bin.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/$(echo $board)-spl.bin
install -p -m 0644 builds/u-boot.bin.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.bin
done
#with dtb
for board in arndale origen
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
install -p -m 0644 builds/$(echo $board)-spl.bin.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/$(echo $board)-spl.bin
install -p -m 0644 builds/u-boot-dtb.bin.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot-dtb.bin
done

install -p -m 0644 builds/u-boot-dtb.bin.snow $RPM_BUILD_ROOT%{_datadir}/uboot/snow/u-boot-dtb.bin

# STE
install -p -m 0644 builds/u-boot.bin.snowball $RPM_BUILD_ROOT%{_datadir}/uboot/snowball/u-boot.bin

# TI
for board in beaglebone beagle panda uevm
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
install -p -m 0644 builds/u-boot.img.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.img
install -p -m 0644 builds/MLO.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/MLO
done

for board in db-mv784mp-gp
do
install -p -m 0644 builds/u-boot.img.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.img
install -p -m 0644 builds/u-boot-spl.kwb.$(echo $board) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.kwb
done

%endif

install -p -m 0755 tools/mkimage $RPM_BUILD_ROOT%{_bindir}
install -p -m 0644 doc/mkimage.1 $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m 0755 tools/mkenvimage $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 tools/dumpimage $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 tools/fit_info $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 tools/fit_check_sign $RPM_BUILD_ROOT%{_bindir}

%ifarch %{arm}
install -p -m 0755 tools/env/fw_printenv $RPM_BUILD_ROOT%{_bindir}
( cd $RPM_BUILD_ROOT%{_bindir}; ln -sf fw_printenv fw_setenv )

install -p -m 0644 tools/env/fw_env.config $RPM_BUILD_ROOT%{_sysconfdir}
%endif


%files
%doc README doc/README.imximage doc/README.kwbimage doc/uImage.FIT
%{_bindir}/fit_check_sign
%{_bindir}/fit_info
%{_bindir}/mkimage
%{_bindir}/mkenvimage
%{_bindir}/dumpimage
%{_mandir}/man1/mkimage.1*
%ifarch %{arm} aarch64
%dir %{_datadir}/uboot/
%endif
%ifarch %{arm}
%{_bindir}/fw_printenv
%{_bindir}/fw_setenv
%config(noreplace) %{_sysconfdir}/fw_env.config
%endif

%ifarch aarch64
%files -n uboot-images-armv8
%{_datadir}/uboot/vexpress_aemv8a/
%endif

%ifarch %{arm}
%files -n uboot-images-armv7
# AllWinner
%{_datadir}/uboot/Bananapi/
%{_datadir}/uboot/Bananapro/
%{_datadir}/uboot/Cubieboard/
%{_datadir}/uboot/Cubieboard2/
%{_datadir}/uboot/Cubietruck/
%{_datadir}/uboot/Mele_A1000/
%{_datadir}/uboot/Mele_M3/
%{_datadir}/uboot/Mini-X/
%{_datadir}/uboot/A10-OLinuXino-Lime/
%{_datadir}/uboot/A10s-OLinuXino-M/
%{_datadir}/uboot/A13-OLinuXino/
%{_datadir}/uboot/A13-OLinuXinoM/
%{_datadir}/uboot/A20-OLinuXino_MICRO/
%{_datadir}/uboot/A20-OLinuXino-Lime/
%{_datadir}/uboot/A20-OLinuXino-Lime2/
# Calxeda
%{_datadir}/uboot/highbank/
# FreeScale
%{_datadir}/uboot/cm_fx6/
%{_datadir}/uboot/hummingboard/
%{_datadir}/uboot/novena/
%{_datadir}/uboot/riotboard/
%{_datadir}/uboot/wandboard_dl/
%{_datadir}/uboot/wandboard_quad/
%{_datadir}/uboot/wandboard_solo/
%{_datadir}/uboot/udoo_quad/
# NVidia
%{_datadir}/uboot/jetson-tk1/
%{_datadir}/uboot/paz00/
%{_datadir}/uboot/trimslice/
# Samsung
%{_datadir}/uboot/arndale/
%{_datadir}/uboot/smdkv310/
%{_datadir}/uboot/snow/
# STE
%{_datadir}/uboot/snowball/
# TI
%{_datadir}/uboot/beagle/
%{_datadir}/uboot/beaglebone/
%{_datadir}/uboot/origen/
%{_datadir}/uboot/panda/
%{_datadir}/uboot/uevm/
#Marvell
%{_datadir}/uboot/db-mv784mp-gp/
%endif

%changelog
* Fri Mar 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2015.04-0.2.rc4
- Update to 2015.04 rc3

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
