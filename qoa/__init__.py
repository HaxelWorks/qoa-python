# %% imports
import _qoa
import numpy as np


def read(filename: str) -> np.ndarray[np.int16]:
    """
    Reads a qoa file and returns the data as a numpy array.
    """
    filename = filename.encode("utf-8")
    desc = _qoa.ffi.new("qoa_desc *")
    pointer = _qoa.lib.qoa_read(filename, desc)
    assert pointer, "Could not read file"

    buffer = _qoa.ffi.buffer(pointer, desc.channels * desc.samples * 2)

    # convert the data to a numpy array
    original_shape = (desc.channels, desc.samples)

    # Convert the CFFI pointer back to numpy array
    array = np.frombuffer(buffer, dtype=np.int16)

    # Reshape the array to the original shape
    array = array.reshape(original_shape, order="F")

    return array.astype(np.int16)


def write(
    filename: str,
    samples: np.ndarray[np.int16],
    samplerate=44100,
) -> int:
    """
    Writes a numpy array to a qoa file.
    """
    filename = filename.encode("utf-8")

    desc = _qoa.ffi.new("qoa_desc *")
    desc.channels = samples.shape[0]
    desc.samples = samples.shape[1]
    desc.samplerate = samplerate

    # convert the data to a CFFI array
    data = samples.ctypes.data
    array = _qoa.ffi.cast("short*", data)
    nframes = _qoa.lib.qoa_write(filename, array, desc)
    return nframes

