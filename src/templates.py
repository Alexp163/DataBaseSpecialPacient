from pathlib import Path

from fastapi import Request
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def render_template(request: Request, name: str, **kwargs):
    return templates.TemplateResponse(request=request, name=name, context=kwargs)
