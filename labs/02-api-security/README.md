services:
  secure-api:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      APP_DB_PATH: /tmp/api_security_lab.db
      JWT_SECRET: ${JWT_SECRET:?Set JWT_SECRET to a generated 32+ character value before running Docker}
      VULNERABLE_MODE: "false"

  vulnerable-api:
    build: .
    profiles: ["vulnerable-lab"]
    command: uvicorn app.vulnerable:app --host 0.0.0.0 --port 8001
    ports:
      - "127.0.0.1:8001:8001"
    environment:
      APP_DB_PATH: /tmp/api_security_lab_vulnerable.db
      JWT_SECRET: ${JWT_SECRET:?Set JWT_SECRET to a generated 32+ character value before running Docker}
      VULNERABLE_MODE: "true"
