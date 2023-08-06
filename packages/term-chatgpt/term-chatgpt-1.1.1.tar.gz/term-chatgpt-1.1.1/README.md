# term-gpt
Ask ChatGPT directly on your terminal! Fast & No OpenAI API key required!

## Quick Start
```bash
$ term-gpt
```
```
? Select mode (Use arrow keys or k-up and j-down keys.)
   terminal chat
   full screen
 » quick ask
   run commands

Ask: Who are you?
✨ Response:
I am Copilot, a large language model developed by OpenAI that can assist in generating human-like text based on the given prompt.
```

## Modes
`term-gpt` has four different modes, including:
- `termainl`: Terminal chat. (continuous)
- `full`: Full screen mode.
- `quick`: "Quick ask" mode. (one-time)
- `run`: Run & ask ChatGPT about shell commands.

Additionally, you can specify the modes by using the `-m` argument. For instance: `term-gpt -m terminal`. Or, if you want to assign the question, use the `-a` argument. For instance: `term-gpt -a "Hello!"`.

### terminal
Terminal chat.

```bash
$ term-gpt -m terminal
```
```
(hint: type 'quit' to quit)

🤔 Who are you?

✨ Copilot
Hello! I am Copilot, a large language model trained by OpenAI. How may I  
assist you today?
```

### full
Full screen mode.

![Full Screen Preview](https://i.imgur.com/EjYcT0p.png)

### quick
Quick mode.

```bash
$ term-gpt -m quick
```
```
Ask: Hello!
✨ Response:
Hi there!
```

### run
Run & ask ChatGPT about shell commands. (Based on your platform)

```bash
$ term-gpt -m run
```
```
(hint: type 'quit' to quit)

🔎 I want to see all the files in this dir
... Working

✨ Copilot
ls

? Select an action (Use arrow keys or k-up and j-down keys.)
 » ✅ Execute
   ✨ Explain
   🤔 Revise
   🔁 Retry
   ❌ Cancel
```

