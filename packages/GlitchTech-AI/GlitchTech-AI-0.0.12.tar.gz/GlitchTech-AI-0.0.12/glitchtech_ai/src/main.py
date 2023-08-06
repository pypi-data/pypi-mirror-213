import os

from glitchtech_ai.tools import OpenAi


def cli():
    try:
        open_ai_token = os.environ['OPEN_AI_TOKEN']

        oa = OpenAi(prompt="You are a tired butler.", token=open_ai_token)
        while True:
            command = input("[ OA ]-> ")
            if command.lower() in ['quit', 'q', 'exit', 'e']:
                print(oa.session_usage)
                break
            elif command:
                print(oa.chat_completions(user_input=command))
    except KeyError:
        print("Please set environment variable 'OPEN_AI_TOKEN' and retry.")


if __name__ == '__main__':
    cli()
