import paho.mqtt.client as MQTT
from typing import Callable
import time

class MqttConnection:
    def __init__(self, broker: str, port: int) -> None:
        """ 
            #### Classe para gerenciar o protocolo mqtt

            ##### Parâmetros

            * `broker`: str &rarr; URL do Broker MQTT

            * `port`: str &rarr; Porta TCP do Broker MQTT
        """
        self.broker = broker
        self.port = port
        self.client = MQTT.Client()
        self.subscribedTopics: dict = {}

        # Exibe uma mensagem quando o cliente se conecta ao Broker
        self.client.on_connect = lambda client, userdata, flags, reason_code : print(f"Connected with {self.broker}. Code: {str(reason_code)}")
        
        def callback(client, userdata, message):
            """#### Função para tratar a mensagem recebida de tópicos inscritos"""
            
            topic = message.topic
            payload = message.payload.decode('utf-8')
            # print(f"Received message '{payload}' on topic '{topic}'")

            # Chama a função de callback definida na inscrição do tópico
            if topic in self.subscribedTopics:
                self.subscribedTopics[topic](payload)

        self.client.on_message = callback

        self.client.connect(self.broker, self.port)

        #Inicia uma thread para verificar mensagens de receita
        self.client.loop_start()

    def publish(self, payload: str | int | float | bool, topic: str) -> bool:
        """#### Função para publicar uma dada mensagem no tópico determinado"""

        msg = self.client.publish(topic, payload)
        return msg.is_published()

    def subscribe(self, topic: str, callback: Callable[[str], None]) -> bool: 
        """#### Increve em um tópico e atribue uma função callback para lidar com as mensagens recebidas"""

        result, _ = self.client.subscribe(topic)
        if result == MQTT.MQTT_ERR_SUCCESS:
            self.subscribedTopics[topic] = callback
            return True
        return False
    
    def disconnect(self):
        """#### Disconecta do Broker"""
        self.client.disconnect()

# exemplo
broker_address = "broker.hivemq.com"
broker_port = 1883

publishTopic = "sg1000"

alertMessage = "alerta"

desarmMessage = "desarme"

#criar instância da classe MQTT
server = MqttConnection(broker_address, broker_port)

#tempo para conectar com o broker
time.sleep(1)

server.publish(alertMessage, publishTopic)

time.sleep(5)

server.publish(desarmMessage, publishTopic)

time.sleep(1)


# subcribeTopic = "sg2000" 

# #função de teste para lidar com mensagem recebias pelo tópico sg1000
# def on_sg1000_message(msg):
#     print(msg)

# #se increve no tópico "sg1000" e lida com as mensagem recebidas na função acima
# server.subscribe(subcribeTopic,on_sg1000_message)




