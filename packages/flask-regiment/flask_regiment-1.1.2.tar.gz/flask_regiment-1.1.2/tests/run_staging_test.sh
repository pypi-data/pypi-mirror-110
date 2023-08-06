trap ctrl_c INT

function ctrl_c() {
    rm -rf ./flask_regiment;
}

rm -rf ./flask_regiment
cp -r ../flask_regiment flask_regiment

sed -i -e 's/domain = "ingest.regiment.tech"/domain = "ingest-staging.regiment.tech"/' ./flask_regiment/bulletlog.py;

FLASK_APP=simple_server FLASK_RUN_PORT=5001 flask run

rm -rf ./flask_regiment