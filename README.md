# Run Local (Tanpa Deploy)

1. Pastikan Python sudah terpasang:

```bash
python --version
```

2. Buat virtual environment:

```bash
python -m venv venv
```

3. Aktifkan virtual environment:

```bash
# CMD
venv\Scripts\activate

# PowerShell
.\venv\Scripts\activate
```

4. Install dependency:

```bash
pip install -r requirements.txt
```

5. Jalankan aplikasi lokal:

```bash
python app.py
```

Server hanya bind ke `127.0.0.1` di port `5000` (atau sesuai `APP_PORT` di `.env`).
