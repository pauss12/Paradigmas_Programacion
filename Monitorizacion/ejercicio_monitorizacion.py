from kafka import KafkaConsumer
import rx
from rx import operators as ops
from rx.scheduler import ThreadPoolScheduler
from tkinter import Tk, Label, Entry, Button, Text, END
import threading

class KafkaUI:

    def __init__(self, topic):

        self.topic = topic

        self.window = tk.Tk()

        # Configuración del consumidor de Kafka
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers='pkc-l6wr6.europe-west2.gcp.confluent.cloud:9092',
            security_protocol='SASL_SSL',
            sasl_mechanism='PLAIN',
            sasl_plain_username='WKIAB3JMF7ZJZ26U',
            sasl_plain_password='4sQiwHFUoQDAr7BJufwWqHz99/K0R4o4iSx4Phf00rn5PQfa0TfvAwyGP/6tVY9c',
            auto_offset_reset='latest'
        )
        
    def observable_subscribe(observer, scheduler):
        topic = input("Ingrese el nombre del Topic de Kafka: ").strip()

    def star_kafka_listening(self):
        observable = create(self.observable_kafka)
        observable.suscribe(on_next=lambda x: self.update_ui_text(x))

    def update_ui_text(self, message):
        self.text.insert(END, "\n" + str(message))



    def start_listening(self):
        # Emitimos cada mensaje recibido al sujeto para que el observador lo procese
        for msg in self.consumer:
            self.kafka_subject.on_next(msg.value.decode("utf-8"))


    def observable_kafka(observer, scheduler):
        topic = self.entry.get().strip()
        if not topic:
            print("Error: Debe ingresar un Topic.")
            return
        else:
            listener = KafkaListener(topic)
            thread1 = threading.Thread(target=listener.start_listening, args=(observable,))
            thread1.start()