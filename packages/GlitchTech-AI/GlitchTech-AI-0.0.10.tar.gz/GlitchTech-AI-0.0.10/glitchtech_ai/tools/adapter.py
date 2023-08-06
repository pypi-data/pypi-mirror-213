import requests


class OpenAi:
    def __init__(self, prompt: str, token: str):
        self.prompt = prompt

        self.host = "https://api.openai.com"
        self.headers = {
            "Authorization": f"Bearer {token}"
        }

        self.session_usage = {}

    def chat_completions(self, user_input, temperature: float = 0.7):
        url = f"{self.host}/v1/chat/completions"
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": self.prompt
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            "temperature": temperature
        }

        r = requests.post(url, headers=self.headers, json=data)

        if r.json().get('error'):
            return r.json().get('error')

        if r.json().get('usage'):
            self.session_usage = self._add_dicts(r.json().get('usage'), self.session_usage)

        return self._get_content(ai_resp=r.json())

    @staticmethod
    def _add_dicts(dict1, dict2):
        result = {}
        for key in dict1.keys() | dict2.keys():
            result[key] = dict1.get(key, 0) + dict2.get(key, 0)
        return result

    @staticmethod
    def _get_content(ai_resp: dict):
        if ai_resp.get('choices'):
            messages = [choice['message'].get('content') for choice in ai_resp.get('choices') if choice.get('message')]
            return "\n".join(messages)


if __name__ == '__main__':
    oa = OpenAi(prompt="Pretend you really enjoy chips and can't stop talking about them.", token="PRIVATE")
    print(
        oa.chat_completions(user_input="What do you call yourself?"),
        oa.session_usage,
        sep='\n'
    )
