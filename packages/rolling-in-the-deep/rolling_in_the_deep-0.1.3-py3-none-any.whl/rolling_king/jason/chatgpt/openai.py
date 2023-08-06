import openai
import json
from rolling_king.zijie.requests.http_sender_module import HttpSender

key_seg_1: str = "sk"
key_seg_2: str = "-"
key_seg_3: str = "wPe4VZsysqVYpOt4nIByT3BlbkFJf1Rx0O9HXr9znv5lzBG4"
openai.api_key = key_seg_1+key_seg_2+key_seg_3


class OpenAi(object):

    def __init__(self):
        self.http_sender = HttpSender("https://api.openai.com")
        self.http_sender.headers = {"Authorization": "Bearer "+openai.api_key}

    def get_models(self) -> dict:
        self.http_sender.send_get_request_by_suburi(sub_uri="/v1/models", input_params=None)
        return json.loads(self.http_sender.get_response.text)

    def get_specific_model(self, model: str = "gpt-3.5-turbo-0301") -> dict:
        self.http_sender.send_get_request_by_suburi(sub_uri="/v1/models/"+model, input_params=None)
        return json.loads(self.http_sender.get_response.text)

    def chat_with_gpt(self, question: str, model="gpt-3.5-turbo-0301") -> list:
        query_dict: dict = {
            "model": model,
            "messages": [{"role": "user", "content": question}]
        }
        self.http_sender.send_json_post_request_by_suburi(sub_uri="/v1/chat/completions",
                                                          json_data=query_dict)
        result_dict: dict = self.http_sender.post_response.json()
        choice_list: list = result_dict['choices']
        result_list = []
        for choice in choice_list:
            result_list.append(choice['message']['content'])
        return result_list


if __name__ == "__main__":
    chatgpt: OpenAi = OpenAi()
    # print(chatgpt.get_models())
    # print(chatgpt.get_specific_model(model="gpt-3.5-turbo-0613"))
    # print(chatgpt.chat_with_gpt(question="请介绍一下字节跳动", model="gpt-3.5-turbo-0613"))
    # print(chatgpt.chat_with_gpt(question="请介绍一下字节跳动", model="gpt-3.5-turbo"))








