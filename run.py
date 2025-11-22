from pathlib import Path
import sqlite3
import click
from app import create_app

BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_FILE = DATABASE_DIR / "wallet.db"
SCHEMA_FILE = DATABASE_DIR / "schema.sql"
SEED_FILE = DATABASE_DIR / "seed_data.sql"

def _ensure_database_dir():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

def _get_connection():
    _ensure_database_dir()
    conn = sqlite3.connect(str(DATABASE_FILE), detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(schema_path: Path = SCHEMA_FILE):
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    conn = _get_connection()
    with schema_path.open("r", encoding="utf-8") as f:
        sql = f.read()
    with conn:
        conn.executescript(sql)
    conn.close()
    return True

def seed_db(seed_path: Path = SEED_FILE):
    if not seed_path.exists():
        return False
    conn = _get_connection()
    with seed_path.open("r", encoding="utf-8") as f:
        sql = f.read()
    with conn:
        conn.executescript(sql)
    conn.close()
    return True

@click.group()
def cli():
    pass

@cli.command("init-db")
@click.option("--schema", default=str(SCHEMA_FILE), help="Path to SQL schema file")
def cli_init_db(schema):
    try:
        init_db(Path(schema))
        click.echo(f"Initialized database at {DATABASE_FILE}")
    except Exception as e:
        click.echo(f"Failed to initialize DB: {e}", err=True)

@cli.command("seed-db")
@click.option("--seed", default=str(SEED_FILE), help="Path to SQL seed file")
def cli_seed_db(seed):
    try:
        ok = seed_db(Path(seed))
        if ok:
            click.echo("Seeded database successfully")
        else:
            click.echo("No seed file found; nothing to do")
    except Exception as e:
        click.echo(f"Failed to seed DB: {e}", err=True)

@cli.command("run")
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=5000, help="Port to listen on", type=int)
@click.option("--debug/--no-debug", default=True, help="Run in debug mode")
def cli_run(host, port, debug):
    app = create_app()
    app.run(host=host, port=port, debug=debug, use_reloader=debug)

if __name__ == "__main__":
    cli()
