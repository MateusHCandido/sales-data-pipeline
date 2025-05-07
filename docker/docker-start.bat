@echo off
echo 🔁 Subindo o MinIO...
docker-compose -f docker-compose.minio.yml up -d
timeout /t 10

echo 🔁 Subindo o PostgreSQL...
docker-compose -f docker-compose.postgres.yml up -d
timeout /t 10

echo 🔁 Subindo Kafka e Connect...
docker-compose -f docker-compose.kafka.yml up -d

echo ✅ Todos os serviços foram iniciados!
pause