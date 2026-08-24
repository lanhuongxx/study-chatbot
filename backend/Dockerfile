# 1. Base image Python
FROM python:3.13-slim

# 2. Thiết lập thư mục làm việc
WORKDIR /app

# 3. Copy và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy toàn bộ code vào container
COPY . .

# 5. Mở port 8000
EXPOSE 8000

# 6. Lệnh chạy FastAPI Server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]