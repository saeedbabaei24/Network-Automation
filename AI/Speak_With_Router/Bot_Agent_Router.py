import os
import json
import re
from netmiko import ConnectHandler

from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


# -----------------------
# ENV / Config
# -----------------------
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

ROUTER_NAME = os.environ.get("ROUTER_NAME", "R1")
ROUTER = {
    "device_type": "cisco_ios",   
    "host": "192.168.199.30",
    "username": "admin",          
    "password": "cisco"    
}



ALLOWED_PATTERNS = [
    r"^show ip interface brief",
    r"^show interface",
    r"^show ip route",
    r"^show running-config \| include",
    r"^show running-config \| section",
    r"^show aaa",
    r"^show tacacs",
    r"^show logging",
    r"^ping ",
    r"^traceroute "
]



def run_cli(command: str) -> str:
    cmd = command.strip()

    # forbiden
    FORBIDDEN = ["conf", "configure", "reload", "write", "copy", "clear", "debug"]
    if any(word in cmd.lower() for word in FORBIDDEN):
        return "ERROR: Configuration or disruptive commands are forbidden."

    # these are alowed
    if not (SHOW_ONLY.match(cmd) or PING_OK.match(cmd) or TRACE_OK.match(cmd)):
        return "ERROR: Only 'show', 'ping', and 'traceroute' are allowed."

    # Prevent show run
    if cmd.lower() == "show running-config":
        return "ERROR: Full running-config is not allowed. Use filtered commands like '| include' or '| section'."

    try:
        conn = ConnectHandler(**ROUTER)
        out = conn.send_command(cmd, read_timeout=30)
        conn.disconnect()
    except Exception as e:
        return f"ERROR: CLI execution failed: {e}"

    
    if "% Invalid input" in out or "% Incomplete command" in out:
        return "ERROR: Invalid Cisco IOS command."

    return out



SHOW_ONLY = re.compile(r"^\s*show\s+", re.IGNORECASE)
PING_OK   = re.compile(r"^\s*ping(\s+|$)", re.IGNORECASE)
TRACE_OK  = re.compile(r"^\s*traceroute(\s+|$)", re.IGNORECASE)

MAX_TOOL_CALLS_PER_QUESTION = 3 # MVP
MAX_ROUNDS = 4                  # go and back to AI

client = OpenAI(api_key=OPENAI_API_KEY)


def run_show(command: str) -> str:
    """Run a single SHOW command on the router and return output."""
    if not SHOW_ONLY.match(command):
        return "ERROR: Only 'show' commands are allowed."

    if not ROUTER["host"] or not ROUTER["username"]:
        return "ERROR: Router connection env vars are not set (ROUTER_HOST/USER/PASS)."

    conn = ConnectHandler(**ROUTER)
    try:
        out = conn.send_command(command, read_timeout=30)
    finally:
        conn.disconnect()
    return out


FUNCTIONS = [
    {
        "name": "run_show",
        "description": f"Run a read-only Cisco IOS SHOW command on device {ROUTER_NAME}",
        "parameters": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"]
        }
    },
    {
        "name": "run_ping",
        "description": f"Run a ping command on device {ROUTER_NAME} to test reachability.",
        "parameters": {
            "type": "object",
            "properties": {"command": {"type": "string", "description": "A Cisco IOS ping command, e.g. ping 8.8.8.8"}},
            "required": ["command"]
        }
    },
    {
        "name": "run_traceroute",
        "description": f"Run a traceroute command on device {ROUTER_NAME}.",
        "parameters": {
            "type": "object",
            "properties": {"command": {"type": "string", "description": "A Cisco IOS traceroute command"}},
            "required": ["command"]
        }
    }
]

SYSTEM_INSTRUCTIONS = f"""
You are a senior network troubleshooting assistant for Cisco IOS.

You must NOT ask the user what command to run.
You must decide and run the minimum commands yourself.

Allowed actions ONLY via tool calls:
- run_show(command)   -> command must start with 'show'
- run_ping(command)   -> command must start with 'ping'
- run_traceroute(command) -> command must start with 'traceroute'

Strict rules:
- NEVER request config mode commands (conf t, configure terminal, write, reload, clear, debug, copy, etc.).
- Use at most 3 tool calls per user question.
- Prefer filtered/short outputs (include/section/| last) instead of huge outputs.
- If the question cannot be answered reliably with allowed commands, state that clearly and propose the best next command(s) you would run.

When you have enough information, STOP calling tools and provide a final answer with:
1) Findings (facts from outputs)
2) Conclusion (yes/no + evidence)
3) Recommendations (improvements)


Device OS: Cisco IOS classic CLI.
Valid examples:
- show running-config | include tacacs
- show running-config | section aaa
- show ip route
- show interface GigabitEthernet0/1
- show logging | include TACACS


"""



def agent_answer(question: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTIONS},
        {"role": "user", "content": question},
    ]

    tool_calls_used = 0

    for _ in range(MAX_ROUNDS):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            functions=FUNCTIONS,
            function_call="auto",
        )

        msg = response.choices[0].message

        # Tool requested?
        if msg.function_call:
            tool_calls_used += 1
            if tool_calls_used > MAX_TOOL_CALLS_PER_QUESTION:
                return "I hit the max diagnostic steps for one question. Please ask more specifically (interface/protocol/target)."

            fn = msg.function_call.name
            args = json.loads(msg.function_call.arguments or "{}")
            cmd = (args.get("command") or "").strip()

            # real run
            result = run_cli(cmd)

            # append assistant tool call message
            messages.append(msg)

            # append function output
            messages.append({
                "role": "function",
                "name": fn,
                "content": f"COMMAND: {cmd}\n\nOUTPUT:\n{result}"
            })
            continue

        # Final answer
        return (msg.content or "").strip() or "(No answer text returned.)"

    return "I couldn't complete within allowed steps. Please ask a narrower question."

# -----------------------
# Telegram handlers
# -----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Ready \n"
        f"Device: {ROUTER_NAME}\n"
        f"Ask any question. I will run SHOW commands and analyze.\n\n"
        f"Examples:\n"
        f"- Why is Gi0/1 down?\n"
        f"- Is BGP healthy?\n"
        f"- Any routing issues?\n"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = (update.message.text or "").strip()
    if not q:
        return

    await update.message.reply_text("Checking the router and analyzing...")

    try:
        answer = agent_answer(q)
    except Exception as e:
        answer = f"Error: {e}"

    #limit of telegram massage
    if len(answer) > 3800:
        answer = answer[:3800] + "\n\n(Trimmed. Ask a more specific question.)"

    await update.message.reply_text(answer)


def main():
    if not TELEGRAM_BOT_TOKEN:
        raise SystemExit("Set TELEGRAM_BOT_TOKEN env var.")
    if not OPENAI_API_KEY:
        raise SystemExit("Set OPENAI_API_KEY env var.")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Telegram Router Agent running...")
    app.run_polling()


if __name__ == "__main__":
    main()