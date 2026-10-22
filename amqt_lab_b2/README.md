# BÁO CÁO THỰC HÀNH IoT - BÀI THỰC HÀNH AMQP / RABBITMQ
**Môn học:** Lập trình / Thực hành IoT  
**Nhóm thực hiện:**  
- Trần Hán Nam - B23DCCN590  
- Đàm Tiến Thành - B23DCCN764  
- Nguyễn Hoàng Long - B23DCCN504  
  

---

# I. MÔI TRƯỜNG VÀ CÀI ĐẶT CHUNG

### 1. Phiên bản Python và các thư viện sử dụng
- **Phiên bản Python:** Python 3.10+
- **Các thư viện sử dụng:**
  - `pika` (Phiên bản `1.4.4`): Thư viện AMQP 0-9-1 client chính thức cho Python, dùng để tương tác với RabbitMQ Broker (kết nối, khai báo Queue, Exchange, Binding, xác nhận thông điệp qua ack).
  - Thư viện chuẩn (Standard Library):
    - `json`: Đóng gói (serialize) và giải mã (deserialize) thông điệp dạng JSON.
    - `time`: Điều khiển chu kỳ trễ gửi dữ liệu (`time.sleep(3)`).
    - `random`: Sinh số ngẫu nhiên mô phỏng số liệu đo lường của cảm biến.

### 2. Cách cài đặt môi trường
Mở cửa sổ dòng lệnh (Terminal / PowerShell) tại thư mục `amqt_lab_b2`:

- **Bước 1: Khởi tạo và kích hoạt môi trường ảo:**
  ```bash
  # Tạo môi trường ảo
  python -m venv venv

  # Kích hoạt trên Windows:
  venv\Scripts\activate

  # Kích hoạt trên Linux / macOS:
  source venv/bin/activate
  ```

- **Bước 2: Cài đặt thư viện Pika:**
  ```bash
  pip install pika
  ```

- **Bước 3: Cài đặt và khởi chạy RabbitMQ Broker:**
  Hệ thống sử dụng RabbitMQ Broker hoạt động cục bộ (Localhost). Cách triển khai chuẩn hóa qua Docker:
  ```bash
  # Khởi tạo và chạy container RabbitMQ có giao diện quản lý Management:
  docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

  # Trường hợp container đã có sẵn từ trước:
  docker start rabbitmq
  ```
  - Cổng dịch vụ AMQP: `localhost:5672`
  - Giao diện quản lý Web Dashboard: `http://localhost:15672` (Tài khoản / Mật khẩu mặc định: `guest` / `guest`).

---

# II. NỘI DUNG VÀ KẾT QUẢ TỪNG BÀI

---

## BÀI 1: GỬI VÀ NHẬN MESSAGE CƠ BẢN QUA QUEUE

### 1. Mô tả bài toán
Mô phỏng kiến trúc Producer - Consumer cơ bản qua hàng đợi tin nhắn của RabbitMQ:
- `producer_bai1.py`: Kết nối tới RabbitMQ, khai báo hàng đợi bền vững `sensor_data_queue` (`durable=True`). Sinh dữ liệu ngẫu nhiên và gửi thông điệp ở chế độ lưu trữ an toàn `delivery_mode=2` định kỳ mỗi 3 giây.
- `consumer_bai1.py`: Lắng nghe trên hàng đợi với cơ chế phân phối tải công bằng (`prefetch_count=1`), nhận tin nhắn, bóc tách JSON, kiểm tra cảnh báo và gửi xác nhận xử lý thủ công `basic_ack`.

### 2. Cách chạy chương trình
Cần mở 2 cửa sổ Terminal riêng biệt:
- **Terminal 1 (Chạy Consumer để sẵn sàng nhận dữ liệu):**
  ```bash
  python consumer_bai1.py
  ```
- **Terminal 2 (Chạy Producer để bắt đầu phát dữ liệu):**
  ```bash
  python producer_bai1.py
  ```
- *Dừng chương trình:* Nhấn `Ctrl + C` trên từng Terminal.

### 3. Địa chỉ IP, cổng và URI các tài nguyên CoAP / AMQP
- **Thông số mạng AMQP thực tế:**
  - Broker Host / IP: `localhost` / `127.0.0.1`
  - Cổng AMQP (Port): `5672`
  - Cổng Web Dashboard: `15672`
  - Tên hàng đợi (Queue): `sensor_data_queue` (Thuộc tính: `durable=True`)
  - Exchange: Default Exchange (`exchange=""`, định tuyến trực tiếp theo tên Queue)
  - Cấu trúc Payload: JSON:
    ```json
    {
      "device_id": "sensor01",
      "temperature": 36.4,
      "humidity": 38.9
    }
    ```
- **Ánh xạ sang URI tài nguyên CoAP tương đương (Port chuẩn `5683`):**
  - URI tài nguyên CoAP: `coap://127.0.0.1:5683/sensors/telemetry_queue`
  - Phương thức CoAP tương đương: `POST` (đẩy dữ liệu vào hàng đợi) hoặc `GET` kèm `Observe` (để nhận tuần tự các phần tử dữ liệu).

### 4. Kết quả đạt được của bài 1
- Thiết lập kênh truyền thông điệp bất đồng bộ bảo toàn dữ liệu (Message Persistence).
- Producer gửi dữ liệu đều đặn mỗi 3 giây.
- Consumer xử lý tuần tự từng tin nhắn (`prefetch_count=1`), xác nhận `basic_ack` sau khi xử lý thành công, đảm bảo tin nhắn không bị thất thoát nếu Consumer đột ngột bị gián đoạn.

### 5. Hình ảnh hoặc log minh chứng chương trình hoạt động

**Terminal 2 - `producer_bai1.py`:**
```text
Sensor Producer started...
Sending data to queue: sensor_data_queue
Sent: {"device_id": "sensor01", "temperature": 32.1, "humidity": 65.4}
Sent: {"device_id": "sensor01", "temperature": 36.4, "humidity": 38.9}
Sent: {"device_id": "sensor01", "temperature": 27.5, "humidity": 72.0}
^C
Producer stopped.
```

**Terminal 1 - `consumer_bai1.py`:**
```text
Monitoring Consumer started...
Waiting for messages from: sensor_data_queue
Press Ctrl+C to stop.

-----------------------------
Device: sensor01
Temperature: 32.1
Humidity: 65.4

-----------------------------
Device: sensor01
Temperature: 36.4
Humidity: 38.9
CANH BAO: Nhiet do cao
CANH BAO: Do am thap

-----------------------------
Device: sensor01
Temperature: 27.5
Humidity: 72.0
^C
Consumer stopped.
```

---

## BÀI 2: MÔ PHỎNG CẢM BIẾN IoT GỬI DỮ LIỆU MÔI TRƯỜNG VÀ GIÁM SÁT NGƯỠNG

### 1. Mô tả bài toán
Mô phỏng thiết bị cảm biến môi trường đo đạc nhiệt độ, độ ẩm và hệ thống giám sát cảnh báo tự động:
- `sensor_producer_bai2.py`: Đóng vai trò cảm biến `sensor01`, sinh ngẫu nhiên nhiệt độ từ 20.0 đến 40.0°C và độ ẩm từ 30.0 đến 80.0%, gửi JSON vào hàng đợi `sensor_data_queue` mỗi 3 giây.
- `monitor_consumer_bai2.py`: Lắng nghe hàng đợi, giải mã gói tin JSON và kiểm tra các điều kiện cảnh báo nghiệp vụ:
  - `temperature > 35` $\rightarrow$ In thông báo: `CANH BAO: Nhiet do cao`.
  - `humidity < 40` $\rightarrow$ In thông báo: `CANH BAO: Do am thap`.
  - Gửi `ch.basic_ack()` xác nhận hoàn tất xử lý.

### 2. Cách chạy chương trình
- **Terminal 1 (Chạy Monitor Consumer trước):**
  ```bash
  python monitor_consumer_bai2.py
  ```
- **Terminal 2 (Chạy Sensor Producer):**
  ```bash
  python sensor_producer_bai2.py
  ```
- *Dừng chương trình:* Nhấn `Ctrl + C`.

### 3. Địa chỉ IP, cổng và URI các tài nguyên CoAP / AMQP
- **Thông số mạng AMQP thực tế:**
  - Broker Host / IP: `localhost` / `127.0.0.1`
  - Cổng AMQP (Port): `5672`
  - Tên hàng đợi (Queue): `sensor_data_queue`
  - Định dạng dữ liệu: JSON chuẩn IoT Telemetry.
- **Ánh xạ sang URI tài nguyên CoAP tương đương (Port chuẩn `5683`):**
  - URI tài nguyên CoAP: `coap://127.0.0.1:5683/sensors/sensor01/environment`
  - Phương thức CoAP tương đương: `POST` (gửi mẫu tin đo đạc) và `GET` (`Observe` để theo dõi cảnh báo ngưỡng).

### 4. Kết quả đạt được của bài 2
- Mô phỏng hoàn chỉnh chu trình thu thập và xử lý số liệu môi trường theo thời gian thực.
- Consumer lọc và phát hiện chính xác các trường hợp số liệu vượt ngưỡng cảnh báo nhiệt độ cao hoặc độ ẩm thấp.
- Cơ chế `auto_ack=False` kết hợp gọi `basic_ack` thủ công đảm bảo tính an toàn dữ liệu cao trong các hệ thống giám sát công nghiệp.

### 5. Hình ảnh hoặc log minh chứng chương trình hoạt động

**Terminal 2 - `sensor_producer_bai2.py`:**
```text
Sensor Producer started...
Sending data to queue: sensor_data_queue
Sent: {"device_id": "sensor01", "temperature": 29.5, "humidity": 62.1}
Sent: {"device_id": "sensor01", "temperature": 37.2, "humidity": 35.8}
Sent: {"device_id": "sensor01", "temperature": 31.0, "humidity": 50.4}
^C
Producer stopped.
```

**Terminal 1 - `monitor_consumer_bai2.py`:**
```text
Monitoring Consumer started...
Waiting for messages from: sensor_data_queue

-----------------------------
Device: sensor01
Temperature: 29.5
Humidity: 62.1

-----------------------------
Device: sensor01
Temperature: 37.2
Humidity: 35.8
CANH BAO: Nhiet do cao
CANH BAO: Do am thap

-----------------------------
Device: sensor01
Temperature: 31.0
Humidity: 50.4
```

---

## BÀI 3: MÔ PHỎNG HỆ THỐNG ĐIỀU PHỐI CẢNH BÁO IoT VỚI EXCHANGE

### 1. Mô tả bài toán
Xây dựng hệ thống phân phối và định tuyến thông điệp thông minh dựa trên mô hình **Direct Exchange** và **Routing Key** của RabbitMQ:
- Khởi tạo Exchange: `iot_alert_exchange` (loại `direct`, `durable=True`).
- `alert_producer_bai3.py`: Phát đi 3 mức cảnh báo với routing key tương ứng:
  - `info`: "Nhiet do phong may chuot muc info"
  - `warning`: "Nhiet do phong may vuot nguong warning"
  - `critical`: "Cam bien kho lanh mat ket noi critical"
- `warning_consumer_bai3.py`: Khởi tạo `warning_queue` và bind với routing key `warning` $\rightarrow$ chỉ tiếp nhận cảnh báo warning.
- `critical_consumer_bai3.py`: Khởi tạo `critical_queue` và bind với routing key `critical` $\rightarrow$ chỉ tiếp nhận cảnh báo critical.

### 2. Cách chạy chương trình
Cần mở đồng thời 3 cửa sổ Terminal:
- **Terminal 1 (Chạy Warning Consumer):**
  ```bash
  python warning_consumer_bai3.py
  ```
- **Terminal 2 (Chạy Critical Consumer):**
  ```bash
  python critical_consumer_bai3.py
  ```
- **Terminal 3 (Chạy Alert Producer để phát cảnh báo):**
  ```bash
  python alert_producer_bai3.py
  ```

### 3. Địa chỉ IP, cổng và URI các tài nguyên CoAP / AMQP
- **Thông số mạng AMQP thực tế:**
  - Broker Host / IP: `localhost` / `127.0.0.1`
  - Cổng (Port): `5672`
  - Exchange: `iot_alert_exchange` (Type: `direct`)
  - Routing Keys: `info`, `warning`, `critical`
  - Hàng đợi và Binding:
    - `warning_queue` $\leftrightarrow$ gắn với routing key `warning`
    - `critical_queue` $\leftrightarrow$ gắn với routing key `critical`
- **Ánh xạ sang URI tài nguyên CoAP tương đương (Port chuẩn `5683`):**
  - URI tài nguyên CoAP:
    - Nhánh Warning: `coap://127.0.0.1:5683/alerts/warning`
    - Nhánh Critical: `coap://127.0.0.1:5683/alerts/critical`
    - Nhánh Info: `coap://127.0.0.1:5683/alerts/info`
  - Phương thức CoAP tương đương: `POST` (để gửi cảnh báo phân cấp) hoặc `GET` (`Observe` trên URI tương ứng để đăng ký nhận cảnh báo theo từng mức độ quan tâm).

### 4. Kết quả đạt được của bài 3
- Làm chủ cơ chế định tuyến nâng cao của AMQP: Message không đẩy thẳng vào Queue mà đi qua Exchange để phân loại theo Routing Key.
- `warning_consumer_bai3.py` chỉ nhận chính xác thông điệp có nhãn `warning`.
- `critical_consumer_bai3.py` chỉ nhận chính xác thông điệp có nhãn `critical`.
- Thông điệp có nhãn `info` không có Queue nào đăng ký ràng buộc nên được Broker tự động loại bỏ một cách an toàn mà không gây nghẽn hệ thống.

### 5. Hình ảnh hoặc log minh chứng chương trình hoạt động

**Terminal 3 - `alert_producer_bai3.py`:**
```text
[Producer] Da gui (info): Nhiet do phong may chuot muc info
[Producer] Da gui (warning): Nhiet do phong may vuot nguong warning
[Producer] Da gui (critical): Cam bien kho lanh mat ket noi critical
```

**Terminal 1 - `warning_consumer_bai3.py`:**
```text
[Warning Consumer] Dang cho canh bao warning...
[warning_queue] Da nhan: Nhiet do phong may vuot nguong warning
```

**Terminal 2 - `critical_consumer_bai3.py`:**
```text
[Critical Consumer] Dang cho canh bao critical...
[critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical
```

*(Nhận xét: Kết quả chứng minh cơ chế phân phối tải và định tuyến dựa trên Direct Exchange của AMQP hoạt động chính xác theo đúng lý thuyết và yêu cầu thực hành).*