# Bài 1 - Gửi và nhận message cơ bản qua queue

## 1. Mô tả

Mô phỏng hệ thống IoT theo mô hình **Producer - Consumer**.

- `producer_bai1.py`: mô phỏng cảm biến, sinh nhiệt độ và độ ẩm ngẫu nhiên, gửi dữ liệu mỗi 3 giây.
- `consumer_bai1.py`: nhận dữ liệu, hiển thị thông tin và phát hiện cảnh báo.

## 2. Broker sử dụng

Sử dụng **RabbitMQ** với giao thức **AMQP**.

Queue:

```text
sensor_data_queue
```

Payload JSON:

```json
{
    "device_id": "sensor01",
    "temperature": 29.5,
    "humidity": 62.1
}
```

## 3. Cách chạy

Cài thư viện:

```cmd
pip install pika
```

Khởi động RabbitMQ:

```cmd
docker start rabbitmq
```

Chạy Consumer:

```cmd
python monitoring_consumer.py
```

Mở terminal khác và chạy Producer:

```cmd
python producer_bai1.py
```

## 4. Kết quả

Producer gửi dữ liệu định kỳ:

```text
Sent: {"device_id": "sensor01", "temperature": 36.4, "humidity": 38.9}
```

Consumer nhận và xử lý:

```text
Device: sensor01
Temperature: 36.4
Humidity: 38.9
CANH BAO: Nhiet do cao
CANH BAO: Do am thap
```

**Kết quả:** Dữ liệu được gửi tuần hoàn qua queue và Consumer phát hiện đúng các điều kiện cảnh báo.

# Bài 2 - Mô phỏng cảm biến IoT gửi dữ liệu môi trường

## 1. Mô tả

Mô phỏng thiết bị IoT gửi telemetry gồm nhiệt độ và độ ẩm.

- `sensor_producer_bai2.py`: sinh dữ liệu ngẫu nhiên và gửi mỗi 3 giây.
- `monitor_consumer_bai2.py`: nhận dữ liệu và kiểm tra cảnh báo.

## 2. Broker sử dụng

Sử dụng **RabbitMQ** với giao thức **AMQP**.

Queue:

```text
sensor_data_queue
```

Payload:

```json
{
    "device_id": "sensor01",
    "temperature": 29.5,
    "humidity": 62.1
}
```

Điều kiện cảnh báo:

```text
temperature > 35 → CANH BAO: Nhiet do cao
humidity < 40    → CANH BAO: Do am thap
```

## 3. Cách chạy

Cài thư viện:

```cmd
pip install pika
```

Khởi động RabbitMQ:

```cmd
docker start rabbitmq
```

Chạy Consumer:

```cmd
python monitor_consumer_bai2.py
```

Mở terminal khác và chạy Producer:

```cmd
python sensor_producer_bai2.py
```

## 4. Kết quả

Ví dụ:

```text
Device: sensor01
Temperature: 36.4
Humidity: 38.9
CANH BAO: Nhiet do cao
CANH BAO: Do am thap
```

**Kết quả:** Payload đúng định dạng JSON, Producer gửi dữ liệu tuần hoàn và Consumer xử lý, phát hiện cảnh báo chính xác.

# Bài 3 - Mô phỏng hệ thống điều phối cảnh báo IoT với Exchange

## 1. Mô tả

Mô phỏng hệ thống phân phối cảnh báo IoT sử dụng **Exchange** và **Routing Key**.

- `alert_producer_bai3.py`: gửi các cảnh báo `info`, `warning`, `critical`.
- `warning_consumer_bai3.py`: chỉ nhận cảnh báo `warning`.
- `critical_consumer_bai3.py`: chỉ nhận cảnh báo `critical`.

## 2. Broker sử dụng

Sử dụng **RabbitMQ** với giao thức **AMQP**.

Direct Exchange:

```text
iot_alert_exchange
```

Routing key:

```text
info
warning
critical
```

Queue và binding:

```text
warning → warning_queue
critical → critical_queue
```

## 3. Cách chạy

Khởi động RabbitMQ:

```cmd
docker start rabbitmq
```

Chạy Warning Consumer:

```cmd
python warning_consumer_bai3.py
```

Chạy Critical Consumer:

```cmd
python critical_consumer_bai3.py
```

Mở terminal khác và chạy Producer:

```cmd
python alert_producer_bai3.py
```

## 4. Kết quả

Producer gửi:

```text
info
warning
critical
```

Warning Consumer:

```text
[warning_queue] Da nhan: Nhiet do phong may vuot nguong warning
```

Critical Consumer:

```text
[critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical
```

Message `info` không được consumer nào nhận.

**Kết quả:** Exchange được tạo, queue được bind đúng routing key và message được phân phối đúng nơi nhận.