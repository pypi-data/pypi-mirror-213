import requests
import questionary
from rich.live import Live
from rich.markdown import Markdown
from argparse import ArgumentParser

from .copilot import Copilot
from .cmd import run_commands
from .term import terminal_chat

parser = ArgumentParser()
parser.add_argument("-m", "--mode", help="Set the mode. (terminal / full / quick / run)", dest="mode", default=None)
parser.add_argument("-a", "--ask", help="Quickly ask Copilot.", dest="content", default=None)
args = parser.parse_args()

if not args.mode:
  ans = questionary.select(
    "Select mode",
    choices=[
      "terminal chat",
      "full screen",
      "quick ask",
      "run commands"
    ],
    instruction="(Use arrow keys or k-up and j-down keys.)"
  ).ask()
else:
  table = {
    "terminal": "terminal chat",
    "full": "full screen",
    "quick": "quick ask",
    "run": "run commands"
  }
  try:
    ans = table[args.mode]
  except KeyError:
    available = "\n".join([
      f"- {k}: {v}" for k, v in table.items()
    ])
    print(f"Invalid mode.\n\nAvailable ones:\n{available}")
    exit(2)


# match syntax (python 3.10+)
match ans:
  case 'full screen':
    Copilot().run()

  case 'terminal chat':
    terminal_chat(args.content)

  case "quick ask":
    if args.content:
      print("Ask: " + args.content)
      prompt = args.content
    else:
      prompt = input("Ask: ")
    print("✨ Response:")
    res = requests.post("https://chatgpt.awdev.repl.co/copilot", json={
      "prompt": "You will now act like Copilot, a large language model trained by OpenAI.\nI will ask you some questions, and you'll answer as concisely as possible.\nMy first request is: " + prompt
    }, stream=True)

    fetched = ""
    def generate(cursor: bool = True):
      return Markdown(fetched + ("█" if cursor else ""), code_theme="one-dark")

    with Live(generate(), refresh_per_second=4) as live:
      for chunk in res.iter_content():
        fetched += chunk.decode('utf-8')
        live.update(generate())

      live.update(generate(False))
      
  case 'run commands':
    run_commands(args.content)

PLACEHOLDER = "I love placeholders! :)"

def placeholder():
  pass