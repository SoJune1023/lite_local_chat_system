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
        console.print("[bold cyan]ollama chat[/bold cyan]  [dim](/exit to quit)[/dim]\n")

        async with httpx.AsyncClient(base_url=BASE_URL, timeout=httpx.Timeout(600)) as client:
            while True:
                user_input = Prompt.ask("[bold green]you[/bold green]")
                
                if user_input.strip().lower() in ("/exit", "/quit"):
                    break

                if user_input.strip().lower() in ("/ollama"):
                    console.print(f"[bold green]Changing model : {self._model} -> ollama[/bold green]")
                    self._model = "ollama"
                    console.print(f"[bold green]Model changed![/bold green]")
                elif user_input.strip().lower() in ("/claude"):
                    console.print(f"[bold green]Changing model : {self._model} -> claude[/bold green]")
                    console.print(f"[bold green]Model changed![/bold green]")
                
                if not user_input.strip():
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
