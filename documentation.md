weather csv file link https://corgis-edu.github.io/corgis/csv/weather/


install hdfs
https://www.digitalocean.com/community/tutorials/how-to-install-hadoop-in-stand-alone-mode-on-ubuntu-18-04

install hadoop specific version
https://dlcdn.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz


run haddop command
1. cat new.txt | python mapper.py | sort -k1,1 | python reducer.py
2. fix issues hdfs
    export HADOOP_INSTALL=/usr/local/hadoop
    export PATH=$PATH:$HADOOP_INSTALL/bin
    export PATH=$PATH:$HADOOP_INSTALL/sbin
    export HADOOP_MAPRED_HOME=$HADOOP_INSTALL
    export HADOOP_COMMON_HOME=$HADOOP_INSTALL
    export HADOOP_HDFS_HOME=$HADOOP_INSTAL
    export YARN_HOME=$HADOOP_INSTALL
    export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_INSTALL/lib/native
    export HADOOP_OPTS="-Djava.library.path=$HADOOP_INSTALL/lib"
3. put file in server 
   hdfs dfs -put ./new.txt   ./hdfs
sudo /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar -file ./mapper.py -mapper ./mapper.py -file ./reducer.py -reducer reducer.py -input ./new -output ./newcount