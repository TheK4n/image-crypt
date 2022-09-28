pkgname='image-crypt'
pkgver=2.0.1
pkgrel=1
pkgdesc="Steganography encryption script"
arch=('x86_64')
license=('MIT')
depends=(
  'python3'
  'python-pillow'
  'python-pyqt5'
  'python-pycryptodomex'
)
makedepends=('git' 'python-setuptools')
url='https://github.com/thek4n/ImageCrypt'
conflicts=('image-crypt')
replaces=('image-crypt')
source=("$pkgname::git+https://github.com/thek4n/ImageCrypt.git#branch=master")
# target_directory::download_protocol+cipher_protocol://...
sha256sums=('SKIP')

package() {
    cd "$srcdir"/"$pkgname"
    # $srcdir - $PWD/src - source files directory
    # $pkgname - image-crypt - target directory downloaded by git
    # $pkgdir - $PWD/pkg - clone of host root, pkg/image-crypt/usr/bin/image-crypt
    make DESTDIR="$pkgdir" PREFIX="/usr" install
}
