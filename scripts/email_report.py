"""
Send email reports via Gmail SMTP.

Usage:
    python scripts/email_report.py "Subject line" "Body text (markdown ok)"
    cat report.md | python scripts/email_report.py "Subject line" -

Reads env vars:
    GMAIL_USER          (sender + recipient)
    GMAIL_APP_PASSWORD  (16-char app password)
    EMAIL_TO            (optional, defaults to GMAIL_USER)
"""

import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def _env(name: str, required: bool = True) -> str | None:
    value = os.environ.get(name)
    if not value and required:
        print(f"ERROR: missing env var {name}", file=sys.stderr)
        sys.exit(2)
    return value


def send(subject: str, body_md: str) -> None:
    sender = _env("GMAIL_USER")
    password = _env("GMAIL_APP_PASSWORD")
    recipient = _env("EMAIL_TO", required=False) or sender

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    html_body = _markdown_to_basic_html(body_md)
    msg.attach(MIMEText(body_md, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())

    print(f"Email sent to {recipient}: {subject}")


def _markdown_to_basic_html(md: str) -> str:
    """Minimal markdown -> HTML. Good enough for email reports."""
    lines = md.split("\n")
    html_lines = ["<html><body style='font-family: -apple-system, sans-serif; line-height: 1.5;'>"]
    in_code = False
    in_list = False

    for line in lines:
        if line.startswith("```"):
            if in_code:
                html_lines.append("</pre>")
                in_code = False
            else:
                html_lines.append("<pre style='background:#f4f4f4;padding:8px;border-radius:4px;'>")
                in_code = True
            continue
        if in_code:
            html_lines.append(_escape(line))
            continue

        if line.startswith("# "):
            html_lines.append(f"<h1>{_escape(line[2:])}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{_escape(line[3:])}</h2>")
        elif line.startswith("### "):
            html_lines.append(f"<h3>{_escape(line[4:])}</h3>")
        elif line.startswith("- ") or line.startswith("* "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{_inline(line[2:])}</li>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if line.strip():
                html_lines.append(f"<p>{_inline(line)}</p>")
            else:
                html_lines.append("<br>")

    if in_list:
        html_lines.append("</ul>")
    if in_code:
        html_lines.append("</pre>")
    html_lines.append("</body></html>")
    return "\n".join(html_lines)


def _escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _inline(s: str) -> str:
    s = _escape(s)
    # **bold**
    while "**" in s:
        s = s.replace("**", "<b>", 1)
        if "**" in s:
            s = s.replace("**", "</b>", 1)
        else:
            break
    return s


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)

    subject = sys.argv[1]
    body = sys.argv[2]
    if body == "-":
        body = sys.stdin.read()

    send(subject, body)


if __name__ == "__main__":
    main()
