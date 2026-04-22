import rclpy
from rclpy.node import Node
from autopatrol_interface.srv import SpeechText
import espeakng

class Speaker(Node):
    def __init__(self):
        super().__init__('speaker')
        self.speaker = espeakng.Speaker()
        self.speaker.voice= 'zh'
        self.speaker_service = self.create_service(SpeechText, 'speechtext', self.speak_callback)

    def speak_callback(self, request, response):
        self.get_logger().info(f"is ready....")
        self.speaker.say(request.text)
        self.speaker.wait()
        response.result = True
        return response

def main():
    rclpy.init()
    node = Speaker()
    rclpy.spin(node)
    rclpy.shutdown()


