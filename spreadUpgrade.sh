#!/bin/sh
openssl pkeyutl -decrypt -inkey privateKey.pem -in aes256PassCipher.txt -out aes256PassDecipher.txt
openssl aes-256-cbc -d -pass file:./aes256PassDecipher.txt -in encZippedFolders.zip -out decZippedFolders.zip

temp_dir=$(mktemp -d)
unzip -q "decZippedFolders.zip" -d "$temp_dir"

#unzip decZippedFolders.zip -d upgradedDirs/
# Define the names of the three folders to replace files within
folder_names=("/TopStor" "/pace" "/topstorweb")

# Loop through the folder names and synchronize files using rsync
for folder_name in "${folder_names[@]}"; do
	folder_path="$temp_dir/$folder_name"
	
	# Check if the folder exists in the destination directory
	if [ -d "$folder_path" ]; then
	# Use rsync to copy only changed or new files to the destination directory
		rsync -avh --delete -r "$folder_path/" "/$folder_name"
		echo "Replaced files within $folder_name"
	else
		echo "Folder $folder_name does not exist in $destination_directory. Skipping."
	fi
done

# Clean up the temporary directory
rm -rf "$temp_dir"

echo "Replacement completed."
