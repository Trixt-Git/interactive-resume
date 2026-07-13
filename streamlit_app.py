from pathlib import Path

app_path = Path(__file__).with_name("app.py")
exec(compile(app_path.read_text(encoding="utf-8"), str(app_path), "exec"))
