config() {
  NEW="$1"
  OLD="$(dirname $NEW)/$(basename $NEW .new)"
  if [ ! -r $OLD ]; then
    mv $NEW $OLD
  elif [ "$(cat $OLD | md5sum)" = "$(cat $NEW | md5sum)" ]; then
    rm $NEW
  fi
}

FILES="slpkg repositories blacklist rules"
for file in $FILES; do
  install -D -m0644 configs/$file.toml $PKG/etc/slpkg/$file.toml.new
done