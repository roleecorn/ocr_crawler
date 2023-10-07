from pathlib import Path
from typing import List


def check_imgpath(imgpath: Path, imgfile: List[str]) -> Path:
    Path(imgpath).mkdir(parents=True, exist_ok=True)

    for afilename in imgfile:
        imgpath = imgpath / afilename
        Path(imgpath).mkdir(parents=True, exist_ok=True)
    return imgpath
