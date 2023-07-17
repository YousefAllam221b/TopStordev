#!/usr/bin/sh
fnupdate () {
	git add .
	git commit -m 'fixing'
	git checkout -b $1
	git checkout $1
	git reset --hard
	git clean -f
	git config --replace-all pull.rebase false
	git checkout -- *
	git rm -rf __py*
	origin=`git remote -v | grep 252 | head -1 | awk '{print $1}'`
	remote=`git remote -v | grep github | head -1 | awk '{print $1}'`
	git add .
	git commit -m 'fixing'
	git pull $remote $1
	git add .
	git commit -m 'fixing'
	if [ $? -ne 0 ];
	then
		echo something went wrong while pulling from remote $remote, branch: $1 .... consult the devleloper
		exit
	fi
	git push $origin $1
	if [ $? -ne 0 ];
	then
		echo something went wrong while pushing to origin: $origin, branch: $1 .... consult the devleloper
		exit
	fi
	sync
	sync
	sync
}
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
		isexit=1
		cd /$job
		if [ $? -ne 0 ];
		then
			echo $job | grep topstorweb
			if [ $? -eq 0 ];
			then
				cd /var/www/html/des20/
				if [ $? -eq 0 ];
				then
					isexit=0
				fi
			fi
			if [ $isexit -eq 1 ];
			then
				echo the directory $job is not found... exiting
				exit
			fi
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
git show | grep commit
echo finished
