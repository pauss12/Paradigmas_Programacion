# Ejercicio: implementar, utilizando una interfaz grafica de TKInter y reactivex, un
# programa que se dedique a escuchar el Topic Kafka “PAPR_MAIS”, “PAPR_INSOA”
# o “PAPR_INSOBC” según el grupo que os corresponda. El programa tendrá un
# Observable que incluirá el KafkaConsumer y se encargará de leer los mensajes.
# Cada vez que se reciba uno, lo emitiremos a los obsevers, que se encargarán de
# actualizar la interfaz gráfica y de imprimir el mensaje por terminal

from tkinter import Tk, Label, Button, Text, END
from kafka import KafkaConsumer
import threading

class KafkaListener:
    def _init_(self, topic):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers='pkc-l6wr6.europe-west2.gcp.confluent.cloud:9092',
            security_protocol='SASL_SSL',
            sasl_mechanism='PLAIN',
            sasl_plain_username='WKIAB3JMF7ZJZ26U',
            sasl_plain_password='4sQiwHFUoQDAr7BJufwWqHz99/K0R4o4iSx4Phf00rn5PQfa0TfvAwyGP/6tVY9c',
            auto_offset_reset='latest'
            )

    def start_listening(self, onMsg):
        for msg in self.consumer:
            onMsg(msg.value.decode("utf-8"))

class KafkaUI:
    def _init_(self):
        self.window = Tk()
        self.window.title("Kafka UI")

        self.entry = Entry()
        self.entry.grid(row=0, column=0)

        self.button = Button(text="Escuchar", command=self.start_kafka_listening)
        self.button.grid(row=0, column=1)

        self.text = Text()
        self.text.grid(row=1, column=0, columnspan=2)

        self.window.mainloop()

    def start_kafka_listening(self):
        observable = create(self.observable_kafka)
        observable.subscribe(on_next=lambda s: self.update_ui_text(s))

    def update_ui_text(self, data):
        self.text.insert(END, "\n" + str(data))

    def observable_kafka(self, observer, scheduler):
        topic = self.entry.get()
        listener = KafkaListener(topic)
        thread = threading.Thread(target=listener.start_listening, args=(observer.on_next,))
        thread.start()

KafkaUI()