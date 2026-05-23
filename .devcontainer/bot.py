import os, sys, subprocess, time, json, requests, uuid

token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")
if not token or not chat_id:
    print("FATAL: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set as Codespace secrets.")
    sys.exit(1)

PORT = 443
RETRY_LIMIT = 3
RETRY_DELAY = 5

def send(msg):
    for i in range(RETRY_LIMIT):
        try:
            r = requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": msg},
                timeout=10
            )
            if r.status_code == 200:
                return
        except:
            pass
        time.sleep(RETRY_DELAY)

send("Starting setup...")

send("Generating config...")
uid = str(uuid.uuid4())
cfg = {
    "inbounds": [{
        "port": PORT,
        "protocol": "vless",
        "settings": {"clients": [{"id": uid}], "decryption": "none"},
        "streamSettings": {"network": "xhttp", "xhttpSettings": {"mode": "packet-up", "path": "/"}}
    }],
    "outbounds": [{"protocol": "freedom"}]
}
with open("/etc/config.json", "w") as f:
    json.dump(cfg, f)

send("Config saved.")

send("Making port public...")
codespace = os.environ.get("CODESPACE_NAME")
subprocess.run(f"gh codespace ports visibility {PORT}:public -c {codespace}", shell=True, check=True)

send(f"Port {PORT} is now public.")

send("Starting Xray...")
proc = subprocess.Popen(
    ["/usr/local/bin/xray", "-c", "/etc/config.json"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

time.sleep(2)
if proc.poll() is not None:
    out, err = proc.communicate()
    send(f"Xray failed to start.\nSTDOUT:\n{out.decode()}\nSTDERR:\n{err.decode()}")
    sys.exit(1)

send("Xray is running.")

send(f"VLESS LINK:\nvless://{uid}@{codespace}-{PORT}.app.github.dev:443?encryption=none&security=tls&type=xhttp&mode=packet-up&sni={codespace}-{PORT}.app.github.dev&path=%2F#ghtun")

send("All done. Tunnel is ready.")
