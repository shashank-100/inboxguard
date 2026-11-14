# Results

Per-episode logs (every send/share the agent made, its final answer) are in `docs/runs/`.

| Model | Defense | Attack episodes | Utility benign | Utility under attack | Attack success |
|---|---|---|---|---|---|
| Claude Opus 5.5 | none | 24 (3 classic styles) | 1.00 | 1.00 | 0.00 |
| Claude Opus 5.5 | data_boundary | 24 (3 classic styles) | 1.00 | 1.00 | 0.00 |
| Claude Sonnet 5.5 | none | 48 (6 styles) | 1.00 | 1.00 | 0.00 |
| Claude Opus 5.5 | none | 48 (6 styles) | 1.00 | 1.00 | 0.00 |

Attack success was 0 for every goal (payroll exfiltration, 2FA theft, contact phishing) and every style, including
user impersonation and spoofed tool output. The Sonnet + data_boundary arm was not run: with 0% attack success and
100% utility already, a defense has nothing left to change.

What this means: for these two models the suite is saturated on security, so its use is (1) as a regression test for
agent stacks built on them (custom prompts, tools, or memory can reintroduce weaknesses), and (2) to measure models that
are not hardened. Next additions with the most signal: multi-step attacks that ask for a benign-looking action first,
attacks hidden in attachments and calendar invites, and open-weight models.
