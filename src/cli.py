import asyncio
import httpx

from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from typing import Literal

BASE_URL = "http://127.0.0.1:8000"
console = Console()

class Client:
    _model: Literal['ollama', 'claude']

    def __init__(self):
        self._model = 'claude'

    async def chat_loop(self) -> None:
        console.print("[bold cyan]lite local chat system[/bold cyan]  [dim](/exit to quit)[/dim]\n")

        async with httpx.AsyncClient(base_url=BASE_URL, timeout=httpx.Timeout(600)) as client:
            while True:
                user_input = Prompt.ask("[bold green]you[/bold green]")
                cmd = user_input.strip().lower()

                if cmd in ("/exit", "/quit"):
                    break

                if cmd in ("/ollama", "/claude"):
                    new_model = cmd[1:]
                    console.print(f"[bold green]Changing model : {self._model} -> {new_model}[/bold green]")
                    self._model = new_model
                    console.print(f"[bold green]Model changed![/bold green]")
                    continue

                if not cmd:
                    continue

                with console.status("[dim]Thinking...[/dim]", spinner="dots"):
                    try:
                        res = await client.post(
                            "/interaction",
                            json={
                                "message": user_input,
                                "model": self._model
                            },
                        )
                        res.raise_for_status()
                    except httpx.ConnectError:
                        console.print("[bold red]Failed to connect server[/bold red]")
                        break
                    except httpx.HTTPStatusError as e:
                        console.print(f"[bold red]Server Error[/bold red] {e.response.status_code}: {e.response.text}")
                        continue

                data = res.json()
                console.print("[bold magenta]ai[/bold magenta]")
                console.print(Markdown(data["message"]))
                console.print()

def main() -> None:
    try:
        instance = Client()
        asyncio.run(instance.chat_loop())
    except KeyboardInterrupt:
        console.print("\n[dim]End[/dim]")

if __name__ == "__main__":
    main()
