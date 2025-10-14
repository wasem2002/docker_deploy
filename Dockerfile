# -----------------------------
# 1️⃣ Base image with Python
# -----------------------------
FROM python:3.12-slim

# -----------------------------
# 2️⃣ Install OS-level libraries
# (includes libgomp1 to fix ImportError)
# -----------------------------
RUN apt-get update && apt-get install -y \
    libgomp1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# 3️⃣ Set working directory
# -----------------------------
WORKDIR /app

# -----------------------------
# 4️⃣ Copy dependencies first
# (for Docker caching)
# -----------------------------
COPY requirements.txt .

# -----------------------------
# 5️⃣ Install Python dependencies
# -----------------------------
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# 6️⃣ Copy the rest of your project files
# -----------------------------
COPY . .

# -----------------------------
# 7️⃣ Collect static files (no prompt)
# -----------------------------
RUN python manage.py collectstatic --noinput

# -----------------------------
# 8️⃣ Expose port 8000
# -----------------------------
EXPOSE 8000

# -----------------------------
# 9️⃣ Start the Django app using Gunicorn
# (replace `my_api` with your project name if different)
# -----------------------------
CMD ["gunicorn", "my_api.wsgi:application", "--bind", "0.0.0.0:8000"]
