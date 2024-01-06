import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from typing import Generator, Iterable

import soundfile as sf
from colorama import Fore
from tqdm.auto import tqdm as tqdm_auto
from tqdm.rich import tqdm as tqdm_rich

import qoa

MAX_WORKERS = 8
N_FILES = 106_574

SRC_FMT = ".mp3"  # must inclucle dot
DST_FMT = ".qoa"  # must inclucle dot
SRC_DIR = r"\\ANA\Muziek\Datasets\Free-Music-Archive\fma_mp3"
DST_DIR = r"C:\Users\axel1\Cache\fma_qoa"

# if the source dir does not exist, create it
if not os.path.exists(SRC_DIR):
    os.makedirs(SRC_DIR)

# DST_DIR = r"\\ANA\Muziek\Datasets\Free-Music-Archive\fma_qoa"
assert SRC_DIR != DST_DIR, "Source and target cannot be the same folder."


class STATS:
    total = 0
    completed = 0
    ffmpeg = 0
    soundfile = 0
    unreadable = 0
    skipped = 0

    @classmethod
    def print(cls):
        if cls.total == 0 or cls.ffmpeg == 0:
            return
        os.system("cls")
        fail_rate = cls.unreadable / cls.total
        succ_rate = cls.completed / cls.total
        ffmpeg_rate = cls.ffmpeg / cls.total
        sf_rate = cls.soundfile / cls.total
        fail_rate = cls.unreadable / cls.total

        skip_rate = cls.skipped / N_FILES
        messages = [
            Fore.BLUE + f"Soundfile: {cls.soundfile} ({sf_rate:.2%})",
            Fore.YELLOW + f"FFmpeg: {cls.ffmpeg} ({ffmpeg_rate:.2%})",
            Fore.GREEN + f"Completed: {cls.completed} ({succ_rate:.2%})",
            Fore.RED + f"Unreadable: {cls.unreadable} ({fail_rate:.2%})",
            Fore.LIGHTBLACK_EX + f"Skipped: {cls.skipped} ({skip_rate:.2%})",
        ]
        print(*messages, sep=Fore.RESET + " | ")


def audio_file_walker(path: str, file_ext="") -> Generator:
    """Walks a directory and yields audio file paths.
    if file_ext is specified, only files with that extension are yielded.
    if root is True, the root directory is also yielded.
    """

    with tqdm_auto(desc="Walking", total=N_FILES) as pbar:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(file_ext):
                    pbar.update()
                    if root:
                        yield os.path.join(root, file)
                    else:
                        yield file

def missing_files(src: Iterable, dst: Iterable) -> list:
    """Filters out files that already exist in the target folder."""

    # remove the file extensions by removing ater the last dot
    def convert(path):
        name = os.path.basename(path)
        name = os.path.splitext(name)[0]
        return int(name)

    src_dict = {convert(path): path for path in src}
    dst_set = {convert(path) for path in dst}

    missing_set = src_dict.keys() - dst_set
    s_names = sorted(missing_set)

    missing_files = [src_dict[name] for name in s_names]
    STATS.skipped = len(src_dict) - len(missing_files)
    return missing_files

def convert(path:str) -> bytes:
    STATS.total += 1
    STATS.unreadable += 1
    with open(path, "rb") as f:
        data = BytesIO(f.read())
    try:
        samples, sr = sf.read(data, dtype="int16", always_2d=True, fill_value=0)
        STATS.soundfile += 1
    except:
        try: # try ffmpeg
            samples, sr = ffmpeg(data)
            STATS.ffmpeg += 1
        except:
            return

    # transpose the samples
    samples = samples.T
    # take only the left channel
    samples = samples[0]
    # encode the samples
    enc = qoa.encode(samples, sr)

    path = os.path.basename(path)
    path = path.replace(SRC_FMT, DST_FMT)
    path = os.path.join(DST_DIR, path)
    STATS.completed += 1
    return enc, path


def ffmpeg(input_data: BytesIO):
    """Use ffmpeg to read the audio file."""
    ffmpeg_cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        "-",
        "-f",
        "wav",
        "pipe:1",
    ]
    input_data.seek(0)
    # Run the FFmpeg command and capture the stdout
    result = subprocess.run(ffmpeg_cmd, input=input_data.read(), stdout=subprocess.PIPE)
    # Convert the raw byte to a wav file
    bytes_io = BytesIO(result.stdout)
    # Read the wav file
    samples, sr = sf.read(bytes_io, dtype="int16", always_2d=True, fill_value=0)
    return samples, sr



mp3_walker = audio_file_walker(SRC_DIR, SRC_FMT)
qoa_walker = audio_file_walker(DST_DIR, DST_FMT)
missing_files = missing_files(mp3_walker, qoa_walker)
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
    converted = pool.map(convert, missing_files)
    progress = tqdm_rich(converted, total=N_FILES - STATS.skipped)
    for output in progress:
        STATS.print()
        if output:
            enc, output_path = output
            with open(output_path, "wb") as f:
                f.write(enc)
