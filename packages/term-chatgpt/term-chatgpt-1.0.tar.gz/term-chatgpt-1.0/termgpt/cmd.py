import os

import requests
import platform

import questionary
from rich.live import Live
from rich.console import Console
from rich.markdown import Markdown

def ask(console: Console, prompt, in_block = True):
  console.print("[gray0]... Working[/gray0]")
  res = requests.post("https://chatgpt.awdev.repl.co/copilot", json={
    "prompt": prompt
  }, stream=True)

  print("\n✨ Copilot", flush=True)
  fetched = ""
  def generate(cursor: bool = True):
    if in_block:
      return Markdown("```sh\n" + fetched + ("█" if cursor else "") + "\n```", code_theme="one-dark")
    else:
      return Markdown(fetched + ("█" if cursor else ""), code_theme="one-dark")

  with Live(generate(), refresh_per_second=4) as live:
    for chunk in res.iter_content():
      fetched += chunk.decode('utf-8')
      live.update(generate())

    live.update(generate(False))

  return fetched

def run_commands(quickr: str = None):
  console = Console()
  auto_ask = quickr

  console.print("[gray0](hint: type 'quit' to quit)[/gray0]\n")
  while True:
    if not auto_ask:
      prompt = input("🔎 I want to ")
    else:
      prompt = auto_ask

    if prompt.lower() in ['quit', 'exit']:
      break

    fetched = ask(console, f"I want you to act like a command generator. You will provide me a command that fits my needs.\nMy platform is: {platform.platform()}, and my first request is that I want to" + prompt + "\nONLY GIVE THE THE COMMAND, DON'T EXPLAIN OR REPLY ANYTHING THAT'S NOT A COMMAND. Additionally, don't put the command in a codeblock!")
    auto_ask = None

    print()

    choices = [
      (execute := "✅ Execute"),
      (explain := "✨ Explain"),
      (revise := "🤔 Revise"),
      (retry := "🔁 Retry"),
      (cancel := "❌ Cancel")
    ]
    while True:
      ans = questionary.select(
        "Select an action",
        choices=choices,
        instruction="(Use arrow keys or k-up and j-down keys.)"
      ).ask()

      if ans == execute:
        print()
        output = os.system(fetched.strip('`'))
        console.print("[green]Success![/green]" if output == 0 else "[red]Failed[/red]")
        print()
        break
        
      if ans == explain:
        choices.remove(explain)
        # ask the bot
        ask(console, f"Can you explain what this command mean and is it safe to run: {fetched}", in_block=False)
        print()

      if ans == revise:
        print()
        fetched = questionary.text("🔁 Revise", default=fetched).ask()
        print(f"\nModified to {fetched}\n")

      if ans == retry:
        auto_ask = prompt
        break

      if ans == cancel:
        break
