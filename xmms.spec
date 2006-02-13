Summary: The X MultiMedia System, a media player
Name: xmms
Version: 1.2.10
Release: 20%{?dist}
Epoch: 1
License: GPL
Group: Applications/Multimedia
URL: http://www.xmms.org/
Source0: http://www.xmms.org/files/1.2.x/%{name}-%{version}.patched.tar.bz2
Source2: xmms.req
Source3: xmms.xpm
Source5: rh_mp3.c
Patch1: xmms-1.2.6-audio.patch
Patch2: xmms-1.2.6-lazy.patch
Patch3: xmms-1.2.8-default-skin.patch
Patch4: xmms-1.2.9-nomp3.patch
Patch5: xmms-1.2.8-arts.patch
Patch6: xmms-1.2.8-alsalib.patch
Patch7: xmms-cd-mountpoint.patch
Patch9: xmms-underquoted.patch
Patch10: xmms-alsa-backport.patch
Patch11: xmms-1.2.10-gcc4.patch
Patch12: xmms-1.2.10-crossfade-0.3.9.patch

Requires: unzip
# the desktop file and redhat-menus are redundant requires really
Requires: /usr/share/desktop-menu-patches/redhat-audio-player.desktop
Requires: redhat-menus >= 0.11

BuildRequires: gtk+-devel, esound-devel, arts-devel, alsa-lib-devel
BuildRequires: libogg-devel, libvorbis-devel, mikmod-devel
BuildRequires: libXt-devel, libSM-devel, libXxf86vm-devel, mesa-libGL-devel
BuildRequires: gettext-devel, zlib-devel
Requires(post): desktop-file-utils >= 0.9
Requires(postun): desktop-file-utils >= 0.9
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Obsoletes: xmms-esd xmms-gl xmms-mikmod xmms-gnome

# This is to avoid requiring all of arts, esound, alsa...
%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE2}

%description
Xmms is a multimedia (Ogg Vorbis, CDs) player for the X Window System with
an interface similar to Winamp's. Xmms supports playlists and
streaming content and has a configurable interface.


%package devel
Summary: Files required for XMMS plug-in development
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}, gtk+-devel

%description devel
Files needed for building plug-ins for the X MultiMedia System.


%prep
%setup -q
# Set default output plugin to ALSA
%patch1 -p1 -b .audio
# Use RTLD_LAZY, not RTLD_NOW
%patch2 -p1 -b .lazy
# Change the default skin
%patch3 -p1 -b .default-skin
# Don't build MP3 support, support bits for MP3 placeholder
%patch4 -p1 -b .nomp3
# Link arts dynamically and detect its presence for choosing output plugin
%patch5 -p1 -b .arts
# Don't link *everything* against alsa-lib
%patch6 -p1 -b .alsalib
# Use something that's more likely to work as the default cdrom mountpoint
%patch7 -p0 -b .cd-mountpoint
# Fix m4 underquoted warning
%patch9 -p1 -b .underquoted
# Backport for recent ALSA
%patch10 -p0 -b .alsa-backport
# Fix compilation with gcc4
%patch11 -p1 -b .gcc4
# Fix for crossfade >= 0.3.9 to work properly
%patch12 -p1 -b .crossfade


%build
%configure \
    --disable-dependency-tracking \
    --enable-kanji \
    --enable-texthack \
    --enable-ipv6 \
    --with-pic
# Hack around old libtool and x86_64 issue
#for i in `find . -name Makefile`; do
#    cat $i | sed s/-lpthread//g > $i.tmp
#    mv $i.tmp $i
#done
%{__make} %{?_smp_mflags}

# Compile the default mp3 "warning dialog" plugin
%{__cc} %{optflags} -fPIC -shared -Wl,-soname -Wl,librh_mp3.so -o librh_mp3.so \
    -I. `gtk-config --cflags gtk` %{SOURCE5}


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
%find_lang %{name}

# Install default mp3 "warning dialog" plugin
%{__install} -m 0755 librh_mp3.so %{buildroot}%{_libdir}/xmms/Input/

# Link to the desktop menu entry included in redhat-menus
%{__mkdir_p} %{buildroot}%{_datadir}/applications
%{__ln_s} %{_datadir}/desktop-menu-patches/redhat-audio-player.desktop \
    %{buildroot}%{_datadir}/applications/

# Install xmms.xpm, the Icon= from the menu entry
%{__install} -D -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/pixmaps/xmms.xpm

# Create empty Skins directory to be included
%{__mkdir_p} %{buildroot}%{_datadir}/xmms/Skins/


%clean
%{__rm} -rf %{buildroot}


%post
/sbin/ldconfig
update-desktop-database -q || :

%postun
/sbin/ldconfig
update-desktop-database -q || :


%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc AUTHORS ChangeLog COPYING FAQ NEWS TODO README
%{_bindir}/xmms
%{_bindir}/wmxmms
%{_libdir}/libxmms.so.*
%dir %{_libdir}/xmms/
%dir %{_libdir}/xmms/Effect/
%dir %{_libdir}/xmms/General/
%dir %{_libdir}/xmms/Input/
%dir %{_libdir}/xmms/Output/
%dir %{_libdir}/xmms/Visualization/
%{_libdir}/xmms/Effect/*.so
%{_libdir}/xmms/General/*.so
%{_libdir}/xmms/Input/*.so
%{_libdir}/xmms/Output/*.so
%{_libdir}/xmms/Visualization/*.so
%exclude %{_libdir}/xmms/*/*.la
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/xmms.xpm
%{_datadir}/xmms/
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,0755)
%{_bindir}/xmms-config
%{_includedir}/xmms/
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la
%{_libdir}/*.so
%{_datadir}/aclocal/xmms.m4


%changelog
* Mon Feb 13 2006 Matthias Saou <http://freshrpms.net/> 1:1.2.10-20
- Spec file cleanup.
- Disable previous -lpthread hack, since it seems to work again now...
- Include crossfade 0.3.9 patch.
- Remove very old x11amp obsoletes.
- Exclude static libraries, update devel summary and description for it.
- List all plugins directories in order to be aware of breakage if the
  libtool problem ever happens again.
- Fix post/postun scriplets.
- Remove xmms_logo.xpm and xmms_mini.xpm, they should be unused.
- Add libXt-devel to fullfill the "checking for X..." configure check.
- Add gettext-devel to make more configure checks happy.

* Wed Dec 28 2005 Hans de Goede <j.w.r.degoede@hhs.nl>  1:1.2.10-19
- Remove -lpthread from all LDFLAGS as this confuses the old libtool
  used by xmms on x86_64 (FE-bug #175493)
- Add missing modular Xorg BuildReqs, this (re)enables session managment
  support and the openGL plugins.

* Tue Dec 20 2005 Matthias Saou <http://freshrpms.net/> 1:1.2.10-18.1
- Update gcc4 patch to include fix for xmms.org bug #1730, fixes FC5 build.

* Sat May 28 2005 Matthias Saou <http://freshrpms.net/> 1:1.2.10-18
- Build with explicit --with-pic to fix compilation of flac plugin on
  x86_64.

* Thu May  5 2005 Matthias Saou <http://freshrpms.net/> 1:1.2.10-17
- Don't have scriplets fail if update-desktop-database returns an error.

* Sat Apr 30 2005 Ville Skyttä <ville.skytta at iki.fi> - 1:1.2.10-16
- Use /media/cdrecorder as the default CDROM mountpoint for the CD audio
  plugin, it's more likely to work nowadays than /mnt/cdrom.
- Drop no longer needed skins tarball.
- Build with dependency tracking disabled.

* Fri Apr 15 2005 Matthias Saou <http://freshrpms.net/> 1:1.2.10-15
- Change main icon from xpm to png (smaller, more consistent).
- Split off the aRts plugin.
- Split off the skins at last, as noarch (#65614).
- Remove generic INSTALL instructions.
- Remove autoconf and automake build reqs, as they're no longer called.
- Remove unneeded glib2-devel build req.

* Wed Apr  6 2005 Seth Vidal <skvidal at phy.duke.edu> 1:1.2.10-14
- put back conflict

* Wed Apr  6 2005 Seth Vidal <skvidal at phy.duke.edu> 1:1.2.10-13
- clean up spec file a bit.
- remove everything except for the last 2 yrs of changelog entries.
- make things match Fedora Extras Packaging Guidelines more

* Wed Apr  6 2005 Seth Vidal <skvidal at phy.duke.edu> 1:1.2.10-12
- Apply patch from David Hill RH bz: 152138

* Thu Mar 24 2005 David Hill <djh[at]ii.net> 1:1.2.10-12
- Add gcc4 patch

* Wed Jan 05 2005 Colin Walters <walters@redhat.com> 1:1.2.10-11
- Change BR on mikmod to mikmod-devel (138057)

* Tue Nov 23 2004 Colin Walters <walters@redhat.com> 1:1.2.10-10
- Add xmms-alsa-backport.patch (bug 140565, John Haxby)

* Wed Oct 13 2004 Colin Walters <walters@redhat.com> 1:1.2.10-9
- Correct update-desktop-database correction for postun

* Wed Oct 13 2004 Colin Walters <walters@redhat.com> 1:1.2.10-8
- Call update-desktop-database on correct directory

* Mon Oct 04 2004 Colin Walters <walters@redhat.com> 1:1.2.10-7
- PreReq desktop-file-utils 0.9
- Run update-desktop-database

* Sun Aug 15 2004 Tim Waugh <twaugh@redhat.com> 1:1.2.10-6
- Fixed another underquoted m4 definition.

* Thu Jul 15 2004 Tim Waugh <twaugh@redhat.com> 1:1.2.10-5
- Fixed warnings in shipped m4 file.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 31 2004 Warren Togami <wtogami@redhat.com> 1:1.2.10-3.p
- #124701 -devel req gtk+-devel

* Thu Mar 11 2004 Bill Nottingham <notting@redhat.com> 1:1.2.10-2.p
- update to 1.2.10
- fix buildreqs (#114857)
- switch default output plugin to ALSA

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 23 2004 Than Ngo <than@redhat.com> 1:1.2.9-5.p
- enable arts plugin, it should work with arts-1.2.0-1.5 or newer.

* Sat Feb 14 2004 Than Ngo <than@redhat.com> 1:1.2.9-4.p
- disable xmms-1.2.8-arts.patch

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 28 2004 Bill Nottingham <notting@redhat.com> 1:1.2.9-2.p
- enable ipv6 (#105774)

* Wed Jan 28 2004 Bill Nottingham <notting@redhat.com> 1:1.2.9-1.p
- update to 1.2.9

* Fri Dec 12 2003 Bill Nottingham <notting@redhat.com> 1:1.2.8-4.p
- rebuild, pick up alsa plugin

* Wed Oct 22 2003 Bill Nottingham <notting@redhat.com> 1:1.2.8-3.p
- fix dependency blacklisting (corollary of #100917)

* Mon Oct 13 2003 Than Ngo <than@redhat.com> 1:1.2.8-2.p
- workaround to fix arts crash

* Mon Sep  8 2003 Bill Nottingham <notting@redhat.com> 1:1.2.8-1.p
- update to 1.2.8
- clean out now-upstream stuff (Welsh po file, other patches)
- switch to Håvard's arts plugin, tweak it's default buffer size
- don't explicitly require trademarked skin name (#84554)

* Mon Jun 30 2003 Bill Nottingham <notting@redhat.com> 1:1.2.7-23.p
- add welsh po file (#98244)

* Sun Jun  8 2003 Tim Powers <timp@redhat.com> 1:1.2.7-22.1.p
- built for RHEL

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.
