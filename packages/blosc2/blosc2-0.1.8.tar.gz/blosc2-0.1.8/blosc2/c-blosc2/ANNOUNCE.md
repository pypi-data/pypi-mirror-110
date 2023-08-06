# Announcing C-Blosc2 2.0.0 (final)
A fast, compressed and persistent data store library for C.

## What is new?

On behalf of the Blosc team, we are happy to announce the second C-Blosc2
release (Release Candidate 2) that is meant to be reviewed by users.  As of RC1
we are declaring both the API and the format frozen, and we are seeking for
feedback from the community so as to better check the library and declare it
apt for its use in production.

In RC2 there is improved support for AArch64 (aka ARM64), ARMv7l, ARMv6l
and powerpc64le. Thanks to Alexandr Romanenko, Mark Kittisopikul and Mosè Giordano
from the Julia packaging team for their help.

Also, we have implemented performance improvements in the BloscLZ codec
and updated different codecs to latest versions (zlib-ng and zstd).

There are a *lot* of new features in C-Blosc2 compared with C-Blosc, its predecessor.
Just have a look at [our RC1 blog](https://www.blosc.org/posts/blosc2-ready-general-review/)
where we list the main improvements, with some historical overview too.

C-Blosc2 should be backward compatible with C-Blosc, so you can start using it
right away and slowly begin to useits new functionality, like the new filters,
prefilters, super-chunks and frames.  See docs in: https://blosc2.readthedocs.io

**IMPORTANT**: Please note that, even if the API and format have been declared frozen,
that does *not* mean that Blosc2 is ready for production yet: bad bugs can still exist
at this stage.  So *do not assume* that your Blosc2 data can be read with future versions.
This is just a call for general review of the library.

For more info, please see the release notes in:

https://github.com/Blosc/c-blosc2/blob/master/RELEASE_NOTES.md

Also, there is blog post introducing the most relevant changes in Blosc2:

https://www.blosc.org/posts/blosc2-ready-general-review/

## What is it?

Blosc2 is a high performance data container optimized for binary data.  It builds on the shoulders of Blosc, the high performance meta-compressor (https://github.com/c-blosc).

Blosc2 expands the capabilities of Blosc by providing a higher lever container that is able to store many chunks on it (hence the super-block name).  It supports storing data on both memory and disk using the same API.  Also, it adds more compressors and filters.

## Download sources

The github repository is over here:

https://github.com/Blosc/c-blosc2

Blosc is distributed using the BSD license, see LICENSES/BLOSC2.txt
for details.

## Mailing list

There is an official Blosc mailing list at:

blosc@googlegroups.com
http://groups.google.es/group/blosc

## Tweeter feed

Please follow @Blosc2 to get informed about the latest developments.


Enjoy Data!
- The Blosc Development Team
