#! /bin/bash
log_path="/tmp/dataflow.log"
app_name="dataflow"
topic="dataflow"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd $SCRIPT_DIR
[ -d "filebeat" ] && exit
curl -L -O https://wair.obs.cn-central-221.ovaijisuan.com/soft/filebeat.tar.gz
mkdir filebeat
tar -xvf filebeat.tar.gz -C filebeat
rm filebeat.tar.gz
sed -i "s#log_path#${log_path}#g" filebeat/filebeat.yml
sed -i "s/app_name/${app_name}/g" filebeat/filebeat.yml
sed -i "s/topic: modelarts/topic: ${topic}/g" filebeat/filebeat.yml
host=\"192.168.0.79:29090\",\"192.168.0.238:29091\",\"192.168.0.30:29092\"
host_new=\"kafka-cluster-kafka-0.kafka-cluster-kafka-brokers.logging.svc.cluster.local:9092\",\"kafka-cluster-kafka-1.kafka-cluster-kafka-brokers.logging.svc.cluster.local:9092\",\"kafka-cluster-kafka-2.kafka-cluster-kafka-brokers.logging.svc.cluster.local:9092\"
sed -i "s#${host}#${host_new}#g" filebeat/filebeat.yml

# 如果你的程序通过普通用户启动需要打开下面的开关,root启动不用修改
#chown -R ma-user:ma-group filebeat
# 后台启动filebeat
cd filebeat/
nohup ./filebeat -c filebeat.yml > stdout.log 2> stderr.log &

# 启动你的应用程序
cd ..