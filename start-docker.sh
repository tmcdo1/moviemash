# Start Elasticsearch and Kibana
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" --name moviemash_es -d docker.elastic.co/elasticsearch/elasticsearch:7.6.0

echo "Letting Elasticsearch get configured. Might take a little bit"
sleep 30

docker run --link moviemash_es:elasticsearch -p 5601:5601 --name moviemash_kib -e "elasticsearch.hosts=http://moviemash_es:9200" -d docker.elastic.co/kibana/kibana:7.6.0

echo "Letting Kibana start up and connect to Elasticsearch. Might take a while..."
sleep 50

echo "Elasticsearch is running on port 9200. Checkout http://localhost:9200"

echo "Kibana is running on port 5601. Check out http://localhost:5601"

