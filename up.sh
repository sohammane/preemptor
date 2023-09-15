function trap_ctrlc ()
{
    # perform cleanup here
    docker-compose down
 
    # exit shell script with error code 2
    # if omitted, shell script will continue execution
    exit 2
}
trap "trap_ctrlc" 2

# renew certificates
certbot renew
cp /etc/letsencrypt/live/qa.api.preemptor.ai/fullchain.pem packages/nginx/
cp /etc/letsencrypt/live/qa.api.preemptor.ai/privkey.pem packages/nginx/
# build & run
docker-compose -f docker-compose.prod.yml up -d --build --remove-orphans
docker-compose logs -f --tail=15 web-server face-embedding-server voice-embedding-server text-embedding-server
