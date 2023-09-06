#!/bin/sh
if [[ $1 = "generateKeys" ]]
then
	openssl genrsa -out privateKey.pem 2048
	openssl rsa -in privateKey.pem -pubout -out publicKey.pem
	openssl rand -out "aes256Pass.txt" 32
elif [[ $1 = "encrypt" ]]
then
	openssl aes-256-cbc -pass file:./aes256Pass.txt -in zippedFolders.zip -out encZippedFolders.zip
	openssl pkeyutl -encrypt -pubin -inkey publicKey.pem -in aes256Pass.txt -out aes256PassCipher.txt
elif [[ $1 = "decrypt" ]]
then
	openssl pkeyutl -decrypt -inkey privateKey.pem -in aes256PassCipher.txt -out aes256PassDecipher.txt
	openssl aes-256-cbc -d -pass file:./aes256PassDecipher.txt -in encZippedFolders.zip -out decZippedFolders.zip
elif [[ $1 = "zip" ]]
then
	zip -r zippedFolders /TopStor /pace /topstorweb
else
	echo "Please enter the argument!"
fi
