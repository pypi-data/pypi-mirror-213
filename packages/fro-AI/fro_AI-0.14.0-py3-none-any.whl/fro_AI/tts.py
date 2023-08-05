class TTS():

    def __init__(self, backend='pyttsx3') -> None:
        if backend == 'pyttsx3':
            import pyttsx3
            self.backend = pyttsx3.init()
        else:
            raise ValueError('目前只支持 pyttsx3')

    def getProperty(self, name):
        """获取当前引擎属性的值

        Args:
            name (str): 要查询的属性的名称。

            以下是可查询的属性名称：
             - "rate": 以每分钟字数为单位的整数语音速率。默认为200字/分钟。
             - "voice": 当前声音的字符串标识符。
             - "voices": 由 pyttsx3.voice.Voice 描述符对象组成的列表
             - "volume": 音量大小，在0.0到1.0范围内。默认为1.0。

        Returns:
            该属性的值
        """
        return self.backend.getProperty(name)

    def setProperty(self, name, value):
        """设置属性值

        Args:
            name (str): 要设置的属性的名称。
            value (any): 要设置的值。

            以下是可设置的属性名称：
             - "rate": 以每分钟字数为单位的整数语音速率。
             - "voice": 当前声音的字符串标识符。
             - "volume": 音量大小，在0.0到1.0范围内。
        Returns:
            None
        """
        return self.backend.setProperty(name, value)

    def say(self, text):
        """将要说的文本添到队列中。

        Args:
            text (str): 要说的文本。

        Returns:
            None
        """
        return self.backend.say(text)

    def runAndWait(self):
        """处理当前所有队列，在处理完之前会阻塞。当所有在此调用之前排队的命令都从队列中清空时返回。

        Returns:
            None
        """
        return self.backend.runAndWait()

    def save_to_file(self, text, filename):
        """将文本转语音并保存到文件

        保存文件时会将队列处理完。

        Args:
            text (str): 要转换的文本
            filename (str): 文件名，含后缀。如：test.mp3
        """
        self.backend.save_to_file(text, filename)
        self.backend.runAndWait()
