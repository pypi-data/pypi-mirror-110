# Create app secret key:
secret: Makefile
	head -c 16 /dev/urandom | hexdump -e '"%x"' > $@

# Create manager authkey:
syncauth: Makefile
	head -c 16 /dev/urandom | hexdump -e '"%x"' > $@

# Copy example config:
config.py: config.py.example
	cp $< $@
