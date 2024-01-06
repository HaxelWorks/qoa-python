# QOA-Python
## The Quite OK Audio Format for Fast, Lossy Compression

A  Python wrapper around [qoa](https://github.com/phoboslab/qoa) Written using the amazing CFFI library.

## Why?

- QOA is fast. It decodes audio 3x faster than Ogg-Vorbis, while offering better quality and compression (278 kbits/s for 44khz stereo) than ADPCM.
- QOA is simple. The reference en-/decoder fits in about 400 lines of C. The file format specification is a single page PDF.
- Lossless with comparable compression to PNG, but fast! It encodes 10x faster and decodes around 5x faster than PNG in OpenCV or PIL.
- Multi-threaded - no GIL hold-ups here.

## Install

```sh
pip install qoa
```

## Usage

You can use the `qoa` library to encode and decode audio files. Here's a basic example:

```python
import qoa

# Read an audio file
np_array = qoa.read('path/to/file')

# Write an audio file
qoa.write(np_array , 'path/to/file')

# Decode an audio file
buffer,shape = qoa.decode('path/to/file')

# Encode an audio file
ffi_buffer = qoa.encode(np_array)
```
