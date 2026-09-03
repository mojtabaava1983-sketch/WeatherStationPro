import sqlite3
from backup import BackupService

def make_db(path):
    with sqlite3.connect(path) as conn:
        conn.execute("CREATE TABLE sample(id INTEGER PRIMARY KEY, value TEXT)")
        conn.execute("INSERT INTO sample(value) VALUES('ok')")
        conn.commit()

def test_create_backup(tmp_path):
    db = tmp_path / "weather.db"
    backup_dir = tmp_path / "backups"
    make_db(db)

    result = BackupService(backup_dir).create_backup(db)

    assert result.integrity_ok is True
    assert result.destination.exists()
    assert result.size_bytes > 0

def test_restore_backup(tmp_path):
    db = tmp_path / "weather.db"
    backup_dir = tmp_path / "backups"
    restored = tmp_path / "restored.db"
    make_db(db)

    service = BackupService(backup_dir)
    result = service.create_backup(db)
    restore = service.restore_backup(result.destination, restored)

    assert restore.integrity_ok is True
    with sqlite3.connect(restored) as conn:
        assert conn.execute("SELECT value FROM sample").fetchone()[0] == "ok"
