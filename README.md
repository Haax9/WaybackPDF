# WaybackPDF

## :speech_balloon: Description

Small python tool used to recover and download archived PDF files for a given domain name. It uses the "Wayback Machine" from archive.org.
This tool is based on this <a href="https://openfacto.fr/2020/04/19/recuperer-des-fichiers-pdf-en-masse-sur-archive-org/" target="_blank" rel="noopener">OpenFacto research</a> and heavily inspired by <a href="https://twitter.com/yannguegan" target="_blank" rel="noopener">@yannguegan's</a> work. His first uploaded script is not reacheable anymore and was lacking some verifications on the gathered files, causing errors. These are the two reasons I recoded the tool and uploaded it.


## :memo: Prerequisite & Install

You only need to install `requests` module as the others used are built-in.

```bash
pip3 install requests
```

Then, simply run the following to install.

```bash
git clone https://github.com/Haax9/WaybackPDF.git
cd waybackPDF/
pip install -r requirements.txt
```

The tool was initially developped for Python3. It might contains some bugs, maybe depending on the structure of gathered data (PDF filenames etc.). Please don't hesitate to give a feedback if you find some.

## :book: Usage

```bash
$ python3 waybackPDF.py --help
usage: waybackPDF.py [-h] -d DOMAIN [-o OUTPUT] [--http HTTP] [-r RESUME]

OSINT tool to download archived PDF files from archive.org for a given
website.

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        The target domain you are looking for files
  -o OUTPUT, --output OUTPUT
                        Optional output directory (Default is the domain name)
  --http HTTP           Use HTTP instead of HTTPS for the target domain. The
                        default behavior uses HTTPS
  -r RESUME, --resume RESUME
                        Start downloading at a given index and skip X previous
                        files
```

## :computer: Example

The easiest way to run the tool and get PDF files is the following.

```bash
$ python3 waybackPDF.py --domain yeswehack.com

[+] Web Archive PDF Downloader 
[+] Target domain : yeswehack.com
[+] Output directory : yeswehack.com/

[*] Requesting PDF list...
[+] 2 PDFs found

[*] Downloading Files...
[+] (1/2) Saved bulletin-20120625001714.pdf
[+] (2/2) Saved YesWeHack-Comm-Presse-20140715174404.pdf

[*] Everything's done !
[*] Happy analysis !
```

However, for some reasons (previous run crashed, targetting specific files etc...) you may need to run the tool and skip some files. The `--resume` option is here for that. Just provide the number of files you want to skip and the tool will start downloading from this index.

```bash
$ python3 waybackPDF.py --domain yeswehack.com --resume 1

[+] Web Archive PDF Downloader
[+] Target domain : yeswehack.com
[+] Output directory : yeswehack.com/

[*] Requesting PDF list...
[+] 2 PDFs found

[*] Downloading Files...

[*] Resume switch on, skipping the first 1 file(s)
[+] (1/1) Saved YesWeHack-Comm-Presse-20140715174404.pdf

[*] Everything's done !
[*] Happy analysis !
```