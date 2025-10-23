import json
from pathlib import Path
from main import app


def export_openapi():
    openapi_schema = app.openapi()
    path = Path("openapi.json")
    path.write_text(json.dumps(openapi_schema, indent=2, ensure_ascii=False))
    print(f"✅ OpenAPI schema saved to {path.resolve()}")


if __name__ == "__main__":
    export_openapi()
