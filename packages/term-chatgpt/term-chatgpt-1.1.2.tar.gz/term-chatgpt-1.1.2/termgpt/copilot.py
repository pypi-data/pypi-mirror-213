from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header, TabbedContent, TabPane, Static, Label, Input, Button
from textual.suggester import SuggestFromList
from textual.validation import Function
from textual.containers import ScrollableContainer

import subprocess
import time
import httpx
import pyperclip

from rich.markdown import Markdown as RichMarkdown

StopButton = Button("◼ Stop", id="stop")
CopyButton = Button("📄 Copy", id="copy")
ShellInput = Input(
  placeholder="Press enter to run command...",
  id="shell-input"
)
ShellInputAsk = Input(
  placeholder="Ask AI and run...",
  id="shell-ask"
)

class Markdown(Static):
  def __init__(self, text: str, *args, **kwargs):
    self._text = text
    super().__init__(*args, **kwargs)

  def on_mount(self) -> None:
    self.update(self._text)

  def update(self, text):
    super().update(RichMarkdown(text, code_theme="one-dark"))

class Notification(Static):
  def on_mount(self) -> None:
      self.set_timer(3, self.remove)

  def on_click(self) -> None:
      self.remove()

class Shell(Static):
  _result = []

  def compose(self) -> None:
    s = ScrollableContainer(id="conta")
    s.mount(Markdown("**History**"))
    yield s
    with TabbedContent(initial="run"):
      with TabPane("Run", id="run"):
        yield ShellInput

      with TabPane("Ask & Run", id="ask"):
        yield ShellInputAsk


  @on(Input.Submitted)
  def input_submit(self, event: Input.Submitted):
    if event.input.id == "shell-input":
      cmd = event.value
      try:
        output = subprocess.Popen(event.value.split(' '), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).communicate()[0]
        self._result = [Label(">>> " + cmd, classes="shell-input-label"), Markdown(f"```\n{(output or b'(No output)').decode('utf-8')}\n```")]
      except Exception as err:
        self._result = [Label(">>> " + cmd), Markdown(f"```\nERROR: {err}\n```")]

      self.query_one('#conta').mount(
        *self._result
      )

class Copilot(App):
  BINDINGS = [
    Binding('escape', 'quit', 'Quit')
  ]
    
  CSS = """
  #chat-input {
    margin-top: 1
  }
  
  #stop {
    background: $error 30%;
    border: none;
    margin-left: 1;
    margin-top: 1;
    display: none;
  }
  .visible {
    display: block !important;
  }
  #input-err {
    margin-left: 1;
  }
  #markdown {
    margin-top: 2;
  }
  #copy {
    margin-top: 1;
    padding: 0 !important;
    background: #0995ec 30%;
    border: none !important;
    display: none;
  }
  Notification {
    dock: bottom;
    layer: notification;
    width: auto;
    margin: 2 4;
    padding: 1 2;
    background: $background;
    color: $text;
    height: auto;
  }
  #shell-input, #shell-ask {
    margin-top: 1;
    border: tall transparent;
    border-bottom: tall #0995ec;
  }
  #conta {
    margin-top: 1;
    min-height: 13;
  }
  .shell-input-label {
    margin-top: 1;
  }
  """

  _SHOULD_STOP = True
  _fetched = ""
  _ask_history = ["Write a Python code that", "Explain why", "Why is", "Why does my code", "How does Python", "How can I", "Make a request to", "How can I download"]

  def compose(self) -> ComposeResult:
    yield Footer()
    yield Header(True, name="copilot")
    with TabbedContent(initial="ask"):
      with TabPane("Ask", id="ask"):  # First tab
        yield Label("🔒 Ask ChatGPT anything, free and secure.")
        yield Input(
          placeholder="Press enter to send...", 
          id="chat-input",
          validators=[
            Function(lambda val: not not val, "Value is not given.")
          ],
          value="",
          suggester=SuggestFromList(self._ask_history, case_sensitive=False)
        )
        yield Label("", id="input-err")
        yield StopButton
        yield Markdown("*Response will appear here!*", id="markdown")
        yield CopyButton
        
  @on(Input.Changed)
  def show_invalid_reasons(self, event: Input.Changed) -> None:
      if event.input.id != "chat-input":
        return

      if not event.validation_result.is_valid:  
          self.query_one("#input-err").update(", ".join(event.validation_result.failure_descriptions))
      else:
          self.query_one("#input-err").update("")

  @on(Input.Submitted)
  def on_chat_input_submit(self, event: Input.Submitted) -> None:
    if event.input.id != "chat-input":
      return
    if self._SHOULD_STOP:
      self._SHOULD_STOP = False
      self._fetched = ""
      self._ask_history.append(event.value)
      self.query_one('#markdown').update('Working...')
      self.run_worker(self._do_work(event))

  async def _do_work(self, event: Input.Submitted):
    value = event.value
  
    self._fetched = ""
    self.query_one('#stop').set_classes("visible")
    self.query_one('#copy').set_classes("") # no copying until done
    
    async with httpx.AsyncClient() as client:
      async with client.stream("POST", "https://chatgpt.awdev.repl.co/copilot", json={
        "prompt": value
      }) as response:
        async for chunk in response.aiter_bytes():
          if self._SHOULD_STOP:
            break
          self._fetched += chunk.decode('utf-8')

          self.query_one("#markdown").update(self._fetched + "█")

    self.query_one('#stop').set_classes("")
    self.query_one('#copy').set_classes("visible")
    self.query_one('#markdown').update(self._fetched)
    self._SHOULD_STOP = True

  @on(StopButton.Pressed)
  def stop_btn_pressed(self, event: Button.Pressed):
    if event.button.id != "stop":
      return
    event.button.set_classes("")
    self.query_one('#copy').set_classes("visible")
    self._SHOULD_STOP = True

  @on(CopyButton.Pressed)
  def copy_btn_pressed(self, event: Button.Pressed):
    if event.button.id != "copy":
      return
  
    try:
      pyperclip.copy(self._fetched)
    except Exception as err:
      file = f"{time.time():.0f}.txt"
      with open(file, "x") as f:
        f.write(self._fetched)

      self.screen.mount(Notification(f"Error: couldn't find copy / paste method\nSaved as {file}."))
