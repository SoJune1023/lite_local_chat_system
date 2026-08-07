import asyncio
import httpx

from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

BASE_URL = "http://127.0.0.1:8000"
console = Console()

async def chat_loop() -> None:
    console.print("[bold cyan]ollama chat[/bold cyan]  [dim](/exit 로 종료)[/dim]\n")

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=120) as client:
        while True:
            user_input = Prompt.ask("[bold green]you[/bold green]")
            if user_input.strip().lower() in ("/exit", "/quit"):
                break
            if not user_input.strip():
                continue

            with console.status("[dim]생각 중...[/dim]", spinner="dots"):
                try:
                    res = await client.post(
                        "/interaction",
                        json={"message": user_input},
                    )
                    res.raise_for_status()
                except httpx.ConnectError:
                    console.print("[bold red]서버 연결 실패[/bold red] — python -m src 로 서버부터 켜둬")
                    break
                except httpx.HTTPStatusError as e:
                    console.print(f"[bold red]서버 에러[/bold red] {e.response.status_code}: {e.response.text}")
                    continue

            data = res.json()
            console.print("[bold magenta]ai[/bold magenta]")
            console.print(Markdown(data["message"]))
            console.print()

def main() -> None:
    try:
        asyncio.run(chat_loop())
    except KeyboardInterrupt:
        console.print("\n[dim]종료됨[/dim]")

if __name__ == "__main__":
    main()