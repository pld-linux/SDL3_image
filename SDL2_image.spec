#
# Conditional build:
%bcond_without	avif		# AV1 Image File Format support
%bcond_without	jxl		# JPEG XL support

Summary:	Simple DirectMedia Layer 2 - Sample Image Loading Library
Summary(pl.UTF-8):	Przykładowa biblioteka do ładowania obrazków dla SDL2
Summary(pt_BR.UTF-8):	Simple DirectMedia Layer 2 - Biblioteca exemplo para carga de Imagens
Name:		SDL2_image
Version:	2.6.3
Release:	2
License:	Zlib-like
Group:		Libraries
Source0:	https://github.com/libsdl-org/SDL_image/releases/download/release-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	191c3eb49cc2dce30abff81398a92e81
Patch0:		%{name}-libjpeg.patch
Patch1:		relax-soname-pattern.patch
URL:		https://github.com/libsdl-org/SDL_image
BuildRequires:	SDL2-devel >= 2.0.9
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_avif:BuildRequires:	libavif-devel}
BuildRequires:	libjpeg-devel >= 8
%{?with_jxl:BuildRequires:	libjxl-devel}
BuildRequires:	libpng-devel >= 2:1.6.0
BuildRequires:	libtiff-devel >= 4
BuildRequires:	libtool >= 2:2
BuildRequires:	libwebp-devel >= 0.6.0
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	rpmbuild(macros) >= 1.527
Requires:	SDL2 >= 2.0.9
%{?with_avif:Suggests:	libavif}
Suggests:	libjpeg >= 8
%{?with_jxl:Suggests:	libjxl}
Suggests:	libpng >= 2:1.6.0
Suggests:	libtiff >= 4
Suggests:	libwebp >= 0.6.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# NOTE: libraries dlopened by sonames detected at build time:
# libavif.so.15
# libjpeg.so.8
# libjxl.so.0.8
# libpng16.so.16
# libtiff.so.5
# libwebp.so.7

%description
This is a simple library to load images of various formats as SDL2
surfaces. This library currently supports BMP, GIF, JPEG, LBM, PCX,
PNG, PNM (PBM/PGM/PPM), TGA, TIFF, WebP, XCF and XPM formats.

%description -l pl.UTF-8
Jest to prosta biblioteka służąca do ładowania różnego formatu
obrazków jako powierzchni SDL2. W chwili obecnej biblioteka obsługuje
następujące formaty: BMP, GIF, JPEG, LBM, PCX, PNG, PNM (PBM/PGM/PPM),
TGA, TIFF, WebP, XCF oraz XPM.

%description -l pt_BR.UTF-8
Simple DirectMedia Layer 2 - Biblioteca exemplo para carga de Imagens.

%package devel
Summary:	Header files and more to develop SDL2_image applications
Summary(pl.UTF-8):	Pliki nagłówkowe do rozwijania aplikacji używających SDL2_image
Summary(pt_BR.UTF-8):	Bibliotecas e arquivos de inclusão para desenvolvimento de aplicações SDL2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	SDL2-devel >= 2.0.9

%description devel
Header files and more to develop SDL2_image applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe do rozwijania aplikacji używających SDL2_image.

%description devel -l pt_BR.UTF-8
Bibliotecas e arquivos de inclusão para desenvolvimento de aplicações
SDL2.

%package static
Summary:	Static SDL2_image libraries
Summary(pl.UTF-8):	Statyczne biblioteki SDL2_image
Summary(pt_BR.UTF-8):	Bibliotecas estáticas para desenvolvimento de aplicações SDL2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Statis SDL2_image libraries.

%description static -l pl.UTF-8
Statyczne biblioteki SDL2_image.

%description static -l pt_BR.UTF-8
Bibliotecas estáticas para desenvolvimento de aplicações SDL2.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-stb-image \
	%{__enable_disable avif} \
	--enable-avif-shared \
	--enable-bmp \
	--enable-gif \
	--enable-jpg \
	--enable-jpg-shared \
	%{__enable_disable jxl} \
	--enable-jxl-shared \
	--enable-lbm \
	--enable-pcx \
	--enable-png \
	--enable-png-shared \
	--enable-pnm \
	--enable-qoi \
	--enable-svg \
	--enable-tga \
	--enable-tif \
	--enable-tif-shared \
	--enable-webp \
	--enable-webp-shared \
	--enable-xcf \
	--enable-xpm \
	--enable-xv

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install .libs/showimage $RPM_BUILD_ROOT%{_bindir}/sdl2show

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.txt
%attr(755,root,root) %{_bindir}/sdl2show
%attr(755,root,root) %{_libdir}/libSDL2_image-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libSDL2_image-2.0.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libSDL2_image.so
%{_libdir}/cmake/SDL2_image
%{_includedir}/SDL2/SDL_image.h
%{_pkgconfigdir}/SDL2_image.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libSDL2_image.a
