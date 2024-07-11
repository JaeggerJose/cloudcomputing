# 使用官方Python運行時作為父映像
FROM python:3.8-slim

# 設定工作目錄為/app
WORKDIR /app

# 將當前目錄內容複製到容器中的/app
COPY ./app_mining /app

COPY ./test.py /app
# 安裝Python依賴
# 如果你的app.py依賴其他Python套件，請在這裡使用pip install命令安裝
# 例如: RUN pip install --trusted-host pypi.python.org Flask
RUN apt-get update && apt-get install -y \
    libcurl4 \
    && rm -rf /var/lib/apt/lists/*
    
# 賦予app_mining執行權限
RUN chmod +x app_mining

# 設定環境變量
# 讓Python輸出直接打印到終端，讓Docker的日誌能夠捕獲到
ENV PYTHONUNBUFFERED=1

# 啟動應用程式
CMD ["python", "./test.py"]
