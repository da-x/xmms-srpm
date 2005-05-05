Summary: The X MultiMedia System, a media player which resembles Winamp
Name: xmms
Version: 1.2.10
Release: 17
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

Requires: unzip
# the desktop file and redhat-menus are redundant requires really
Requires: /usr/share/desktop-menu-patches/redhat-audio-player.desktop
Requires: redhat-menus >= 0.11

BuildRequires: gtk+-devel esound-devel arts-devel alsa-lib-devel
BuildRequires: libvorbis-devel mikmod-devel
Requires(pre): desktop-file-utils >= 0.9
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Obsoletes: x11amp0.7-1-1 x11amp xmms-esd xmms-gl xmms-mikmod xmms-gnome

%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE2}

%description
Xmms is a multimedia (Ogg Vorbis, CDs) player for the X Window System with
an interface similar to Winamp's. Xmms supports playlists and
streaming content and has a configurable interface.

%package devel
Summary: Static libraries and header files for Xmms plug-in development.
Group: Development/Libraries
Obsoletes: x11amp-devel
Requires: %{name} = %{epoch}:%{version} gtk+-devel

%description devel
The static libraries and header files needed for building plug-ins for
the Xmms multimedia player.

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

%build
%configure --disable-dependency-tracking \
  --enable-kanji \
  --enable-texthack \
  --enable-ipv6

make

gcc -fPIC $RPM_OPT_FLAGS -shared -Wl,-soname -Wl,librh_mp3.so -o librh_mp3.so \
     %{SOURCE5} -I. `gtk-config --cflags gtk`

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

install -m 755 librh_mp3.so %{buildroot}%{_libdir}/xmms/Input

mkdir -pv %{buildroot}%{_datadir}/applications
(cd $RPM_BUILD_ROOT%{_datadir}/applications && ln -sf \
  %{_datadir}/desktop-menu-patches/redhat-audio-player.desktop)

mkdir -p %{buildroot}%{_datadir}/pixmaps/mini
install -m 644 xmms/xmms_logo.xpm %{buildroot}%{_datadir}/pixmaps/
install -m 644 xmms/xmms_mini.xpm %{buildroot}%{_datadir}/pixmaps/mini/
install -m 644 %{SOURCE3} %{buildroot}%{_datadir}/pixmaps/

# create empty skins directory to be included
mkdir -p %{buildroot}%{_datadir}/xmms/Skins

# unpackaged files
rm -f %{buildroot}/%{_datadir}/xmms/*/lib*.{a,la} \
      %{buildroot}/%{_libdir}/libxmms.la \
      %{buildroot}/%{_libdir}/xmms/*/*.la \
      %{buildroot}/%{_mandir}/man1/gnomexmms*

%find_lang %{name}

%post
/sbin/ldconfig  
update-desktop-database %{_datadir}/desktop-menu-patches || :

%postun
/sbin/ldconfig 
update-desktop-database %{_datadir}/desktop-menu-patches || :

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc AUTHORS COPYING ChangeLog FAQ NEWS TODO README 
%{_bindir}/xmms
%{_bindir}/wmxmms
%{_libdir}/libxmms.so.1*
%{_libdir}/xmms/
%{_datadir}/applications/*
%{_datadir}/pixmaps/xmms.xpm
%{_datadir}/pixmaps/xmms_logo.xpm
%{_datadir}/pixmaps/mini/xmms_mini.xpm
%{_datadir}/xmms/
%{_mandir}/man1/[wx]*

%files devel
%defattr(-,root,root,0755)
%{_includedir}/xmms/
%{_bindir}/xmms-config
%{_datadir}/aclocal/xmms.m4
%{_libdir}/lib*.a
%{_libdir}/lib*.so

%changelog
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
