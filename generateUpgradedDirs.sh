#!/bin/sh
if [[ $1 = "generateKeys" ]]
then
	openssl genrsa -out privateKey.pem 2048
	openssl rsa -in privateKey.pem -pubout -out publicKey.pem
	openssl rand -out "aes256Pass.txt" 32
elif [[ $1 = "encrypt" ]]
then
	zip -r zippedFolders /TopStor /pace /topstorweb
	openssl aes-256-cbc -pass file:./aes256Pass.txt -in zippedFolders.zip -out encZippedFolders.zip
	openssl pkeyutl -encrypt -pubin -inkey publicKey.pem -in aes256Pass.txt -out aes256PassCipher.txt
else
	echo "Please enter the argument!"
fi
