#docker run --restart unless-stopped --name git -v /root/gitrepo:/usr/local/apache2/htdocs/ --hostname sgit -p 10.11.11.252:80:80 -v /root/gitrepo/httpd.conf:/usr/local/apache2/conf/httpd.conf -itd -v /root/gitrepo/hosts:/etc/hosts -v /root/gitrepo/resolv.conf:/etc/resolv.conf git
docker run --name intdns --restart unless-stopped --hostname sintdns --net bridge0 -e DNS_DOMAIN=qs.dom -e DNS_IP=10.11.12.7 -e LOG_QUERIES=true -itd --ip 10.11.12.7 docksal/dns
docker run --restart unless-stopped --name git -v /root/gitrepo:/usr/local/apache2/htdocs/ --hostname sgit -p 10.11.11.252:80:80 -v /root/gitrepo/httpd.conf:/usr/local/apache2/conf/httpd.conf -itd -v /root/gitrepo/resolv.conf:/etc/resolv.conf git
#docker run --name pxe --restart unless-stopped -v /root/gitrepo:/usr/local/apache2/htdocs/ --hostname spxe --net host -itd -v /root/gitrepo/hosts:/etc/hosts --cap-add=NET_ADMIN -v /root/gitrepo/resolv.conf:/etc/resolv.conf: pxe 
#docker run --name intpxe --restart unless-stopped --hostname intpxe --net bridge0 -itd -v /root/gitrepo/hosts:/etc/hosts --cap-add=NET_ADMIN -v /root/gitrepo/resolv.conf:/etc/resolv.conf -p 10.11.12.8:53:53 pxe 
#docker run --restart unless-stopped --name httpd --hostname localhost --net bridge0  -v /root/gitrepo/hosts:/etc/hosts -v /root/gitrepo/resolv.conf:/etc/resolv.conf -p 10.11.12.8:19999:19999 -p 10.11.12.8:5001:5001 -p 10.11.12.8:80:80 -p 10.11.12.8:443:443 -v /root/topstorwebetc/httpd.conf:/usr/local/apache2/conf/httpd.conf -v /root/topstorwebetc:/usr/local/apache2/topstorwebetc -v /root/topstorweb:/usr/local/apache2/htdocs/ -itd git
docker run --restart unless-stopped --name httpd --hostname shttpd --net bridge0 -v /root/gitrepo/resolv.conf:/etc/resolv.conf -p 10.11.12.8:19999:19999 -p 10.11.12.8:5001:5001 -p 10.11.12.8:80:80 -p 10.11.12.8:443:443 -v /root/topstorwebetc/httpd.conf:/usr/local/apache2/conf/httpd.conf -v /root/topstorwebetc:/usr/local/apache2/topstorwebetc -v /root/topstorweb:/usr/local/apache2/htdocs/ -itd git
