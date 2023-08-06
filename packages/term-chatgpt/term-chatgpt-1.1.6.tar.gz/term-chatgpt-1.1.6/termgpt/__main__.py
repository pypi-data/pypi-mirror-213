def main():
  try:
    from .main import main as runner
    runner()
  except (ImportError, SyntaxError):
    from rich.console import Console
    from rich.markdown import Markdown
    Console().print(Markdown('Are you using the python command? Try `python3 `*`-m`*` term-gpt` instead!'))

if __name__ == "__main__":
  main()