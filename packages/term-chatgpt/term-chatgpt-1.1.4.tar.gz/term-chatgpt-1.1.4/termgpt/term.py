import requests

from rich.live import Live
from rich.console import Console
from rich.markdown import Markdown

def terminal_chat(quickr = None):
  msgs = []
  console = Console()
  console.print("[gray0](hint: type 'quit' to quit)[/gray0]\n")
  auto_fill = quickr

  while True:
    if auto_fill:
      prompt = auto_fill
      console.print("🤔 [gray0]" + prompt + "[/gray0]")
    else:
      prompt = input("🤔 ")

    if prompt.lower() in ['quit', 'exit']:
      break
    msgs.append({ "role": "user", "content": prompt })

    fetched = ""
    def gen_markdown(cursor: bool = True):
      return Markdown(fetched.replace("ChatGPT", "Copilot").replace("Copilot: ", "", 1).replace("You: ", "", 1).replace("The chat starts now.", "", 1) + ("█" if cursor else ""), code_theme="one-dark")

    print("\n✨ Copilot")
    with Live(gen_markdown(), refresh_per_second=4) as live:
      for chunk in requests.post("https://chatgpt.awdev.repl.co/completions", json={
        "messages": msgs
      }, stream=True).iter_content():
        fetched += chunk.decode('utf-8')
        live.update(gen_markdown())

      live.update(gen_markdown(False))

    print()
    msgs.append({ "role": "assistant", "content": fetched })
    auto_fill = None
