# NOTE: xorg/driver/glamor.git and xorg/releases/individual/driver/glamor-egl are the same package
# (although some glamor-egl release tarballs, e.g. 0.5.0, are broken)
Summary:	Open-source X.org graphics common driver based on GL library
Summary(pl.UTF-8):	Ogólny sterownik graficzny X.org o otwartych źródłach, oparty na bibliotece GL
Name:		glamor
Version:	0.6.0
Release:	1
License:	MIT
Group:		Libraries
#Source0:	http://cgit.freedesktop.org/xorg/driver/glamor/snapshot/%{name}-%{version}.tar.gz
Source0:	http://xorg.freedesktop.org/releases/individual/driver/%{name}-egl-%{version}.tar.bz2
# Source0-md5:	b3668594675f71a75153ee52dbd35535
Patch0:		%{name}-pc.patch
Patch1:		%{name}-link.patch
URL:		http://www.freedesktop.org/wiki/Software/Glamor
BuildRequires:	EGL-devel
BuildRequires:	OpenGL-devel
BuildRequires:	Mesa-libgbm-devel >= 9
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake
BuildRequires:	libdrm-devel >= 2.4.23
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pixman-devel >= 0.21.8
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(gl) >= 7.1.0
BuildRequires:	xorg-proto-dri2proto-devel >= 2.6
BuildRequires:	xorg-util-util-macros >= 1.8
BuildRequires:	xorg-xserver-server-devel >= 1.10
Requires:	%{name}-libs = %{version}-%{release}
Requires:	Mesa-libgbm >= 9
Requires:	libdrm >= 2.4.23
Requires:	pixman >= 0.21.8
Requires:	xorg-xserver-server >= 1.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# relies on symbols from X server
%define		skip_post_check_so	libglamor.so.*

%description
The glamor module is an open-source 2D graphics common driver for the
X Window System as implemented by X.org. It supports a variety of
graphics chipsets which have OpenGL/EGL/GBM supports.

It's a GL-based rendering acceleration library for X server:
 - It uses GL functions and shader to complete the 2D graphics
   operations.
 - It uses normal texture to represent a drawable pixmap if possible.
 - It calls GL functions to render to the texture directly.

It's somehow hardware independently. And could be a building block of
any X server's DDX driver. This package can support every platform
which has OpenGL and gbm and drm libraries.

%description -l pl.UTF-8
Moduł glamor to mający otwarte źródła ogólny sterownik grafiki 2D dla
systemu X Window w implementacji X.org. Obsługuje różne układy
graficzne, obsługiwane przez kod biblioteki OpenGL/EGL/GBM.

Jest to oparta na GL biblioteka akceleracji renderowania dla serwera
X:
 - wykorzystuje funkcje GL i shader do wykonywania operacji
   graficznych 2D,
 - używa zwykłych tekstur do reprezentacji map bitowych do rysowania,
 - wywołuje funkcje GL do bezpośredniego renderowania tekstur.

Jest w pewien sposób niezależna od sprzętu. Może być blokiem tworzącym
dowolny sterownik DDX serwera X. Ten pakiet może obsłużyć dowolną
platformę, mającą biblioteki OpenGL, gbm i drm.

%package libs
Summary:	Glamor shared library
Summary(pl.UTF-8):	Biblioteka współdzielona Glamor
Group:		Libraries
Requires:	OpenGL
Requires:	pixman >= 0.21.8

%description libs
Glamor shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona Glamor.

%package devel
Summary:	Header file for Glamor modules API
Summary(pl.UTF-8):	Plik nagłówkowy API modułów Glamor
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	EGL-devel
Requires:	OpenGL-devel
Requires:	libdrm-devel >= 2.4.23
Requires:	pixman-devel >= 0.21.8
Requires:	pkgconfig(gl) >= 7.1.0
Requires:	xorg-xserver-server-devel >= 1.10

%description devel
Header file for Glamor modules API.

%description devel -l pl.UTF-8
Plik nagłówkowy API modułów Glamor.

%prep
%setup -q -n %{name}-egl-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-glx-tls
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libglamor.la \
	$RPM_BUILD_ROOT%{_libdir}/xorg/modules/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xorg/modules/libglamoregl.so
%{_datadir}/X11/xorg.conf.d/glamor.conf

%files libs
%defattr(644,root,root,755)
%doc COPYING ChangeLog README
%attr(755,root,root) %{_libdir}/libglamor.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libglamor.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libglamor.so
%{_includedir}/xorg/glamor.h
%{_pkgconfigdir}/glamor.pc
%{_pkgconfigdir}/glamor-egl.pc
