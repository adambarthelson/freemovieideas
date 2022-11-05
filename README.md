# FreeMovieIdeas's Janky Image Extractor


## 1. Prerequisites (Install Git)
There are several ways to install Git on a Mac. The easiest is probably to install the Xcode Command Line Tools. On Mavericks (10.9) or above you can do this simply by trying to run git from the Terminal the very first time.
```
git --version
```
If you don’t have it installed already, it will prompt you to install it.


### 2. Git clone and this repository
```
cd ~/Desktop && git clone http://repo_url.git && cd "$(basename "$_" .git)" && open .
```

### 3. Move movie idea images into the `images_to_extract` folder (can do so via a manual copy/paste)


## Installation (via same Terminal window)

1. Install [Homebrew](https://brew.sh)
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Brew install dependencies
```
brew install python3 tesseract
```

3. Install some important Python libraries
```
pip3 install pytesseract pandas openpyxl
```

4. Extract those movie ideas!
```
python3 freemovieideas.py
```

An excel file can now be found at `freemovieidea-archive.xlsx` in your current directory.
