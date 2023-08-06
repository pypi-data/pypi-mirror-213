# pictl

A command line tool for Image Compression and Upload (ex. S3-type)

## Why a new project

When I publish blog articles, it's quite inefficient for me to prepare images.

Although there exist many good enough tools, like [uPic](https://github.com/gee1k/uPic), [PicGo](https://github.com/Molunerfinn/PicGo), and so on, they still cannot meet my need completely.

For me, these points are very necessary:

- All images should be compressed and transformed into `webp` format (less storage and loading time).
- All images can be uploaded to S3-like object storage with a unique short name.
- It should be very easy to use. It‘s better if no web UI or GUI. Command line first.
- (Optional) The customized watermark can be added into all images automatically.
- (Optional) All images can be resized into the defined default size automatically.
- (Optional) It defaults to read the image from the clipboard.

Actually uPic and PicGo can provide most of the above functions, but not so good in some points.

- They don't provide the transformation to `webp` format.
- They don't provide the support for Cloudflare R2 (though uPic paid version in appstore provides it).

It's quite time-consuming for me to write a plugin for PicGo or rewrite codes for uPic.

So why not write a new tool?

## The project name

Because it's designed for image helper in writing blog articles and using only with command line,
it's named PICTL, a short name for **Pi**cture **C**on**t**ro**l**.

## The architecture

Here is the architecture of this project.

It seems very similar to PicGo 😂, but it will be different.

![The architecture](https://github.com/zhonger/pictl/assets/12064158/4560bc88-c58e-4f35-8dd3-0ccc4ff36673)

## Installation

### From source

```bash
git clone https://github.com/zhonger/pictl
cd pictl
pip3 install .
```

### PIP

```bash
pip3 install pictl
```

### Brew

```bash
brew tap zhonger/pictl
brew install pictl
```

## Usage

### Config

The config file for PICTL is named `.pictlrc` with `toml` format. The global config file is located at `~/.pictlrc`. The local config file is located at `./.pictlrc`. If there is a local config file, it will be used firstly. If the necessary settings cannot be found in the local config file, the settings in the global config file will be used instead.

#### Manually

```bash
[basic]
length = 6
algorithm = "sha1"

[upload]
endpoint = "https://s3.amazonaws.com"
key = "qwqewqwqeqweqwe"
secret = "dadfadaeqweqeqe"
url = "https://i.lisz.me"
```

### Interactive way
