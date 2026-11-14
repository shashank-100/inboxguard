"""A small simulated workspace (inbox + files) and the agent's tools, operating on one JSON state file.

Every side effect (sent emails, shared files) is appended to the state, so utility and security are checked from the
final state, AgentDojo-style. CLI:  python -m inboxguard.env <state.json> <command> [args]
  search <query>            list matching emails (id, from, subject, date)
  read <email_id>           full email
  files                     list files
  open <name>               file contents
  send <to> <subject> <body>
  share <name> <to>
"""
import json
import sys


def load(path):
    with open(path) as f:
        return json.load(f)


def save(path, st):
    with open(path, "w") as f:
        json.dump(st, f, indent=1)


def run(path, cmd, args):
    st = load(path)
    if cmd == "search":
        q = " ".join(args).lower()
        hits = [e for e in st["emails"] if not q or q in (e["subject"] + " " + e["body"] + " " + e["from"]).lower()]
        return [{"id": e["id"], "from": e["from"], "subject": e["subject"], "date": e["date"]} for e in hits]
    if cmd == "read":
        e = next((e for e in st["emails"] if str(e["id"]) == args[0]), None)
        return e or {"error": f"no email {args[0]}"}
    if cmd == "files":
        return [f["name"] for f in st["files"]]
    if cmd == "open":
        f = next((f for f in st["files"] if f["name"] == args[0]), None)
        return f or {"error": f"no file {args[0]}"}
    if cmd == "send":
        to, subject, body = args[0], args[1], " ".join(args[2:])
        st["sent"].append({"to": to.lower(), "subject": subject, "body": body})
        save(path, st)
        return {"ok": True}
    if cmd == "share":
        st["shared"].append({"file": args[0], "to": args[1].lower()})
        save(path, st)
        return {"ok": True}
    return {"error": f"unknown command {cmd}"}


if __name__ == "__main__":
    print(json.dumps(run(sys.argv[1], sys.argv[2], sys.argv[3:]), indent=1))
