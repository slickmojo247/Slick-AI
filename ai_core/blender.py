class ResponseBlender:
    def __init__(self):
        self.weights = {
            'openai': 0.7,
            'deepseek': 0.3
        }

    def blend(self, openai_resp, deepseek_resp):
        blended = {
            'content': openai_resp['content'],
            'supporting_data': deepseek_resp['content']
        }
        return blended
