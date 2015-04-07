%global candidate rc5

Name:           uboot-tools
Version:        2015.04
Release:        0.6%{?candidate:.%{candidate}}%{?dist}
Summary:        U-Boot utilities

Group:          Development/Tools
License:        GPLv2+ BSD LGPL-2.1+ LGPL-2.0+
URL:            http://www.denx.de/wiki/U-Boot
Source0:        ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}%{?candidate:-%{candidate}}.tar.bz2
Source1:        armv7-boards

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
Patch13:  0013-WANDBOARD-run-the-dsitro-bootcmd-first-before-fallin.patch
Patch14:  0014-BBB-tell-u-boot-to-look-in-the-first-partition-to-lo.patch
Patch15:  0001-omap4-distro-boot-partition-fixup.patch

BuildRequires:  dtc, openssl-devel
BuildRequires:  fedora-logos, netpbm-progs
BuildRequires:  git, bc
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
make vexpress_aemv8a_juno_config vexpress_aemv8a_semi_config O=builds/vexpress_aemv8a/
make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1 O=builds/vexpress_aemv8a/
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
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/vexpress_aemv8a/

install -p -m 0644 builds/vexpress_aemv8a/u-boot.bin $RPM_BUILD_ROOT%{_datadir}/uboot/vexpress_aemv8a/
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
%doc README doc/README.imximage doc/README.kwbimage doc/uImage.FIT
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
