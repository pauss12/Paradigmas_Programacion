
from kafka import KafkaConsumer


consumer = KafkaConsumer(
    "PAPR_MAIS",
    bootstrap_servers='pkc-l6wr6.europe-west2.gcp.confluent.cloud:9092',
    security_protocol='SASL_SSL',
    sasl_mechanism='PLAIN',
    sasl_plain_username='WKIAB3JMF7ZJZ26U',
    sasl_plain_password='4sQiwHFUoQDAr7BJufwWqHz99/K0R4o4iSx4Phf00rn5PQfa0TfvAwyGP/6tVY9c',
    auto_offset_reset='latest'
    )


for msg in consumer:
    print(msg.value.decode("utf-8"))



