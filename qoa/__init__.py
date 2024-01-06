from _qoa import ffi, lib
import numpy as np


def encode(samples: np.ndarray[np.int16], samplerate=44100) -> ffi.buffer:
    """
    Encodes the given samples into a qoa file format and returns the bytes.

    Args:
        samples (np.ndarray[np.int16]): The audio samples to encode.
        samplerate (int, optional): The sample rate of the audio. Defaults to 44100.

    Returns:
        ffi.buffer: The encoded audio data in bytes.
    """

    if not samples.dtype == np.int16:
        raise TypeError(f"Samples must be type np.int16, got {type(samples)}")

    # create the qoa_desc struct
    desc = ffi.new("qoa_desc *")
    desc.samplerate = samplerate

    # set the number of channels and samples
    if samples.ndim == 1:
        desc.channels = 1
        desc.samples = len(samples)
    else:
        desc.channels = samples.shape[0]
        desc.samples = samples.shape[1]

    # convert the data to a CFFI array
    data = samples.ctypes.data
    array = ffi.cast("short*", data)

    # create pointers for the output
    n_bytes = ffi.new("unsigned int *")
    ptr = lib.qoa_encode(array, desc, n_bytes)
    output = bytes(ffi.buffer(ptr, n_bytes[0]))
    lib.free(ptr)
    return output


def write(samples: np.ndarray[np.int16], filename: str, samplerate=44100):
    """
    Encodes the given samples into a qoa file format and writes it to a file.

    Args:
        samples (np.ndarray[np.int16]): The audio samples to encode.
        filename (str): The name of the file to write the encoded audio data to.
        samplerate (int, optional): The sample rate of the audio. Defaults to 44100.
    """
    output = encode(samples, samplerate)
    with open(filename, "wb") as f:
        f.write(output)


def decode(filename: str) -> (ffi.buffer, tuple):
    """
    Decodes a qoa file and returns the audio data and its shape.

    Args:
        filename (str): The name of the qoa file to decode.

    Returns:
        tuple: A tuple containing the decoded audio data in bytes and its shape.
    """
    filename = filename.encode("utf-8")
    desc = ffi.new("qoa_desc *")
    ptr = lib.qoa_read(filename, desc)
    ptr = ffi.gc(ptr, lib.free) # make sure memory is freed when the buffer is garbage collected
    buffer = ffi.buffer(ptr, desc.channels * desc.samples * 2) # 2 bytes per sample
    shape = (desc.channels, desc.samples)
    return buffer, shape


def read(filename: str) -> np.ndarray[np.int16]:
    """
    Reads a qoa file and returns the audio data as a numpy array.

    Args:
        filename (str): The name of the qoa file to read.

    Returns:
        np.ndarray[np.int16]: The audio data as a 16bit numpy array.
    """

    buffer, shape = decode(filename)
    array = np.frombuffer(buffer, dtype=np.int16)
    if array.size == 0:
        print(f"Could not read file {filename}")
        return None
    return array.reshape(shape, order="F")
