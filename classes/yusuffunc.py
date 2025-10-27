from datetime import datetime


class YusufMat:

    @staticmethod
    def yadd(a, b):
        return a + 2*b

    @staticmethod
    def yprint(msg):
        """Print the current datetime followed by the message."""
        print(datetime.now())
        print(msg)
