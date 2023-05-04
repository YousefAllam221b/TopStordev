#!/usr/bin/sh
fnupdate () {
	git checkout -b $1
	git checkout  $1
	#git reset --hard
	git add --all
	git rm -rf __py*
	git commit -am 'fixing' 
	git push origin $1
	if [ $? -ne 0 ];
	then
		fold=`pwd | awk -F'/' '{print $NF'`
		echo something went wrong while updating $1 in directory $fold.... consult the devleloper
		exit
	fi
	sync
	sync
	sync
}

cd /TopStor/
echo `git show --abbrev-commit | grep commit ` > /TopStor/lastcommit
git add --all
git commit -am'fixing'
sleep 1
cjobs=(`echo TopStor pace topstorweb`)
branch=$1
branchc=`echo $branch | wc -c`
if [ $branchc -le 3 ];
then
	echo no valid branch is supplied .... exiting
	exit
fi 
flag=1
while [ $flag -ne 0 ];
do
	rjobs=(`echo "${cjobs[@]}"`)
	echo rjobs=${rjobs[@]}
	for job in "${rjobs[@]}";
	do
		echo '###########################################'
 		echo $job
		cd /$job
		if [ $? -ne 0 ];
		then
			echo the directory $job is not found... exiting
			exit
		fi
		fnupdate $branch 
		cjobs=(`echo "${cjobs[@]}" | sed "s/$job//g" `)
  	done
	lencjobs=`echo $cjobs | wc -c`
	if [ $lencjobs -le 3 ];
	then
		flag=0
	fi
done
cd /TopStor
echo finished
