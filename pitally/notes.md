# burn new image

sudo sh make_image.sh
/opt/etcher-cli/balena-etcher  -d /dev/mmcblk0 ./pitally_image.img


# setup ftp server

#Install pitally

# setup pureftpd
yaourt -S pure-ftpd tree ffmpeg


pure-pw useradd pi -u ftp -d /srv/ftp # pitally_01234
#pure-pw passwd pi
pure-pw mkdb
echo "/bin/false" >> /etc/shells

echo "
ChrootEveryone               no
BrokenClientsCompatibility   no
MaxClientsNumber             50
Daemonize                    yes
ChrootEveryone               no
BrokenClientsCompatibility   no
MaxClientsNumber             50
Daemonize                    yes
MaxClientsPerIP              8
VerboseLog                   no
DisplayDotFiles              yes
AnonymousOnly                no
NoAnonymous                 no
SyslogFacility none
FortunesFile /etc/pure-ftpd/welcome.msg
DontResolve                  yes
MaxIdleTime                  15
PureDB                       /etc/pureftpd.pdb
LimitRecursion               10000 8
AnonymousCanCreateDirs       no
MaxLoad                      4
AntiWarez                    no
Umask                        133:022
MinUID                       14
AllowUserFXP                 no
AllowAnonymousFXP            no
ProhibitDotFilesWrite        no
ProhibitDotFilesRead         no
AutoRename                   no
AnonymousCantUpload          yes
AltLog clf:/var/log/pureftpd.log
KeepAllFiles                 yes
CreateHomeDir                yes
MaxDiskUsage                   99
CustomerProof                yes
NoTruncate                   yes
TLS 0
TLSCipherSuite -S:HIGH:MEDIUM:+TLSv1
" > /etc/pure-ftpd/pure-ftpd.conf

sudo chown ftp:ftp /srv/ftp
sudo systemctl enable pure-ftpd.service
sudo pitally_drive.sh --enable-service


#test :
dd if=/dev/zero of=/tmp/test_ftp count=1024 bs=1024
wput /tmp/test_ftp  ftp://pi:pitally_01234@localhost
curl ftp://localhost/tmp/test_ftp > /dev/null

#router

uci set system.@system[0].hostname='pitally-router'
uci commit system
/etc/init.d/system reload

