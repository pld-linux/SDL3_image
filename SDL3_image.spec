#
# Conditional build:
%bcond_without	avif		# AV1 Image File Format support
%bcond_without	jxl		# JPEG XL support

Summary:	Simple DirectMedia Layer 3 - Sample Image Loading Library
Summary(pl.UTF-8):	Przykładowa biblioteka do ładowania obrazków dla SDL3
Summary(pt_BR.UTF-8):	Simple DirectMedia Layer 3 - Biblioteca exemplo para carga de Imagens
Name:		SDL3_image
Version:	3.2.4
Release:	1
License:	Zlib-like
Group:		Libraries
#Source0Download: https://github.com/libsdl-org/SDL_image/releases
Source0:	https://github.com/libsdl-org/SDL_image/releases/download/release-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	42d93037a22c5a5bb3b1eacbef072b2f
URL:		https://github.com/libsdl-org/SDL_image
BuildRequires:	SDL3-devel >= 3.2.6
BuildRequires:	cmake >= 3.16
%{?with_avif:BuildRequires:	libavif-devel >= 1.0}
BuildRequires:	libjpeg-devel >= 8
%{?with_jxl:BuildRequires:	libjxl-devel}
BuildRequires:	libpng-devel >= 2:1.6.0
BuildRequires:	libtiff-devel >= 4
BuildRequires:	libwebp-devel >= 0.6.0
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	rpmbuild(macros) >= 1.605
Requires:	SDL3 >= 3.2.6
%{?with_avif:Suggests:	libavif >= 1.0}
Suggests:	libjpeg >= 8
%{?with_jxl:Suggests:	libjxl}
Suggests:	libpng >= 2:1.6.0
Suggests:	libtiff >= 4
Suggests:	libwebp >= 0.6.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# NOTE: libraries dlopened by sonames detected at build time:
# libavif.so.16
# libjpeg.so.8
# libjxl.so.0.11
# libpng16.so.16
# libtiff.so.5
# libwebp.so.7
# libwebpdemux.so.2

%description
This is a simple library to load images of various formats as SDL3
surfaces. This library currently supports AVIF, BMP, GIF, JPEG,
JPEG-XL, LBM, PCX, PNG, PNM (PBM/PGM/PPM), QOI, TGA, TIFF, WebP, XCF
and XPM formats.

%description -l pl.UTF-8
Jest to prosta biblioteka służąca do ładowania różnego formatu
obrazków jako powierzchni SDL3. W chwili obecnej biblioteka obsługuje
następujące formaty: AVIF, BMP, GIF, JPEG, JPEG-XL, LBM, PCX, PNG, PNM
(PBM/PGM/PPM), QOI, TGA, TIFF, WebP, XCF oraz XPM.

%description -l pt_BR.UTF-8
Simple DirectMedia Layer 3 - Biblioteca exemplo para carga de Imagens.

%package devel
Summary:	Header files and more to develop SDL3_image applications
Summary(pl.UTF-8):	Pliki nagłówkowe do rozwijania aplikacji używających SDL3_image
Summary(pt_BR.UTF-8):	Bibliotecas e arquivos de inclusão para desenvolvimento de aplicações SDL3
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	SDL3-devel >= 3.2.6

%description devel
Header files and more to develop SDL3_image applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe do rozwijania aplikacji używających SDL3_image.

%description devel -l pt_BR.UTF-8
Bibliotecas e arquivos de inclusão para desenvolvimento de aplicações
SDL3.

%prep
%setup -q

%build
%cmake -B build \
	-DSDLIMAGE_INSTALL_MAN=ON \
	%{!?with_avif:-DSDLIMAGE_AVIF=OFF} \
	%{?with_jxl:-DSDLIMAGE_JXL=ON} \
	-DSDLIMAGE_STRICT=ON \

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install build/showanim $RPM_BUILD_ROOT%{_bindir}/sdl3-showanim
install build/showimage $RPM_BUILD_ROOT%{_bindir}/sdl3-showimage

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.md
%attr(755,root,root) %{_bindir}/sdl3-showanim
%attr(755,root,root) %{_bindir}/sdl3-showimage
%attr(755,root,root) %{_libdir}/libSDL3_image.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libSDL3_image.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libSDL3_image.so
%{_libdir}/cmake/SDL3_image
%{_includedir}/SDL3_image
%{_pkgconfigdir}/sdl3-image.pc
%{_mandir}/man3/IMG_Animation.3type*
%{_mandir}/man3/IMG_FreeAnimation.3*
%{_mandir}/man3/IMG_Load*.3*
%{_mandir}/man3/IMG_Read*.3*
%{_mandir}/man3/IMG_Save*.3*
%{_mandir}/man3/IMG_Version.3*
%{_mandir}/man3/IMG_is*.3*
%{_mandir}/man3/SDL_IMAGE_*.3*
