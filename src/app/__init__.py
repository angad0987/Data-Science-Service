from flask import Flask, json
from flask import request,jsonify
from confluent_kafka import Producer
import os
from .services.messageService import MessageService

app=Flask(__name__)
app.config.from_pyfile('config.py')

messageService=MessageService()
kafka_host=os.getenv('KAFKA_HOST','kafka')
kafka_port=os.getenv('KAFKA_PORT','9092')
kafka_bootstrap_servers=f"{kafka_host}:{kafka_port}"


# Configure the producer
producer = Producer({'bootstrap.servers': kafka_bootstrap_servers})

@app.route('/v1/ds/message',methods=['POST'])
def handle_message():
    message=request.json.get('message')
    result=messageService.processMessage(message)
    resultdic=result.dict()
    serialisedResult = json.dumps(resultdic)
    producer.produce('expenseDetails', key='key1', value=serialisedResult)
    return jsonify(resultdic)

@app.route('/',methods=['GET'])
def index():
    print("This is the index file")

if __name__ == "__main__":
    app.run(host="localhost",port=8010,debug=True)
