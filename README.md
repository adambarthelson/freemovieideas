# FreeMovieIdeas's Janky Image Text Extractor


## 1. Prerequisites (Install Git)
There are several ways to install Git on a Mac. The easiest is probably to install the Xcode Command Line Tools. On Mavericks (10.9) or above you can do this simply by trying to run git from the Terminal the very first time.
```
git --version
```
If you don’t have it installed already, it will prompt you to install it.


### 2. Git clone and this repository
```
cd ~/Desktop && git clone https://github.com/adambarthelson/freemovieideas.git && cd "$(basename "$_" .git)" && open .
```

### 3. Move movie idea images into the `images_to_extract` folder (can do so via a manual copy/paste)


## Installation (via same Terminal window)

1. Install [Docker]()
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Build docker image (took my machine ~2 min)
```
docker build -t fmi .
```

## Extract those movie ideas!
```
docker run --rm --volume $(pwd):/app fmi:latest python3 freemovieideas.py
```

An excel file can now be found at `freemovieidea-archive.xlsx` in your current directory.
