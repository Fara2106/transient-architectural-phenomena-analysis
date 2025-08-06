if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit
fi
#docker run --name webserver-$1 -p $1:8080 tomcat-table-generator
taskset -c 0 docker run --name webserver-$1 -p $1:8080 --cap-add=sys_nice --cpus=1 --cpuset-cpus="0" tomcat-table-generator
