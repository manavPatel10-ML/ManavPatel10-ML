# groq_chatbot.py

from groq import Groq
from rich.console import Console
from rich.panel import Panel
from datetime import datetime

# ── Setup ─────────────────────────────────────────────────
API_KEY = "YOUR_API_KEY"   # 🔑 Replace with your new key
client = Groq(api_key=API_KEY)
console = Console()

# ── Available FREE Models on Groq ─────────────────────────
# ── Available FREE Models on Groq (UPDATED) ─────────────────────────
MODELS = {
    "1": ("llama-3.3-70b-versatile", "LLaMA 3.3 70B — Best Quality"),
    "2": ("llama-3.1-8b-instant", "LLaMA 3.1 8B — Fast & Cheap"),
    "3": ("openai/gpt-oss-20b", "GPT-OSS 20B — OpenAI OSS"),
}

# ── Model Selection ───────────────────────────────────────ss
def select_model() -> str:
    console.print(Panel(
        "\n".join([f"[cyan]{k}[/cyan]. {v[1]}" for k, v in MODELS.items()]),
        title="[bold]Select AI Model[/bold]",
        border_style="cyan"
    ))

    choice = console.input(
        "[bold]Enter choice (1-3) [default=1]: [/bold]"
    ).strip()

    model_id = MODELS.get(choice, MODELS["1"])[0]
    console.print(f"[green]✅ Using: {model_id}[/green]\n")

    return model_id

# ── Chat Function ─────────────────────────────────────────
def chat_with_groq(conversation_history: list, model: str) -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=conversation_history,
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ── Main Function ─────────────────────────────────────────
def main():
    console.print(Panel.fit(
        "[bold cyan]⚡ NOVA Ai Chatbot[/bold cyan]\n"
        "[dim]Ultra-fast LLaMA 3 powered by Groq (FREE)[/dim]\n"
        "[yellow]Commands: 'quit' | 'clear' | 'model' | 'history'[/yellow]",
        border_style="cyan"
    ))

    selected_model = select_model()

    # System Prompt (AI Personality)
    conversation_history = [
        {
            "role": "system",
            "content": (
                "You are an expert AI assistant. "
                "You help with coding, business, academics, "
                "data analysis, and general knowledge. "
                "Be concise, clear, and friendly."
            )
        }
    ]

    while True:
        try:
            user_input = console.input(
                "[bold green]You:[/bold green] "
            ).strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit"]:
                console.print("[cyan]👋 Goodbye![/cyan]")
                break

            if user_input.lower() == "clear":
                conversation_history = [conversation_history[0]]
                console.print(
                    "[yellow]✅ Conversation cleared![/yellow]\n"
                )
                continue

            if user_input.lower() == "model":
                selected_model = select_model()
                continue

            if user_input.lower() == "history":
                console.print(Panel(
                    "\n".join([
                        f"[{'green' if m['role']=='user' else 'magenta'}]"
                        f"{m['role'].upper()}:[/"
                        f"{'green' if m['role']=='user' else 'magenta'}] "
                        f"{m['content'][:80]}..."
                        for m in conversation_history[1:]
                    ]) or "No history yet.",
                    title="Chat History",
                    border_style="yellow"
                ))
                continue

            # Add user message
            conversation_history.append({
                "role": "user",
                "content": user_input
            })

            # Get response
            with console.status("[dim]⚡ Groq is thinking...[/dim]"):
                response = chat_with_groq(
                    conversation_history,
                    selected_model
                )

            # Save assistant response
            conversation_history.append({
                "role": "assistant",
                "content": response
            })

            timestamp = datetime.now().strftime("%H:%M")

            console.print(Panel(
                response,
                title=f"[bold magenta]🤖 AI [{timestamp}] | {selected_model}[/bold magenta]",
                border_style="magenta",
                padding=(1, 2)
            ))

            console.print()

        except KeyboardInterrupt:
            console.print("\n[yellow]Type 'quit' to exit.[/yellow]")

# ── Run Program ───────────────────────────────────────────
if __name__ == "__main__":
    main()
