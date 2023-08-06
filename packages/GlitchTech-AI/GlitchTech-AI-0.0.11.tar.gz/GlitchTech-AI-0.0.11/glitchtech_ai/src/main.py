from dotenv import dotenv_values
from glitchtech_ai.tools import OpenAi


def cli():
    env_vars = dotenv_values()
    token = env_vars['API_KEY']

    oa = OpenAi(prompt="You are a tired butler.", token=token)
    while True:
        command = input("[ OA ]-> ")
        if command.lower() in ['quit', 'q', 'exit', 'e']:
            print(oa.session_usage)
            break
        elif command:
            print(oa.chat_completions(user_input=command))


if __name__ == '__main__':
    cli()
