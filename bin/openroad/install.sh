#!/bin/bash 

echo "#---------------------------------------"
echo "# Download OpenROAD alpha-release:"
echo "#---------------------------------------"

VERSION=2019-09-05_20-10
CWD=$PWD
curl -L -O https://github.com/The-OpenROAD-Project/alpha-release/releases/download/v${VERSION}/OpenROAD-${VERSION}.tar.gz
tar xvfz OpenROAD-${VERSION}.tar.gz
ln -s openroad/OpenROAD-${VERSION}/bin latest


# Remove yosys and download static yosys binaries.
## Google drive link: 
##     https://drive.google.com/open?id=1NKdesTjagx3lm4FGgcUHDuVilf-m2HCf
cd openroad/OpenROAD-${VERSION}/bin
rm -f yosys*

fileid="1NKdesTjagx3lm4FGgcUHDuVilf-m2HCf"
filename="openroad-yosys.tar.gz"

# Reference: https://gist.github.com/iamtekeste/3cdfd0366ebfd2c0d805#gistcomment-2359248
function gdrive_download () {
  CONFIRM=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "https://docs.google.com/uc?export=download&id=$1" -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')
  wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$CONFIRM&id=$1" -O $2
  rm -rf /tmp/cookies.txt
}

gdrive_download $fileid $filename
tar xvfz $filename

ln -sf openroad-yosys/* .
ln -s ../share

cd $CWD
