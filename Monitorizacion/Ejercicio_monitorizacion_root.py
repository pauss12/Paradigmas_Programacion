#Nos suscribimos a un canal; y nos quedamos esperando a que nos lleguen mensajes
#para mostrarlos por pantalla.

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from kafka import KafkaConsumer
import rx
from rx import operators as ops
from rx.subject import Subject
import threading

class KafkaApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Kafka Listener")

        # Definir el Subject antes de llamar a setup_ui
        self.kafka_subject = Subject()  # Observable para manejar los mensajes de Kafka

        self.setup_ui()
        self.consumer_thread = None

    def setup_ui(self):
        # Campo de entrada para el Topic de Kafka
        tk.Label(self.root, text="Kafka Topic:").pack(pady=5)
        self.topic_entry = tk.Entry(self.root)
        self.topic_entry.pack(pady=5)

        # Botón para iniciar la escucha
        self.start_button = tk.Button(self.root, text="Empezar a Escuchar", command=self.start_listening)
        self.start_button.pack(pady=5)

        # Campo de texto para mostrar los mensajes recibidos
        self.messages_text = ScrolledText(self.root, width=50, height=20)
        self.messages_text.pack(pady=10)

        # Observador que actualizará la UI y la terminal con cada mensaje recibido
        self.kafka_subject.pipe(
            ops.observe_on(rx.scheduler.ThreadPoolScheduler(1))
        ).subscribe(
            on_next=self.update_ui_with_message,
            on_error=self.handle_error
        )

    def start_listening(self):
        # Obtener el Topic del campo de entrada
        topic = self.topic_entry.get().strip()
        if not topic:
            self.messages_text.insert(tk.END, "Error: Debe ingresar un Topic.\n")
            return

        # Si hay un hilo de escucha en ejecución, terminarlo
        if self.consumer_thread and self.consumer_thread.is_alive():
            self.kafka_subject.on_error(Exception("Ya se está escuchando un Topic."))
            return

        # Iniciar un nuevo hilo para KafkaConsumer
        self.consumer_thread = threading.Thread(target=self.consume_messages, args=(topic,))
        self.consumer_thread.daemon = True  # Para cerrar el hilo con la aplicación
        self.consumer_thread.start()

    def consume_messages(self, topic):
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers='pkc-l6wr6.europe-west2.gcp.confluent.cloud:9092',
                security_protocol='SASL_SSL',
                sasl_mechanism='PLAIN',
                sasl_plain_username='WKIAB3JMF7ZJZ26U',
                sasl_plain_password='4sQiwHFUoQDAr7BJufwWqHz99/K0R4o4iSx4Phf00rn5PQfa0TfvAwyGP/6tVY9c',
                auto_offset_reset='latest'
            )

            for msg in consumer:
                # Emitir el mensaje al observable
                self.kafka_subject.on_next(msg.value.decode("utf-8"))

        except Exception as e:
            self.kafka_subject.on_error(e)

    def update_ui_with_message(self, message):
        # Insertar el mensaje en el campo de texto y en la terminal
        self.messages_text.insert(tk.END, f"{message}\n")
        self.messages_text.see(tk.END)  # Desplazar automáticamente al último mensaje
        print(message)

    def handle_error(self, error):
        # Manejar errores e informarlos en la UI
        self.messages_text.insert(tk.END, f"Error: {error}\n")
        print(f"Error: {error}")

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = KafkaApp(root)
    root.mainloop()