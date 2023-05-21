from pathlib import Path


def check_imgpath(imgpath: Path, imgfile: list[str]) -> Path:
    Path(imgpath).mkdir(parents=True, exist_ok=True)

    for afilename in imgfile:
        imgpath = imgpath / afilename
        Path(imgpath).mkdir(parents=True, exist_ok=True)
    return imgpath
