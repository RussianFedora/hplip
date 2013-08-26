# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}

Summary: HP Linux Imaging and Printing Project
Name: hplip
Version: 3.13.7
Release: 1%{?dist}
License: GPLv2+ and MIT
Group: System Environment/Daemons

Url: http://hplip.sourceforge.net/
Source0: http://downloads.sourceforge.net/sourceforge/hplip/hplip-%{version}.tar.gz
Source1: hpcups-update-ppds.sh
Source2: copy-deviceids.py
Patch1: hplip-pstotiff-is-rubbish.patch
Patch2: hplip-strstr-const.patch
Patch3: hplip-ui-optional.patch
Patch4: hplip-no-asm.patch
Patch5: hplip-deviceIDs-drv.patch
Patch6: hplip-mucks-with-spooldir.patch
Patch7: hplip-udev-rules.patch
Patch8: hplip-retry-open.patch
Patch9: hplip-snmp-quirks.patch
Patch10: hplip-discovery-method.patch
Patch11: hplip-hpijs-marker-supply.patch
Patch12: hplip-clear-old-state-reasons.patch
Patch13: hplip-systray-dbus-exception.patch
Patch14: hplip-hpcups-sigpipe.patch
Patch15: hplip-logdir.patch
Patch16: hplip-bad-low-ink-warning.patch
Patch17: hplip-deviceIDs-ppd.patch
Patch18: hplip-skip-blank-lines.patch
Patch19: hplip-dbglog-newline.patch
Patch21: hplip-ppd-ImageableArea.patch
Patch22: hplip-raw_deviceID-traceback.patch
Patch23: hplip-UnicodeDecodeError.patch
Patch24: hplip-addprinter.patch
Patch25: hplip-dbus-exception.patch
Patch26: hplip-notification-exception.patch
Patch28: hplip-wifisetup.patch
Patch29: hplip-makefile-chgrp.patch
Patch30: hplip-hpaio-localonly.patch
Patch31: hplip-IEEE-1284-4.patch
Patch32: hplip-check.patch
Patch33: hplip-mkstemp.patch

Patch99: hplip-3.13.7-rfremixify.patch

%global hpijs_epoch 1
Requires: hpijs%{?_isa} = %{hpijs_epoch}:%{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: python-imaging
Requires: cups
Requires: wget
Requires: dbus-python

BuildRequires: net-snmp-devel
BuildRequires: cups-devel
BuildRequires: python2-devel
BuildRequires: libjpeg-devel
BuildRequires: desktop-file-utils
BuildRequires: libusb1-devel
BuildRequires: openssl-devel
BuildRequires: sane-backends-devel
BuildRequires: dbus-devel

# Make sure we get postscriptdriver tags.
BuildRequires: python-cups, cups

%description
The Hewlett-Packard Linux Imaging and Printing Project provides
drivers for HP printers and multi-function peripherals.

%package common
Summary: Files needed by the HPLIP printer and scanner drivers
Group: System Environment/Libraries
License: GPLv2+
# /usr/lib/udev/rules.d
Requires: systemd

%description common
Files needed by the HPLIP printer and scanner drivers.

%package libs
Summary: HPLIP libraries
Group: System Environment/Libraries
License: GPLv2+ and MIT
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Requires: python

%description libs
Libraries needed by HPLIP.

%package gui
Summary: HPLIP graphical tools
Group: Applications/System
License: BSD
Requires: PyQt4
Requires: python-reportlab
Requires: pygobject2
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libsane-hpaio%{?_isa} = %{version}-%{release}

%description gui
HPLIP graphical tools.

%package -n hpijs
Summary: HP Printer Drivers
Group: Applications/Publishing
License: BSD
Epoch: %{hpijs_epoch}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: cups >= 1:1.4

%description -n hpijs
hpijs is a collection of optimized drivers for HP printers.
hpijs supports the DeskJet 350C, 600C, 600C Photo, 630C, Apollo 2000,
Apollo 2100, Apollo 2560, DeskJet 800C, DeskJet 825, DeskJet 900,
PhotoSmart, DeskJet 990C, and PhotoSmart 100 series.

%package -n libsane-hpaio
Summary: SANE driver for scanners in HP's multi-function devices
Group: System Environment/Daemons
License: GPLv2+
Obsoletes: libsane-hpoj < 0.91
Provides: libsane-hpoj = 0.91
Requires: sane-backends
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description -n libsane-hpaio
SANE driver for scanners in HP's multi-function devices (from HPOJ).

%prep
%setup -q

# The pstotiff filter is rubbish so replace it (launchpad #528394).
%patch1 -p1 -b .pstotiff-is-rubbish

# Fix compilation.
%patch2 -p1 -b .strstr-const

# Make utils.checkPyQtImport() look for the gui sub-package (bug #243273).
%patch3 -p1 -b .ui-optional

# Make sure to avoid handwritten asm.
%patch4 -p1 -b .no-asm

# Corrected several IEEE 1284 Device IDs using foomatic data.
# Color LaserJet CM1312nfi (bug #581005)
# Color LaserJet 3800 (bug #581935)
# Color LaserJet 2840 (bug #582215)
# Color LaserJet CP1518ni (bug #613689)
# Color LaserJet 2600n (bug #613712)
# Color LaserJet 2500/3700/4550/4600/4650/4700/5550/CP1515n/CP2025n
#                CP3525/CP4520 Series/CM2320nf (bug #659040)
# Color LaserJet CP2025dn (bug #651509)
# Color LaserJet CM4730 MFP (bug #658831)
# Color LaserJet CM3530 MFP (bug #659381)
# LaserJet 4050 Series/4100 Series/2100 Series/4350/5100 Series/8000 Series
#          P3005/P3010 Series/P4014/P4515 (bug #659039)
# LaserJet Professional P1606dn (bug #708472)
# LaserJet Professional M1212nf MFP (bug #742490)
# LaserJet M1536dnf MFP (bug #743915)
# LaserJet M1522nf MFP (bug #745498)
# LaserJet M1319f MFP (bug #746614)
# LaserJet M1120 MFP (bug #754139)
# LaserJet P1007 (bug #585272)
# LaserJet P1505 (bug #680951)
# LaserJet P2035 (Ubuntu #917703)
# PSC 1600 series (bug #743821)
# Officejet 6300 series (bug #689378)
# LaserJet Professional P1102w (bug #795958)
# Color LaserJet CM4540 MFP (bug #968177)
# Color LaserJet cp4005 (bug #980976)
%patch5 -p1 -b .deviceIDs-drv
chmod +x %{SOURCE2}
mv prnt/drv/hpijs.drv.in{,.deviceIDs-drv-hpijs}
%{SOURCE2} prnt/drv/hpcups.drv.in \
           prnt/drv/hpijs.drv.in.deviceIDs-drv-hpijs \
           > prnt/drv/hpijs.drv.in

# Stopped hpcups pointlessly trying to read spool files
# directly (bug #552572).
%patch6 -p1 -b .mucks-with-spooldir

# Don't add printer queue, just check plugin.
# Move udev rules from /etc/ to /usr/lib/ (bug #748208).
%patch7 -p1 -b .udev-rules

# Retry when connecting to device fails (bug #532112).
%patch8 -p1 -b .retry-open

# Mark SNMP quirks in PPD for HP OfficeJet Pro 8500 (bug #581825).
%patch9 -p1 -b .snmp-quirks

# Fixed hp-setup traceback when discovery page is skipped (bug #523685).
%patch10 -p1 -b .discovery-method

# Fixed bogus low ink warnings from hpijs driver (bug #643643).
%patch11 -p1 -b .hpijs-marker-supply

# Clear old printer-state-reasons we used to manage (bug #510926).
%patch12 -p1 -b .clear-old-state-reasons

# Catch DBusException in hp-systray (bug #746024).
%patch13 -p1 -b .systray-dbus-exception

# Avoid busy loop in hpcups when backend has exited (bug #525944).
%patch14 -p1 -b .hpcups-sigpipe

# CUPS filters should use TMPDIR when available (bug #865603).
%patch15 -p1 -b .logdir

# Fixed Device ID parsing code in hpijs's dj9xxvip.c (bug #510926).
%patch16 -p1 -b .bad-low-ink-warning

# Add Device ID for
# LaserJet 1200 (bug #577308)
# LaserJet 1320 series (bug #579920)
# LaserJet 2300 (bug #576928)
# LaserJet P2015 Series (bug #580231)
# LaserJet 4250 (bug #585499)
# Color LaserJet 2605dn (bug #583953)
# Color LaserJet 3800 (bug #581935)
# Color LaserJet 2840 (bug #582215)
# LaserJet 4050 Series/4100 Series/2100 Series/2420/4200/4300/4350/5100 Series
#          8000 Series/M3027 MFP/M3035 MFP/P3005/P3010 Series (bug #659039)
# Color LaserJet 2500/2550/2605dn/3700/4550/4600
#                4650/4700/5550/CP3525 (bug #659040)
# Color LaserJet CM4730 MFP (bug #658831)
# Color LaserJet CM3530 MFP (bug #659381)
# Designjet T770 (bug #747957)
# Color LaserJet CM4540 MFP (bug #968177)
# Color LaserJet cp4005 (bug #980976)
for ppd_file in $(grep '^diff' %{PATCH17} | cut -d " " -f 4);
do
  gunzip ${ppd_file#*/}.gz
done
%patch17 -p1 -b .deviceIDs-ppd
for ppd_file in $(grep '^diff' %{PATCH17} | cut -d " " -f 4);
do
  gzip -n ${ppd_file#*/}
done

# Hpcups (ljcolor) was putting black lines where should be blank lines (bug #579461).
%patch18 -p1 -b .skip-blank-lines

# Added missing newline to string argument in dbglog() call (bug #585275).
%patch19 -p1 -b .dbglog-newline

# Fix ImageableArea for Laserjet 8150/9000 (bug #596298).
for ppd_file in $(grep '^diff' %{PATCH21} | cut -d " " -f 4);
do
  gunzip ${ppd_file#*/}.gz
done
%patch21 -p1 -b .ImageableArea
for ppd_file in $(grep '^diff' %{PATCH21} | cut -d " " -f 4);
do
  gzip -n ${ppd_file#*/}
done

# Fixed traceback on error condition in device.py (bug #628125).
%patch22 -p1 -b .raw_deviceID-traceback

# Avoid UnicodeDecodeError in printsettingstoolbox.py (bug #645739).
%patch23 -p1 -b .UnicodeDecodeError

# Call cupsSetUser in cupsext's addPrinter method before connecting so
# that we can get an authentication callback (bug #538352).
%patch24 -p1 -b .addprinter

# Catch D-Bus exceptions in fax dialog (bug #645316).
%patch25 -p1 -b .dbus-exception

# Catch GError exception when notification showing failed (bug #665577).
%patch26 -p1 -b .notification-exception

# Avoid KeyError in ui4/wifisetupdialog.py (bug #680939).
%patch28 -p1 -b .wifisetup

# Don't run 'chgrp lp /var/log/hp' and 'chgrp lp /var/log/hp/tmp' in makefile
%patch29 -p1 -b .chgrp

# Pay attention to the SANE localOnly flag in hpaio (bug #743593).
%patch30 -p1 -b .hpaio-localonly

# Support IEEE 1284.4 protocol over USB (bug #858861).
%patch31 -p1 -b .hplip-IEEE-1284-4

# Various adjustments to make 'hp-check' run more smoothly (bug #683007).
%patch32 -p1 -b .check

# Avoid several bugs in createTempFile (bug #925032).
%patch33 -p1 -b .mkstemp

# Support RFRemix
%patch99 -p1 -b .rfremixify

sed -i.duplex-constraints \
    -e 's,\(UIConstraints.* \*Duplex\),//\1,' \
    prnt/drv/hpcups.drv.in

# Change shebang /usr/bin/env python -> /usr/bin/python (bug #618351).
find -name '*.py' -print0 | xargs -0 \
    sed -i.env-python -e 's,^#!/usr/bin/env python,#!/usr/bin/python,'

%build
%configure \
        --enable-scan-build --enable-gui-build --enable-fax-build \
        --disable-foomatic-rip-hplip-install --enable-pp-build \
        --enable-qt4 --enable-hpcups-install --enable-cups-drv-install \
        --enable-foomatic-drv-install \
        --enable-hpijs-install --enable-udev-acl-rules \
        --disable-policykit --with-mimedir=%{_datadir}/cups/mime

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make

%install
mkdir -p %{buildroot}%{_bindir}
make install DESTDIR=%{buildroot}

# Create /var/run/hplip
mkdir -p %{buildroot}%{_localstatedir}/run/hplip

# Remove unpackaged files
rm -rf  %{buildroot}%{_sysconfdir}/sane.d \
        %{buildroot}%{_docdir} \
        %{buildroot}%{_datadir}/hal/fdi \
        %{buildroot}%{_datadir}/hplip/pkservice.py \
        %{buildroot}%{_bindir}/hp-pkservice

rm -f   %{buildroot}%{_bindir}/foomatic-rip \
        %{buildroot}%{_libdir}/cups/filter/foomatic-rip \
        %{buildroot}%{_libdir}/*.la \
        %{buildroot}%{python_sitearch}/*.la \
        %{buildroot}%{_libdir}/libhpip.so \
        %{buildroot}%{_libdir}/sane/*.la \
        %{buildroot}%{_datadir}/cups/model/foomatic-ppds \
        %{buildroot}%{_datadir}/applications/hplip.desktop \
        %{buildroot}%{_datadir}/ppd/HP/*.ppd

mkdir -p %{buildroot}%{_datadir}/applications
sed -i -e '/^Categories=/d' hplip.desktop
# Encoding key is deprecated
sed -i -e '/^Encoding=/d' hplip.desktop
desktop-file-install --vendor HP                                \
        --dir %{buildroot}%{_datadir}/applications              \
        --add-category System                                   \
        --add-category Settings                                 \
        --add-category HardwareSettings                         \
        hplip.desktop

# Regenerate hpcups PPDs on upgrade if necessary (bug #579355).
install -p -m755 %{SOURCE1} %{buildroot}%{_bindir}/hpcups-update-ppds

%{__mkdir_p} %{buildroot}%{_sysconfdir}/sane.d/dll.d
echo hpaio > %{buildroot}%{_sysconfdir}/sane.d/dll.d/hpaio

# Images in docdir should not be executable (bug #440552).
find doc/images -type f -exec chmod 644 {} \;

# Create an empty plugins directory to make sure it gets the right
# SELinux file context (bug #564551).
%{__mkdir_p} %{buildroot}%{_datadir}/hplip/prnt/plugins

# Remove files we don't want to package.
rm -f %{buildroot}%{_datadir}/hplip/hpaio.desc
rm -f %{buildroot}%{_datadir}/hplip/hplip-install
rm -rf %{buildroot}%{_datadir}/hplip/install.*
rm -f %{buildroot}%{_datadir}/hplip/uninstall.*
rm -f %{buildroot}%{_bindir}/hp-uninstall
rm -f %{buildroot}%{_datadir}/hplip/upgrade.*
rm -f %{buildroot}%{_bindir}/hp-upgrade
rm -f %{buildroot}%{_bindir}/hp-config_usb_printer
rm -f %{buildroot}%{_unitdir}/hplip-printer@.service
rm -f %{buildroot}%{_datadir}/hplip/config_usb_printer.*
rm -f %{buildroot}%{_datadir}/hplip/hpijs.drv.in.template
rm -f %{buildroot}%{_datadir}/cups/mime/pstotiff.types
rm -f %{buildroot}%{_datadir}/hplip/fax/pstotiff*
rm -f %{buildroot}%{_cups_serverbin}/filter/hpcac

# The systray applet doesn't work properly (displays icon as a
# window), so don't ship the launcher yet.
rm -f %{buildroot}%{_sysconfdir}/xdg/autostart/hplip-systray.desktop

%files
%doc COPYING doc/*
%{_bindir}/hp-align
%{_bindir}/hp-clean
%{_bindir}/hp-colorcal
%{_bindir}/hp-devicesettings
%{_bindir}/hp-diagnose_plugin
%{_bindir}/hp-diagnose_queues
%{_bindir}/hp-doctor
%{_bindir}/hp-fab
%{_bindir}/hp-faxsetup
%{_bindir}/hp-firmware
%{_bindir}/hp-info
%{_bindir}/hp-levels
%{_bindir}/hp-linefeedcal
%{_bindir}/hp-logcapture
%{_bindir}/hp-makecopies
%{_bindir}/hp-makeuri
%{_bindir}/hp-mkuri
%{_bindir}/hp-plugin
%{_bindir}/hp-pqdiag
%{_bindir}/hp-printsettings
%{_bindir}/hp-probe
%{_bindir}/hp-query
%{_bindir}/hp-scan
%{_bindir}/hp-sendfax
%{_bindir}/hp-setup
%{_bindir}/hp-testpage
%{_bindir}/hp-timedate
%{_bindir}/hp-unload
%{_bindir}/hp-wificonfig
%{_cups_serverbin}/backend/hp
%{_cups_serverbin}/backend/hpfax
%{_cups_serverbin}/filter/pstotiff
%{_cups_serverbin}/filter/hpps
%{_datadir}/cups/mime/pstotiff.convs
# Files
%{_datadir}/hplip/align.py*
%{_datadir}/hplip/check-plugin.py*
%{_datadir}/hplip/clean.py*
%{_datadir}/hplip/colorcal.py*
%{_datadir}/hplip/devicesettings.py*
%{_datadir}/hplip/diagnose_plugin.py*
%{_datadir}/hplip/diagnose_queues.py*
%{_datadir}/hplip/doctor.py*
%{_datadir}/hplip/fab.py*
%{_datadir}/hplip/fax
%{_datadir}/hplip/faxsetup.py*
%{_datadir}/hplip/firmware.py*
%{_datadir}/hplip/hpdio.py*
%{_datadir}/hplip/hplip_clean.sh
%{_datadir}/hplip/hpssd*
%{_datadir}/hplip/info.py*
%{_datadir}/hplip/__init__.py*
%{_datadir}/hplip/levels.py*
%{_datadir}/hplip/linefeedcal.py*
%{_datadir}/hplip/logcapture.py*
%{_datadir}/hplip/makecopies.py*
%{_datadir}/hplip/makeuri.py*
%{_datadir}/hplip/plugin.py*
%{_datadir}/hplip/pqdiag.py*
%{_datadir}/hplip/printsettings.py*
%{_datadir}/hplip/probe.py*
%{_datadir}/hplip/query.py*
%{_datadir}/hplip/scan.py*
%{_datadir}/hplip/sendfax.py*
%{_datadir}/hplip/setup.py*
%{_datadir}/hplip/testpage.py*
%{_datadir}/hplip/timedate.py*
%{_datadir}/hplip/unload.py*
%{_datadir}/hplip/wificonfig.py*
# Directories
%{_datadir}/hplip/base
%{_datadir}/hplip/copier
%{_datadir}/hplip/data/ldl
%{_datadir}/hplip/data/localization
%{_datadir}/hplip/data/pcl
%{_datadir}/hplip/data/ps
%{_datadir}/hplip/installer
%{_datadir}/hplip/pcard
%{_datadir}/hplip/prnt
%{_datadir}/hplip/scan
%{_localstatedir}/lib/hp
%dir %attr(0774,root,lp) %{_localstatedir}/log/hp
%dir %attr(1774,root,lp) %{_localstatedir}/log/hp/tmp
%dir %attr(0775,root,lp) %{_localstatedir}/run/hplip

%files common
%doc COPYING
%{_prefix}/lib/udev/rules.d/*.rules
%dir %{_sysconfdir}/hp
%config(noreplace) %{_sysconfdir}/hp/hplip.conf
%dir %{_datadir}/hplip
%dir %{_datadir}/hplip/data
%{_datadir}/hplip/data/models

%files libs
%{_libdir}/libhpip.so.*
# The so symlink is required here (see bug #489059).
%{_libdir}/libhpmud.so*
# Python extension
%{python_sitearch}/*

%files gui
%{_bindir}/hp-check
%{_bindir}/hp-print
%{_bindir}/hp-systray
%{_bindir}/hp-toolbox
%{_datadir}/applications/*.desktop
# Files
%{_datadir}/hplip/check.py*
%{_datadir}/hplip/print.py*
%{_datadir}/hplip/systray.py*
%{_datadir}/hplip/toolbox.py*
# Directories
%{_datadir}/hplip/data/images
%{_datadir}/hplip/ui4

%files -n hpijs
%{_bindir}/hpijs
%{_bindir}/hpcups-update-ppds
%dir %{_datadir}/ppd/HP
%{_datadir}/ppd/HP/*.ppd.gz
%{_datadir}/cups/drv/*
%{_cups_serverbin}/filter/hpcups
%{_cups_serverbin}/filter/hpcupsfax
%{_cups_serverbin}/filter/hplipjs

%files -n libsane-hpaio
%{_libdir}/sane/libsane-*.so*
%config(noreplace) %{_sysconfdir}/sane.d/dll.d/hpaio

%post -n hpijs
%{_bindir}/hpcups-update-ppds &>/dev/null ||:

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%changelog
* Mon Aug 26 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 3.13.7-1.R
- support RFRemix

* Tue Jul 23 2013 Jiri Popelka <jpopelka@redhat.com> - 3.13.7-1
- 3.13.7
- Device IDs for CM4540 (bug #968177) and cp4005 (bug #980976).


* Mon Jun 24 2013 Jiri Popelka <jpopelka@redhat.com> - 3.13.6-2
- add one more arch-specific dependency.

* Mon Jun 24 2013 Jiri Popelka <jpopelka@redhat.com> - 3.13.6-1
- 3.13.6
- hplip-ipp-accessors.patch merged upstream
- /etc/cron.daily/hplip_cron -> /usr/share/hplip/hplip_clean.sh

* Wed May 29 2013 Tim Waugh <twaugh@redhat.com> - 3.13.5-2
- Avoid several bugs in createTempFile (bug #925032).

* Tue May 14 2013 Jiri Popelka <jpopelka@redhat.com> - 3.13.5-1
- 3.13.5
- change udev rule to not add printer queue, just check plugin.

* Fri May 10 2013 Jiri Popelka <jpopelka@redhat.com> - 3.13.4-3
- Device ID for HP LaserJet 2200 (bug #873123#c8).

* Thu Apr 11 2013 Tim Waugh <twaugh@redhat.com> - 3.13.4-2
- Fixed changelog dates.
- Device ID for HP LaserJet P1005 (bug #950776).
- mark cron job file as config(noreplace)

* Tue Apr 09 2013 Jiri Popelka <jpopelka@redhat.com> - 3.13.4-1
- 3.13.4

* Fri Mar 15 2013 Jiri Popelka <jpopelka@redhat.com> - 3.13.3-3
- Remove unused Requires.

* Thu Mar 14 2013 Tim Waugh <twaugh@redhat.com> - 3.13.3-2
- Moved hpfax pipe to /var/run/hplip (bug #917756).

* Fri Mar 08 2013 Jiri Popelka <jpopelka@redhat.com> - 3.13.3-1
- 3.13.3

* Thu Feb 14 2013 Jiri Popelka <jpopelka@redhat.com> - 3.13.2-1
- 3.13.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Jiri Popelka <jpopelka@redhat.com> - 3.12.11-7
- No need to run update-desktop-database (and require desktop-file-utils)
  because there are no MimeKey lines in the desktop files.

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 3.12.11-6
- rebuild due to "jpeg8-ABI" feature drop

* Fri Jan 18 2013 Jiri Popelka <jpopelka@redhat.com> 3.12.11-5
- Use arch-specific dependencies.
- Don't provide private python extension libs.

* Wed Jan 16 2013 Jiri Popelka <jpopelka@redhat.com> 3.12.11-4
- hpijs no longer requires net-snmp (bug #376641, bug #895643).

* Tue Jan 15 2013 Jiri Popelka <jpopelka@redhat.com> 3.12.11-3
- Use the form of import of PIL that is pillow compatible (bug #895266).

* Fri Dec 07 2012 Jiri Popelka <jpopelka@redhat.com> 3.12.11-2
- desktop file: remove deprecated Encoding key and Application category

* Tue Nov 27 2012 Jiri Popelka <jpopelka@redhat.com> 3.12.11-1
- 3.12.11
-- release-parport.patch merged upstream

* Thu Nov 22 2012 Tim Waugh <twaugh@redhat.com> 3.12.10-5.a
- Make 'hp-check' check for hpaio set-up correctly (bug #683007).

* Wed Oct 17 2012 Tim Waugh <twaugh@redhat.com> 3.12.10-4.a
- Some more CUPS filters using the wrong temporary directory
  (bug #865603).

* Tue Oct 16 2012 Tim Waugh <twaugh@redhat.com> 3.12.10-3.a
- CUPS filters should use TMPDIR when available (bug #865603).

* Thu Oct 11 2012 Jiri Popelka <jpopelka@redhat.com> 3.12.10-2.a
- 3.12.10a

* Thu Oct 04 2012 Jiri Popelka <jpopelka@redhat.com> 3.12.10-1
- 3.12.10

* Tue Oct 02 2012 Jiri Popelka <jpopelka@redhat.com> 3.12.9-6
- Ship %%{_localstatedir}/log/hp/tmp directory (bug #859658)

* Thu Sep 27 2012 Jiri Popelka <jpopelka@redhat.com> 3.12.9-5
- remove useless Conflicts:, Obsoletes: and Provides: fields
- remove %%pre section (stopping&disabling of hplip service on upgrade)
- make hplip_cron work with non-english locale

* Mon Sep 24 2012 Jiri Popelka <jpopelka@redhat.com> 3.12.9-4
- amend hplip-notification-exception.patch (bug #859543).

* Thu Sep 20 2012 Jiri Popelka <jpopelka@redhat.com> 3.12.9-3
- Support IEEE 1284.4 protocol over USB (bug #858861).

* Fri Sep 07 2012 Jiri Popelka <jpopelka@redhat.com> 3.12.9-2
- build against CUPS-1.6

* Fri Sep 07 2012 Jiri Popelka <jpopelka@redhat.com> 3.12.9-1
- 3.12.9
-- no longer needed: fax-ppd.patch

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Jiri Popelka <jpopelka@redhat.com> 3.12.6-1
- 3.12.6

* Tue Jun 05 2012 Jiri Popelka <jpopelka@redhat.com> 3.12.4-3
- Require systemd instead of udev.

* Mon Apr 30 2012 Tim Waugh <twaugh@redhat.com> 3.12.4-2
- The hpijs sub-package no longer requires cupsddk-drivers (which no
  longer exists as a real package), but cups >= 1.4.

* Thu Apr 12 2012 Jiri Popelka <jpopelka@redhat.com> 3.12.4-1
- 3.12.4

* Wed Mar 21 2012 Tim Waugh <twaugh@redhat.com> 3.12.2-4
- Release parport if unsupported model connected (bug #699052).

* Wed Feb 29 2012 Tim Waugh <twaugh@redhat.com> 3.12.2-3
- Added another IEEE 1284 Device ID for Color LaserJet CP2025dn to
  cope with its DNS-SD response, which has no usb_* keys (bug #651509).

* Wed Feb 22 2012 Tim Waugh <twaugh@redhat.com> 3.12.2-2
- Added IEEE 1284 Device ID for LaserJet Professional P1102w (bug #795958).

* Tue Feb 07 2012 Jiri Popelka <jpopelka@redhat.com> 3.12.2-1
- 3.12.2

* Wed Jan 18 2012 Jiri Popelka <jpopelka@redhat.com> 3.11.12-3
- Added IEEE 1284 Device ID for LaserJet P2035.

* Wed Jan 11 2012 Tim Waugh <twaugh@redhat.com> 3.11.12-2
- When copying Device IDs from hpcups to hpijs, use ModelName as the
  key instead of ShortNickName (bug #651509 comment #7).

* Mon Dec 19 2011 Jiri Popelka <jpopelka@redhat.com> 3.11.12-1
- 3.11.12

* Mon Nov 21 2011 Tim Waugh <twaugh@redhat.com> 3.11.10-11
- Added IEEE 1284 Device ID for Designjet T770 (bug #747957).

* Wed Nov 16 2011 Tim Waugh <twaugh@redhat.com> 3.11.10-10
- Corrected IEEE 1284 Device ID for LaserJet M1120 MFP (bug #754139).

* Wed Nov 16 2011 Jiri Popelka <jpopelka@redhat.com> 3.11.10-9
- revert prnt/hpcups/HPCupsFilter.cpp 3.11.5->3.11.7 change (bug #738089).

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.10-8
- Rebuilt for glibc bug#747377

* Tue Oct 25 2011 Tim Waugh <twaugh@redhat.com> 3.11.10-7
- Catch DBusException in hp-systray (bug #746024).

* Mon Oct 24 2011 Jiri Popelka <jpopelka@redhat.com> 3.11.10-6
- Move udev rules to /lib/udev/rules.d (bug #748208).

* Thu Oct 20 2011 Tim Waugh <twaugh@redhat.com> 3.11.10-5
- Pay attention to the SANE localOnly flag in hpaio (bug #743593).

* Mon Oct 17 2011 Tim Waugh <twaugh@redhat.com> 3.11.10-4
- Corrected IEEE 1284 Device ID for LaserJet M1319f MFP (bug #746614)

* Wed Oct 12 2011 Tim Waugh <twaugh@redhat.com> 3.11.10-3
- Corrected IEEE 1284 Device ID for LaserJet M1522nf MFP (bug #745498).

* Fri Oct  7 2011 Tim Waugh <twaugh@redhat.com> 3.11.10-2
- Corrected IEEE 1284 Device IDs:
  - LaserJet M1536dnf MFP (bug #743915)
  - PSC 1600 series (bug #743821)

* Tue Oct 04 2011 Jiri Popelka <jpopelka@redhat.com> 3.11.10-1
- 3.11.10
- Use _cups_serverbin macro from cups-devel for where to put driver executables.
- No need to define BuildRoot and clean it in clean and install section anymore.
- Corrected IEEE 1284 Device IDs:
  Officejet 6300 series (bug #689378)
  LaserJet Professional M1212nf MFP (bug #742490)

* Fri Sep 23 2011 Tim Waugh <twaugh@redhat.com> 3.11.7-5
- Fixed broken patch for pstotiff.

* Tue Sep 06 2011 Jiri Popelka <jpopelka@redhat.com> 3.11.7-4
- Fixed xsane crash when doing a multi-image scan (bug #725878)

* Fri Sep  2 2011 Tim Waugh <twaugh@redhat.com> 3.11.7-3
- Fixed hpcups crash when required plugin missing (bug #733461).

* Thu Aug 18 2011 Tim Waugh <twaugh@redhat.com> 3.11.7-2
- Create debugging files securely (CVE-2011-2722, bug #725830).

* Mon Jul 25 2011 Jiri Popelka <jpopelka@redhat.com> 3.11.7-1
- 3.11.7

* Mon Jul 11 2011 Jiri Popelka <jpopelka@redhat.com> 3.11.5-5
- rebuilt against new net-snmp-5.7

* Tue Jun 28 2011 Tim Waugh <twaugh@redhat.com> 3.11.5-4
- Added Device ID for HP LaserJet Professional P1606dn (bug #708472).
- Update IEEE 1284 Device IDs in hpijs.drv from hpcups.drv.

* Fri Jun 10 2011 Tim Waugh <twaugh@redhat.com> 3.11.5-3
- Fix building against CUPS 1.5.
- Re-create installed hpcups PPDs unconditionally (bug #712241).

* Thu May 19 2011 Jiri Popelka <jpopelka@redhat.com> 3.11.5-2
- Main package requires wget to avoid
  misleading errors about network connectivity (bug #705843).

* Thu May 12 2011 Jiri Popelka <jpopelka@redhat.com> 3.11.5-1
- 3.11.5

* Fri Apr  1 2011 Tim Waugh <twaugh@redhat.com> 3.11.3a-2
- Some rpmlint fixes for obsoletes/provides tags.

* Thu Mar 31 2011 Tim Waugh <twaugh@redhat.com> 3.11.3a-1
- 3.11.3a.

* Fri Mar 18 2011 Jiri Popelka <jpopelka@redhat.com> 3.11.3-1
- 3.11.3 (new hpps filter)

* Tue Mar  1 2011 Jiri Popelka <jpopelka@redhat.com> 3.11.1-5
- Avoid KeyError in ui4/wifisetupdialog.py (bug #680939).
- Corrected IEEE 1284 Device IDs:
  LaserJet 1300 (bug #670548)
  LaserJet 3390 (bug #678565)
  LaserJet P1505 (bug #680951)

* Tue Feb 22 2011 Tim Waugh <twaugh@redhat.com> - 3.11.1-4
- Ship hpijs.drv to give another driver option in case of problems
  with hpcups.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb  4 2011 Tim Waugh <twaugh@redhat.com> - 3.11.1-2
- Fixed typo causing ";marker-supply-low-warning" state reason to be
  reported by hpijs (bug #675151).

* Mon Jan 24 2011 Jiri Popelka <jpopelka@redhat.com> 3.11.1-1
- 3.11.1

* Mon Jan 17 2011 Tim Waugh <twaugh@redhat.com> - 3.10.9-14
- Applied patch to fix CVE-2010-4267, remote stack overflow
  vulnerability (bug #670252).

* Wed Jan 12 2011 Tim Waugh <twaugh@redhat.com> - 3.10.9-13
- Removed unused hpcac filter to avoid unnecessary perl dependency.

* Wed Jan 12 2011 Tim Waugh <twaugh@redhat.com> - 3.10.9-12
- Removed duplicate pstotiff files.

* Wed Jan 12 2011 Tim Waugh <twaugh@redhat.com> - 3.10.9-11
- Fixed "CUPS Web Interface" button (bug #633899).
- Set mimedir explicitly via configure.

* Wed Jan 05 2011 Jiri Popelka <jpopelka@redhat.com> 3.10.9-10
- Catch GError exception when notification showing failed (bug #665577).

* Wed Dec 15 2010 Tim Waugh <twaugh@redhat.com> - 3.10.9-9
- Enable D-Bus threading (and require pygobject2) (bug #600932).
- Fixed incorrect signal name in setup dialog (bug #653626).
- Another missing newline in filter output (Ubuntu #418053).
- Prevent hpaio segfaulting on invalid URIs (bug #649092).
- Catch D-Bus exceptions in fax dialog (bug #645316).

* Fri Dec 03 2010 Jiri Popelka <jpopelka@redhat.com> 3.10.9-8
- Corrected IEEE 1284 Device IDs:
  HP Color LaserJet CP2025dn (bug #651509).
  HP Color LaserJet CM3530 MFP (bug #659381).

* Fri Dec 03 2010 Jiri Popelka <jpopelka@redhat.com> 3.10.9-7
- The pycups requirement is now python-cups.
- Corrected IEEE 1284 Device IDs:
  HP LaserJet 4050/4100/2100 Series/2420/4200/4300/4350/5100/8000
              M3027 MFP/M3035 MFP/P3005/P3010/P4014/P4515 (bug #659039).
  HP Color LaserJet 2500/2550 series/3700/4550/4600/4650/4700/5550
                    CP1515n/CP3525/CP4520/CM2320nf MFP (bug #659040).
  HP Color LaserJet CM4730 MFP (bug #658831).

* Fri Nov 12 2010 Tim Waugh <twaugh@redhat.com> - 3.10.9-6
- Call cupsSetUser in cupsext's addPrinter method before connecting so
  that we can get an authentication callback (bug #538352).
- Prevent hp-fab traceback when run as root.

* Thu Nov 11 2010 Jiri Popelka <jpopelka@redhat.com> 3.10.9-5
- Don't emit SIGNALs in ui4.setupdialog.SetupDialog the PyQt3 way (bug #623834).

* Sun Oct 24 2010 Jiri Popelka <jpopelka@redhat.com> 3.10.9-4
- Avoid UnicodeDecodeError in printsettingstoolbox.py (bug #645739).

* Mon Oct 18 2010 Tim Waugh <twaugh@redhat.com> - 3.10.9-3
- Fixed traceback on error condition in device.py (bug #628125).
- Fixed bogus low ink warnings from hpijs driver (bug #643643).

* Thu Oct 14 2010 Jiri Popelka <jpopelka@redhat.com> - 3.10.9-2
- Fixed utils.addgroup() to return array instead of string (bug #642771).

* Mon Oct 04 2010 Jiri Popelka <jpopelka@redhat.com> - 3.10.9-1
- 3.10.9.

* Thu Sep 30 2010 Tim Waugh <twaugh@redhat.com> - 3.10.6-7
- More fixes from package review:
  - Avoided another macro in comment.
  - Use python_sitearch macro throughout.

* Wed Sep 29 2010 jkeating - 3.10.6-6
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Jiri Popelka <jpopelka@redhat.com> - 3.10.6-5
- Increased timeouts for curl, wget, ping for high latency networks (bug #635388).

* Sat Sep 18 2010 Dan Horák <dan[at]danny.cz> - 3.10.6-4
- drop the ExcludeArch for s390(x)

* Wed Sep 15 2010 Tim Waugh <twaugh@redhat.com>
- Fixes from package review:
  - Main package and hpijs sub-package require cups for directories.
  - The common sub-package requires udev for directories.
  - The libs sub-package requires python for directories.
  - Avoided macro in comment.
  - The lib sub-package now runs ldconfig for post/postun.
  - Use python_sitearch macro.

* Mon Sep 13 2010 Jiri Popelka <jpopelka@redhat.com>
- Added IEEE 1284 Device ID for HP LaserJet 4000 (bug #633227).

* Fri Aug 20 2010 Tim Waugh <twaugh@redhat.com> - 3.10.6-3
- Added another SNMP quirk for an OfficeJet Pro 8500 variant.

* Thu Aug 12 2010 Tim Waugh <twaugh@redhat.com> - 3.10.6-2
- Use correct fax PPD name for Qt3 UI.

* Tue Jul 27 2010 Jiri Popelka <jpopelka@redhat.com> - 3.10.6-1
- 3.10.6.
- Changed shebang /usr/bin/env python -> /usr/bin/python (bug #618351).
- Corrected IEEE 1284 Device IDs:
  - HP Color LaserJet CP1518ni (bug #613689).
  - HP Color LaserJet 2600n (bug #613712).

* Mon Jul 26 2010 Tim Waugh <twaugh@redhat.com>
- Removed selinux-policy version conflict as it is no longer
  necessary.

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.10.5-8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 24 2010 Jiri Popelka <jpopelka@redhat.com> - 3.10.5-7
- Added COPYING to common sub-package.

* Thu Jun 24 2010 Jiri Popelka <jpopelka@redhat.com> - 3.10.5-6
- Main package requires explicit version of hplip-libs.

* Thu Jun 17 2010 Tim Waugh <twaugh@redhat.com> - 3.10.5-5
- Fixed marker-supply attributes in hpijs (bug #605269).

* Wed Jun  9 2010 Tim Waugh <twaugh@redhat.com> - 3.10.5-4
- Mark SNMP quirks in PPD for HP OfficeJet Pro 8500 (bug #581825).

* Mon Jun 07 2010 Jiri Popelka <jpopelka@redhat.com> - 3.10.5-3
- hplip-gui requires libsane-hpaio

* Thu Jun 03 2010 Jiri Popelka <jpopelka@redhat.com> - 3.10.5-2
- Fix ImageableArea for Laserjet 8150/9000 (#596298)

* Mon May 17 2010 Jiri Popelka <jpopelka@redhat.com> - 3.10.5-1
- 3.10.5.   No longer need tray-icon-crash.patch
- Increase the timeout for system tray availability checking (bug #569969).

* Wed May 12 2010 Jiri Popelka <jpopelka@redhat.com> - 3.10.2-16
- Prevent segfault in cupsext when opening PPD file (bug #572775).

* Wed May 12 2010 Jiri Popelka <jpopelka@redhat.com> - 3.10.2-15
- Added/corrected more IEEE 1284 Device IDs:
  - HP LaserJet 4250 (bug #585499).
  - HP Color LaserJet 2605dn (bug #583953).
  - HP LaserJet P1007 (bug #585272).

* Wed May 12 2010 Jiri Popelka <jpopelka@redhat.com> - 3.10.2-14
- Wait for max 30s to see if a system tray becomes available (bug #569969).

* Wed Apr 28 2010 Tim Waugh <twaugh@redhat.com> - 3.10.2-13
- Clear old printer-state-reasons we used to manage (bug #510926).

* Tue Apr 27 2010 Jiri Popelka <jpopelka@redhat.com> - 3.10.2-12
- Added missing newline to string argument in dbglog() call (bug #585275).

* Fri Apr 16 2010 Tim Waugh <twaugh@redhat.com> - 3.10.2-11
- Added/corrected more IEEE 1284 Device IDs:
  - HP Color LaserJet CM1312nfi (bug #581005).
  - HP Color LaserJet 3800 (bug #581935).
  - HP Color LaserJet 2840 (bug #582215).
  - HP PSC 2400 (bug #583103).

* Fri Apr 16 2010 Jiri Popelka <jpopelka@redhat.com> - 3.10.2-10
- Fixed black/blank lines in ljcolor hpcups output (bug #579461).
  Work-around is to send entire blank raster lines instead of skipping them.

* Fri Apr  9 2010 Jiri Popelka <jpopelka@redhat.com> - 3.10.2-9.1
- Added/Corrected several IEEE 1284 Device IDs
  (bugs #577262, #577282, #577282, #577288, #577292, #577302,
  ,#577306, #577308, #577898, #579920, #580231)

* Wed Apr  7 2010 Tim Waugh <twaugh@redhat.com> - 3.10.2-8
- Regenerate hpcups PPDs on upgrade if necessary (bug #579355).

* Fri Mar 26 2010 Jiri Popelka <jpopelka@redhat.com> - 3.10.2-6
- Add Device ID for HP LaserJet 2300 (#576928)

* Tue Mar 23 2010 Tim Waugh <twaugh@redhat.com> - 3.10.2-5
- Explicitly destroy tray icon on exit (bug #543286).

* Thu Mar  4 2010 Tim Waugh <twaugh@redhat.com> - 3.10.2-4
- Main package doesn't require hal.
- Sub-package common requires udev.

* Wed Mar  3 2010 Tim Waugh <twaugh@redhat.com> - 3.10.2-3
- Set defattr in gui sub-package file manifest.
- Avoid mixed use of spaces and tabs.

* Mon Mar  1 2010 Tim Waugh <twaugh@redhat.com> - 3.10.2-2
- Removed SYSFS use in udev rules and actually made them work
  (bug #560754).
- Use a temporary file in pstotiff to allow gs random access.

* Fri Feb 26 2010 Tim Waugh <twaugh@redhat.com> - 3.10.2-1
- 3.10.2.  No longer need preferences-crash patch.
- The pstotiff filter is rubbish so replace it (launchpad #528394).
- Stopped hpcups pointlessly trying to read spool files
  directly (bug #552572).

* Sat Feb 20 2010 Tim Waugh <twaugh@redhat.com> - 3.9.12-8
- Corrected several IEEE 1284 Device IDs using foomatic data
  (launchpad bug #523259).

* Tue Feb 16 2010 Tim Waugh <twaugh@redhat.com> - 3.9.12-7
- Ship %%{_datadir}/hplip/prnt/plugins directory (bug #564551).

* Fri Feb  5 2010 Tim Waugh <twaugh@redhat.com> - 3.9.12-6
- Build requires cups for postscriptdriver tags for .drv file.

* Thu Feb  4 2010 Tim Waugh <twaugh@redhat.com> - 3.9.12-5
- Rebuild for postscriptdriver tags.

* Wed Jan 20 2010 Tim Waugh <twaugh@redhat.com> - 3.9.12-4
- Fixed crash when using Preferences dialog (bug #555979).

* Tue Jan 12 2010 Tim Waugh <twaugh@redhat.com> - 3.9.12-3
- Do ship pkit module even though the PolicyKit mechanism is not
  shipped (bug #554817).

* Tue Jan  5 2010 Tim Waugh <twaugh@redhat.com> - 3.9.12-2
- Retry when connecting to device fails (bug #532112).
- Don't ship PolicyKit mechanism (bug #551773).

* Tue Dec 22 2009 Tim Waugh <twaugh@redhat.com> - 3.9.12-1
- 3.9.12.  No longer need hpcups-plugin patch.

* Thu Dec 10 2009 Tim Waugh <twaugh@redhat.com> - 3.9.10-5
- Reverted fix for bug #533462 until bug #541604 is solved.

* Thu Nov 26 2009 Tim Waugh <twaugh@redhat.com> 3.9.10-4
- Fixed Device ID parsing code in hpijs's dj9xxvip.c (bug #510926).

* Thu Nov 26 2009 Tim Waugh <twaugh@redhat.com> 3.9.10-3
- Removed duplex constraints on page sizes with imageable areas larger
  than possible when duplexing (bug #541572).
- Fixed duplex reverse sides being horizontally flipped (bug #541604).

* Wed Nov 18 2009 Tim Waugh <twaugh@redhat.com> 3.9.10-2
- Fixed duplex handling in hpcups.drv (bug #533462).

* Wed Nov  4 2009 Tim Waugh <twaugh@redhat.com> 3.9.10-1
- 3.9.10.  No longer need clear-previous-state-reasons,
  hpcups-reorder, non-scripts, parenths, plugin-error,
  requirespageregion or state-reasons-newline patches.

* Mon Nov  2 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-21
- Added 'requires proprietary plugin' to appropriate model names
  (bug #513283).

* Fri Oct 30 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-20
- Reverted retry patch until it can be tested some more.

* Thu Oct 29 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-19
- Retry when connecting to device fails (bug #528483).
- Avoid busy loop in hpcups when backend has exited (bug #525944).

* Wed Oct 28 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-18
- Set a printer-state-reason when there's a missing required plugin
  (bug #531330).

* Tue Sep 29 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-17
- Give up trying to print a job to a reconnected device (bug #515481).

* Wed Sep 23 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-16
- Enable parallel port support when configuring (bug #524979).

* Wed Sep 16 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-15
- Fixed hp-setup traceback when discovery page is skipped (bug #523685).

* Fri Aug 28 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-14
- Include missing base files.

* Fri Aug 28 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-13
- Use dll.d file instead of post scriptlet for hpaio (bug #519988).
- Fixed RequiresPageRegion patch (bug #518756).

* Thu Aug 27 2009 Tomas Mraz <tmraz@redhat.com> - 3.9.8-12
- rebuilt with new openssl

* Wed Aug 26 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-11
- Set RequiresPageRegion in hpcups PPDs (bug #518756).

* Tue Aug 25 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-10
- Removed never-used definition of BREAKPOINT in scan/sane/common.h
  in hope of fixing the build.

* Tue Aug 25 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-9
- New common sub-package for udev rules and config file (bug #516459).
- Don't install base/*.py with executable bit set.

* Mon Aug 24 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-8
- Fixed typos in page sizes (bug #515469).
- Build no longer requires libudev-devel.
- Fixed state reasons handling problems (bug #501338).

* Wed Aug 19 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-6
- Make sure to avoid handwritten asm.
- Don't use obsolete configure options.

* Wed Aug 19 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-5
- Use upstream udev rules instead of hal policy (bug #518172).
- Removed unnecessary dependency on PyQt as we only use PyQt4 now.

* Wed Aug 12 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-4
- Upstream patch to fix paper size order and LJColor device class
  color space.

* Wed Aug 12 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-3
- The python-reportlab dependency was in the wrong sub-package.

* Thu Aug  6 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-2
- Removed access_control.grant_group line from HAL fdi file.

* Wed Aug  5 2009 Tim Waugh <twaugh@redhat.com> 3.9.8-1
- 3.9.8.

* Tue Aug  4 2009 Tim Waugh <twaugh@redhat.com> 3.9.6b-5
- Fix hpcups fax PPDs (bug #515356)

* Tue Jul 28 2009 Tim Waugh <twaugh@redhat.com> 3.9.6b-4
- Fixed ui-optional patch for qt4 code path (bug #500473).
- Fixed HWResolution for 'Normal' output from the hpcups driver
  (laundpad bug #405400).

* Mon Jul 27 2009 Tim Waugh <twaugh@redhat.com> 3.9.6b-2
- 3.9.6b.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Tim Waugh <twaugh@redhat.com> 3.9.2-8
- Use existing libusb-using routines to try fetching Device ID.

* Thu Jul 23 2009 Tim Waugh <twaugh@redhat.com> 3.9.2-7
- Error checking in the libudev device-id fallback code.

* Tue Jul 21 2009 Tim Waugh <twaugh@redhat.com> 3.9.2-6
- Fixed device-id reporting.

* Wed Jun 24 2009 Tim Waugh <twaugh@redhat.com> 3.9.2-5
- Set disc media for disc page sizes (bug #495672).

* Mon Mar  9 2009 Tim Waugh <twaugh@redhat.com> 3.9.2-4
- Ship libhpmud.so (bug #489059).
- Fixed no-root-config patch (bug #489055).

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Tim Waugh <twaugh@redhat.com> 3.9.2-2
- 3.9.2.  No longer need systray or quit patches.

* Tue Jan 27 2009 Tim Waugh <twaugh@redhat.com> 2.8.12-7
- Only ship compressed PPD files.

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> 2.8.12-6
- rebuild with new openssl

* Tue Jan 13 2009 Tim Waugh <twaugh@redhat.com> 2.8.12-5
- Fixed Quit menu item in device manager (bug #479751).

* Tue Jan 13 2009 Tim Waugh <twaugh@redhat.com> 2.8.12-4
- Prevent crash when DEVICE_URI/PRINTER environment variables are not
  set (bug #479808 comment 6).

* Tue Jan 13 2009 Tim Waugh <twaugh@redhat.com> 2.8.12-3
- Make --qt4 the default for the systray applet, so that it appears
  in the right place, again (bug #479751).
- Removed hal preprobe rules as they were causing breakage
  (bug #479648).

* Mon Jan 12 2009 Tim Waugh <twaugh@redhat.com> 2.8.12-2
- Don't write to system-wide configuration file (bug #479178).

* Tue Dec 23 2008 Tim Waugh <twaugh@redhat.com> 2.8.12-1
- 2.8.12.

* Thu Dec 11 2008 Tim Waugh <twaugh@redhat.com> 2.8.10-2
- Rediff libsane patch.

* Thu Dec 11 2008 Tim Waugh <twaugh@redhat.com> 2.8.10-1
- 2.8.10.  No longer need gzip-n or quiet patches.

* Thu Dec 11 2008 Tim Waugh <twaugh@redhat.com> 2.8.7-5
- Prevent backend crash when D-Bus not running (bug #474362).

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.8.7-4
- Rebuild for Python 2.6

* Tue Oct 21 2008 Tim Waugh <twaugh@redhat.com> 2.8.7-3
- Ship PPDs in the correct location (bug #343841).

* Fri Sep 26 2008 Tim Waugh <twaugh@redhat.com> 2.8.7-2
- Moved Python extension into libs sub-package (bug #461236).

* Mon Aug  4 2008 Tim Waugh <twaugh@redhat.com> 2.8.7-1
- 2.8.7.
- Avoid hard-coded rpaths.
- New libs sub-package (bug #444016).

* Thu Jul 31 2008 Tim Waugh <twaugh@redhat.com>
- Move libhpip.so* to the main package to avoid libsane-hpaio
  depending on hpijs (bug #457440).

* Thu Jul 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.8.6b-2
- fix license tag

* Mon Jul 28 2008 Tim Waugh <twaugh@redhat.com> 2.8.6b-1
- 2.8.6b.

* Mon Jun 23 2008 Tim Waugh <twaugh@redhat.com> 2.8.6-1
- 2.8.6.  No longer need libm patch.

* Fri Jun  6 2008 Tim Waugh <twaugh@redhat.com> 2.8.5-2
- Make --qt4 the default for the systray applet, so that it appears
  in the right place.  Requires PyQt4.

* Tue Jun  3 2008 Tim Waugh <twaugh@redhat.com> 2.8.5-1
- 2.8.5.
- Configure with --enable-dbus.  Build requires dbus-devel.
- Fix chmod 644 line.
- Ship hp-systray in the gui sub-package, but don't ship the desktop
  launcher yet as the systray applet is quite broken.
- Don't run autoconf.

* Tue May 13 2008 Tim Waugh <twaugh@redhat.com> 2.8.2-3
- Move installer directory to main package (bug #446171).

* Fri Apr  4 2008 Tim Waugh <twaugh@redhat.com> 2.8.2-2
- Update hplip.fdi for Fedora 9: info.bus -> info.subsystem.
- Images in docdir should not be executable (bug #440552).

* Tue Mar  4 2008 Tim Waugh <twaugh@redhat.com> 2.8.2-1
- 2.8.2.  No longer need alloc, unload-traceback or media-empty patches.
- Ship cupsddk driver.  The hpijs sub-package now requires cupsddk-drivers.

* Tue Mar  4 2008 Tim Waugh <twaugh@redhat.com> 2.7.12-6
- Fixed marker-supply-low strings.

* Wed Feb 13 2008 Tim Waugh <twaugh@redhat.com> 2.7.12-5
- Rebuild for GCC 4.3.

* Fri Jan 25 2008 Tim Waugh <twaugh@redhat.com> 2.7.12-4
- The hpijs compression module doesn't allocate enough memory (bug #428536).

* Wed Jan 23 2008 Tim Waugh <twaugh@redhat.com> 2.7.12-3
- Really grant the ACL for the lp group (bug #424331).

* Fri Jan 18 2008 Tim Waugh <twaugh@redhat.com> 2.7.12-2
- Ship installer directory (bug #428246).
- Avoid multilib conflict (bug #341531).
- The hpijs sub-package requires net-snmp (bug #376641).

* Fri Jan 18 2008 Tim Waugh <twaugh@redhat.com> 2.7.12-1
- 2.7.12.  No longer need ljdot4 patch.

* Fri Jan  4 2008 Tim Waugh <twaugh@redhat.com> 2.7.10-2
- Don't ship udev rules; instead, grant an ACL for group lp (bug #424331).

* Fri Dec 07 2007 Release Engineering <rel-eng at fedoraproject dot org> - 2.7.10-2
- Rebuild for deps

* Mon Oct 22 2007 Tim Waugh <twaugh@redhat.com> 2.7.10-1
- 2.7.10.

* Fri Oct 12 2007 Tim Waugh <twaugh@redhat.com> 2.7.9-3
- Applied patch to fix remnants of CVE-2007-5208 (bug #329111).

* Tue Oct  9 2007 Tim Waugh <twaugh@redhat.com> 2.7.9-2
- Use raw instead of 1284.4 communication for LJ4000 series (bug #249191).
- Build requires openssl-devel.

* Wed Oct  3 2007 Tim Waugh <twaugh@redhat.com> 2.7.9-1
- 2.7.9.
- Adjusted udev rules to be less permissive.  We use ConsoleKit to add
  ACLs to the device nodes, so world-writable device nodes can be avoided.

* Tue Sep 25 2007 Tim Waugh <twaugh@redhat.com> 2.7.7-5
- Prevent hpfax trying to load configuration files as user lp.

* Thu Sep  6 2007 Tim Waugh <twaugh@redhat.com> 2.7.7-4
- Reverted udev rules change.
- Ship a HAL FDI file to get correct access control on the USB device
  nodes (bug #251470).
- Make libsane-hpaio requires the main hplip package, needed for
  libhpip.so (bug #280281).

* Thu Aug 30 2007 Tim Waugh <twaugh@redhat.com> 2.7.7-3
- Updated udev rules to allow scanning by console user.

* Wed Aug 29 2007 Tim Waugh <twaugh@redhat.com> 2.7.7-2
- Better buildroot tag.
- More specific license tag.

* Fri Aug  3 2007 Tim Waugh <twaugh@redhat.com> 2.7.7-1
- 2.7.7.

* Mon Jul 23 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-10
- Move libhpmud to hpijs package (bug #248978).

* Fri Jul 20 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-9
- Remove hplip service on upgrade.
- Updated selinux-policy conflict for bug #249014.
- Fixed the udev rules file (bug #248740, bug #249025).

* Tue Jul 17 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-8
- Fixed hp-toolbox desktop file (bug #248560).

* Mon Jul 16 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-7
- Low ink is a warning condition, not an error.

* Wed Jul 11 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-6
- Add hp-check back, but in the gui sub-package.
- Show the HP Toolbox menu entry again.

* Mon Jul  9 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-5
- Read system config when run as root (bug #242974).

* Mon Jul  9 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-4
- Moved reportlab requirement to gui sub-package (bug #189030).
- Patchlevel 1.

* Sat Jul  7 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-3
- Fixed pre scriptlet (bug #247349, bug #247322).

* Fri Jul  6 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-2
- Main package requires python-reportlab for hp-sendfax (bug #189030).
- Explicitly enable scanning.
- Main package requires python-imaging for hp-scan (bug #247210).

* Mon Jul  2 2007 Tim Waugh <twaugh@redhat.com>
- Updated selinux-policy conflict for bug #246257.

* Fri Jun 29 2007 Tim Waugh <twaugh@redhat.com> 2.7.6-1
- 2.7.6.

* Thu Jun 28 2007 Tim Waugh <twaugh@redhat.com> 1.7.4a-3
- Another go at avoiding AVC messages on boot (bug #244205).

* Thu Jun 14 2007 Tim Waugh <twaugh@redhat.com> 1.7.4a-2
- Don't try to write a /root/.hplip.conf file when running as a CUPS
  backend (bug #244205).

* Wed Jun 13 2007 Tim Waugh <twaugh@redhat.com> 1.7.4a-1
- Don't put the version in the desktop file; let desktop-file-install do it.
- 1.7.4a.  No longer need marker-supply or faxing-with-low-supplies
  patches.  Cheetah and cherrypy directories no longer shipped in source
  tarball.

* Mon Jun 11 2007 Tim Waugh <twaugh@redhat.com>
- Don't ship hp-check (bug #243273).
- Moved hp-setup back to the base package, and put code in
  utils.checkPyQtImport() to check for the gui sub-package as well as
  PyQt (bug #243273).

* Fri Jun  8 2007 Tim Waugh <twaugh@redhat.com>
- Moved hp-setup to the ui package (bug #243273).
- Prevent SELinux audit message from the CUPS backends (bug #241776)

* Thu May 10 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-10
- Prevent a traceback when unloading a photo card (bug #238617).

* Fri May  4 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-9
- When faxing, low ink/paper is not a problem (bug #238664).

* Tue Apr 17 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-8
- Update desktop database on %%postun as well (bug #236163).

* Mon Apr 16 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-7
- Some parts can run without GUI support after all (bug #236161).
- Added /sbin/service and /sbin/chkconfig requirements for the scriptlets
  (bug #236445).
- Fixed %%post scriptlet's condrestart logic (bug #236445).

* Fri Apr 13 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-6
- Fixed dangling symlinks (bug #236156).
- Move all fax bits to the gui package (bug #236161).
- Don't ship fax PPD and backend twice (bug #236092).
- Run update-desktop-database in the gui package's %%post scriptlet
  (bug #236163).
- Moved desktop-file-utils requirement to gui package (bug #236163).
- Bumped selinux-policy conflict version (bug #236092).

* Thu Apr  5 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-5
- Better media-empty-error state handling: always set the state.

* Wed Apr  4 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-4
- Clear the media-empty-error printer state.

* Wed Apr  4 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-3
- Fixed typo in marker-supply-low patch.

* Wed Apr  4 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-2
- Split out a gui sub-package (bug #193661).
- Build requires sane-backends-devel (bug #234813).

* Tue Apr  3 2007 Tim Waugh <twaugh@redhat.com>
- Change 'Hidden' to 'NoDisplay' in the desktop file, and use the System
  category instead of Utility (bug #170762).
- Link libsane-hpaio against libsane (bug #234813).

* Fri Mar 30 2007 Tim Waugh <twaugh@redhat.com>
- Use marker-supply-low IPP message.

* Thu Mar  1 2007 Tim Waugh <twaugh@redhat.com> 1.7.2-1
- 1.7.2.

* Wed Feb 14 2007 Tim Waugh <twaugh@redhat.com> 1.7.1-1
- 1.7.1.

* Wed Jan 10 2007 Tim Waugh <twaugh@redhat.com> 1.6.12-1
- 1.6.12.  No longer need broken-conf, loop, out-of-paper or
  sane-debug patches.

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1.6.10-7
- rebuild against python 2.5

* Wed Dec  6 2006 Tim Waugh <twaugh@redhat.com>
- Minor state fixes for out-of-paper patch.

* Thu Nov 23 2006 Tim Waugh <twaugh@redhat.com> 1.6.10-6
- Report out-of-paper and offline conditions in CUPS backend (bug #216477).

* Wed Nov  1 2006 Tim Waugh <twaugh@redhat.com> 1.6.10-5
- Fixed debugging patch.

* Wed Nov  1 2006 Tim Waugh <twaugh@redhat.com> 1.6.10-4
- Allow debugging of the SANE backend.

* Mon Oct 30 2006 Tim Waugh <twaugh@redhat.com> 1.6.10-3
- IPv6 support (bug #198377).  Local-only sockets are IPv4, and ought
  to be changed to unix domain sockets in future.

* Fri Oct 27 2006 Tim Waugh <twaugh@redhat.com> 1.6.10-2
- 1.6.10.  No longer need compile patch.
- Fixed default config file (bug #211072).
- Moved libhpip to hpijs sub-package (bug #212531).

* Fri Sep 29 2006 Tim Waugh <twaugh@redhat.com> 1.6.7-4
- Don't wake up every half a second (bug #204725).

* Mon Sep 25 2006 Tim Waugh <twaugh@redhat.com>
- Fixed package URL.

* Mon Aug 21 2006 Tim Waugh <twaugh@redhat.com> 1.6.7-3
- Don't look up username in PWDB in the fax backend (removed redundant code).

* Mon Aug  7 2006 Tim Waugh <twaugh@redhat.com> 1.6.7-2
- 1.6.7.
- Conflict with selinux-policy < 2.3.4 to make sure new port numbers are
  known about (bug #201357).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - (none):1.6.6a-3.1
- rebuild

* Tue Jul  4 2006 Tim Waugh <twaugh@redhat.com> 1.6.6a-3
- libhpip should link against libm (bug #197599).

* Wed Jun 28 2006 Tim Waugh <twaugh@redhat.com> 1.6.6a-2
- 1.6.6a.

* Mon Jun 26 2006 Tim Waugh <twaugh@redhat.com>
- Patchlevel 1.
- Fixed libsane-hpaio %%post scriptlet (bug #196663).

* Fri Jun 16 2006 Tim Waugh <twaugh@redhat.com> 1.6.6-2
- 1.6.6.

* Mon Jun 12 2006 Tim Waugh <twaugh@redhat.com> 0.9.11-6
- Build requires autoconf (bug #194682).

* Fri May 26 2006 Tim Waugh <twaugh@redhat.com> 0.9.11-5
- Include doc files (bug #192790).

* Mon May 15 2006 Tim Waugh <twaugh@redhat.com> 0.9.11-4
- Patchlevel 2.

* Wed May 10 2006 Tim Waugh <twaugh@redhat.com> 0.9.11-3
- Move hpijs to 0.9.11 too.

* Wed May 10 2006 Tim Waugh <twaugh@redhat.com> 0.9.11-2
- 0.9.11.
- Keep hpijs at 0.9.8 for now.

* Fri Apr 21 2006 Tim Waugh <twaugh@redhat.com> 0.9.10-6
- Patchlevel 2.

* Wed Apr 19 2006 Tim Waugh <twaugh@redhat.com>
- Don't package COPYING twice (bug #189162).

* Tue Apr 18 2006 Tim Waugh <twaugh@redhat.com> 0.9.10-5
- Patchlevel 1.
- Fixed another case-sensitive match.
- Require hpijs sub-package (bug #189140).
- Don't package unneeded files (bug #189162).
- Put fax PPD in the right place (bug #186213).

* Tue Apr  4 2006 Tim Waugh <twaugh@redhat.com> 0.9.10-4
- Use case-insensitive matching.  0.9.8 gave all-uppercase in some
  situations.
- Last known working hpijs comes from 0.9.8, so use that.

* Tue Mar 28 2006 Tim Waugh <twaugh@redhat.com> 0.9.10-3
- Always use /usr/lib/cups/backend.

* Tue Mar 28 2006 Tim Waugh <twaugh@redhat.com> 0.9.10-2
- 0.9.10.
- Ship PPDs.

* Fri Mar 24 2006 Tim Waugh <twaugh@redhat.com> 0.9.9-7
- Include hpfax.
- Build requires libusb-devel.

* Thu Mar 23 2006 Tim Waugh <twaugh@redhat.com> 0.9.9-6
- CUPS backend directory is always in /usr/lib.

* Mon Mar 13 2006 Tim Waugh <twaugh@redhat.com> 0.9.9-4
- Quieten hpssd on startup.

* Sat Mar 11 2006 Tim Waugh <twaugh@redhat.com> 0.9.9-3
- Patchlevel 1.

* Thu Mar  9 2006 Tim Waugh <twaugh@redhat.com> 0.9.9-2
- 0.9.9.  No longer need quiet or 0.9.8-4 patches.

* Wed Mar 01 2006 Karsten Hopp <karsten@redhat.de> 0.9.8-6
- Buildrequires: desktop-file-utils

* Mon Feb 27 2006 Tim Waugh <twaugh@redhat.com> 0.9.8-5
- Patchlevel 4.

* Tue Feb 14 2006 Tim Waugh <twaugh@redhat.com> 0.9.8-4
- Added Obsoletes: hpoj tags back in (bug #181476).

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - (none):0.9.8-3.1
- bump again for double-long bug on ppc(64)

* Tue Feb  7 2006 Tim Waugh <twaugh@redhat.com> 0.9.8-3
- Patchlevel 3.

* Fri Feb  3 2006 Tim Waugh <twaugh@redhat.com> 0.9.8-2
- Patchlevel 2.

* Thu Feb  2 2006 Tim Waugh <twaugh@redhat.com> 0.9.8-1
- 0.9.8.
- No longer need initscript patch.
- Don't package hpfax yet.

* Wed Jan 18 2006 Tim Waugh <twaugh@redhat.com> 0.9.7-8
- Don't package PPD files.

* Thu Jan  5 2006 Tim Waugh <twaugh@redhat.com> 0.9.7-7
- Fix initscript (bug #176966).

* Mon Jan  2 2006 Tim Waugh <twaugh@redhat.com> 0.9.7-6
- Rebuild.

* Fri Dec 23 2005 Tim Waugh <twaugh@redhat.com> 0.9.7-5
- Rebuild.

* Wed Dec 21 2005 Tim Waugh <twaugh@redhat.com> 0.9.7-4
- Build requires python-devel, libjpeg-devel (bug #176317).

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Dec  7 2005 Tim Waugh <twaugh@redhat.com> 0.9.7-3
- Use upstream patch 0.9.7-2.
- No longer need lpgetstatus or compile patches.

* Fri Nov 25 2005 Tim Waugh <twaugh@redhat.com> 0.9.7-2
- Prevent LPGETSTATUS overrunning format buffer.

* Thu Nov 24 2005 Tim Waugh <twaugh@redhat.com> 0.9.7-1
- 0.9.7.

* Fri Nov 18 2005 Tim Waugh <twaugh@redhat.com> 0.9.6-7
- Fix compilation.

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> 0.9.6-6
- rebuilt against new openssl

* Mon Nov  7 2005 Tim Waugh <twaugh@redhat.com> 0.9.6-5
- Rebuilt.

* Wed Oct 26 2005 Tim Waugh <twaugh@redhat.com> 0.9.6-4
- Ship initscript in %%{_sysconfdir}/rc.d/init.d.

* Fri Oct 14 2005 Tim Waugh <twaugh@redhat.com>
- Install the desktop file with Hidden=True (bug #170762).

* Fri Oct 14 2005 Tim Waugh <twaugh@redhat.com> 0.9.6-3
- Don't install desktop file (bug #170762).
- Quieten the hpssd daemon at startup (bug #170762).

* Wed Oct 12 2005 Tim Waugh <twaugh@redhat.com> 0.9.6-2
- 0.9.6.

* Tue Sep 20 2005 Tim Waugh <twaugh@redhat.com> 0.9.5-3
- Apply upstream patch to fix scanning in LaserJets and parallel InkJets.

* Mon Sep 19 2005 Tim Waugh <twaugh@redhat.com> 0.9.5-2
- 0.9.5.
- No longer need condrestart patch.
- Fix compile errors.

* Tue Jul 26 2005 Tim Waugh <twaugh@redhat.com> 0.9.4-3
- Fix condrestart in the initscript.

* Mon Jul 25 2005 Tim Waugh <twaugh@redhat.com> 0.9.4-2
- Use 'condrestart' not 'restart' in %%post scriptlet.

* Fri Jul 22 2005 Tim Waugh <twaugh@redhat.com> 0.9.4-1
- forward-decl patch not needed.
- 0.9.4.

* Fri Jul  1 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-8
- Removed Obsoletes: hpoj tags (bug #162222).

* Thu Jun 30 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-7
- Rebuild to get Python modules precompiled.

* Wed Jun 22 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-6
- For libsane-hpaio ExcludeArch: s390 s390x, because it requires
  sane-backends.

* Wed Jun 15 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-5
- Use static IP ports (for SELinux policy).

* Tue Jun 14 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-4
- Conflicts: hpijs from before this package provided it.
- Conflicts: system-config-printer < 0.6.132 (i.e. before HPLIP support
  was added)

* Thu Jun  9 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-3
- Added Obsoletes: for xojpanel and hpoj-devel (but we don't actually package
  devel files yet).

* Thu Jun  9 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-2
- Add 'hpaio' to SANE config file, not 'hpoj' (bug #159954).

* Thu Jun  9 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-1
- Use /usr/share/applications for putting desktop files in (bug #159932).
- Requires PyQt (bug #159932).

* Tue Jun  7 2005 Tim Waugh <twaugh@redhat.com> 0.9.3-0.1
- Initial package, based on Mandriva spec file.
