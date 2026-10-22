# BÁO CÁO THỰC HÀNH IoT - BÀI THỰC HÀNH MQTT

**Môn học:** Lập trình / Thực hành IoT  
**Nhóm thực hiện:**  
- Trần Hán Nam - B23DCCN590  
- Đàm Tiến Thành - B23DCCN764  
- Nguyễn Hoàng Long - B23DCCN504  

**Thư mục bài tập:** `mqtt_lab_b1`  

---

# I. MÔI TRƯỜNG VÀ CÀI ĐẶT CHUNG

### 1. Phiên bản Python và các thư viện sử dụng
- **Phiên bản Python:** Python 3.10+
- **Các thư viện sử dụng:**
  - `paho-mqtt` (Phiên bản `2.1.0`): Thư viện client giao tiếp với MQTT Broker, sử dụng Callback API v2 (`CallbackAPIVersion.VERSION2`).
  - Thư viện chuẩn (Standard Library):
    - `json`: Đóng gói (serialize) và giải mã (deserialize) dữ liệu tin nhắn dạng JSON.
    - `time`: Điều khiển chu kỳ trễ gửi dữ liệu (`time.sleep`) và độ trễ chờ phản hồi.
    - `random`: Mô phỏng số liệu ngẫu nhiên của các cảm biến môi trường.
    - `datetime`: Trích xuất dấu thời gian thực (`H:M:S`) khi nhận thông điệp.

### 2. Cách cài đặt môi trường
Mở cửa sổ dòng lệnh (Terminal / PowerShell) tại thư mục `mqtt_lab_b1`:

- **Bước 1: Khởi tạo và kích hoạt môi trường ảo:**
  ```bash
  # Khởi tạo môi trường ảo
  python -m venv venv

  # Kích hoạt trên Windows:
  venv\Scripts\activate

  # Kích hoạt trên Linux / macOS:
  source venv/bin/activate
  ```

- **Bước 2: Cài đặt thư viện Paho MQTT:**
  ```bash
  pip install paho-mqtt
  ```

- **Bước 3: Kiểm tra kết nối tới MQTT Broker:**
  Broker sử dụng là Public MQTT Broker: `test.mosquitto.org` trên cổng `1883`. Kiểm tra kết nối mạng bằng lệnh:
  ```powershell
  Test-NetConnection -ComputerName test.mosquitto.org -Port 1883
  ```
  *(Kết quả `TcpTestSucceeded : True` xác nhận Broker hoạt động bình thường).*

---

# II. NỘI DUNG VÀ KẾT QUẢ TỪNG BÀI

---

## BÀI 1: ỨNG DỤNG GỬI VÀ NHẬN THÔNG ĐIỆP MQTT CƠ BẢN

### 1. Mô tả bài toán
Mô phỏng mô hình Publish/Subscribe cơ bản bằng Python qua MQTT:
- `publisher_bai1.py`: Kết nối tới MQTT Broker và phát chuỗi thông điệp kèm mã sinh viên mỗi 2 giây.
- `subscriber_bai1.py`: Lắng nghe topic chung, nhận dữ liệu và in ra màn hình kèm thời gian thực nhận được.

### 2. Cách chạy chương trình
Cần mở 2 cửa sổ Terminal riêng biệt:
- **Terminal 1 (Chạy Subscriber trước):**
  ```bash
  python subscriber_bai1.py
  ```
- **Terminal 2 (Chạy Publisher để gửi tin):**
  ```bash
  python publisher_bai1.py
  ```
- *Dừng chương trình:* Nhấn `Ctrl + C` trên từng terminal.

### 3. Địa chỉ IP, cổng và URI các tài nguyên CoAP / MQTT
- **Thông số kết nối MQTT thực tế:**
  - Broker Host / IP: `test.mosquitto.org` (`54.36.178.49`)
  - Cổng kết nối (Port): `1883` (TCP không mã hóa)
  - Topic MQTT: `iot/lab/message`
- **Ánh xạ sang URI tài nguyên CoAP tương đương (Port chuẩn `5683`):**
  - URI tài nguyên CoAP: `coap://test.mosquitto.org:5683/iot/message`
  - Phương thức CoAP tương đương: `POST` (để gửi message) và `GET` (để lấy message).

### 4. Kết quả đạt được của bài 1
- Thiết lập kết nối ổn định giữa MQTT Client và Public Broker `test.mosquitto.org:1883`.
- Publisher tự động đánh số thứ tự `Message i`, đóng gói chuỗi định danh và xuất bản tuần hoàn mỗi 2 giây.
- Subscriber nhận đầy đủ thông điệp theo thời gian thực, không thất thoát gói tin, hiển thị rõ ràng kèm dấu thời gian hệ thống (`HH:MM:SS`).

### 5. Hình ảnh hoặc log minh chứng chương trình hoạt động

**Terminal 2 - `publisher_bai1.py`:**
```text
Dang ket noi toi MQTT Broker ...
Ket noi thanh cong
Da gui: Xin chao tu client Python MQTT - B23DCCN590 - Tran Han Nam - Message 1
Da gui: Xin chao tu client Python MQTT - B23DCCN590 - Tran Han Nam - Message 2
Da gui: Xin chao tu client Python MQTT - B23DCCN590 - Tran Han Nam - Message 3
Da gui: Xin chao tu client Python MQTT - B23DCCN590 - Tran Han Nam - Message 4
^CDung publisher...
Da ngat ket noi.
```

**Terminal 1 - `subscriber_bai1.py`:**
```text
Dang ket noi toi MQTT Broker...
Ket noi MQTT Broker thanh cong!
Dang lang nghe topic: iot/lab/message
Cho message...

Nhan duoc message:
Topic: iot/lab/message
Payload: Xin chao tu client Python MQTT - B23DCCN590 - Tran Han Nam - Message 1
Time: 16:38:00
----------------------------------------
Nhan duoc message:
Topic: iot/lab/message
Payload: Xin chao tu client Python MQTT - B23DCCN590 - Tran Han Nam - Message 2
Time: 16:38:02
----------------------------------------
Nhan duoc message:
Topic: iot/lab/message
Payload: Xin chao tu client Python MQTT - B23DCCN590 - Tran Han Nam - Message 3
Time: 16:38:04
----------------------------------------
^CDang ngat ket noi...
Da ngat ket noi MQTT Broker.
```

---

## BÀI 2: MÔ PHỎNG CẢM BIẾN NHIỆT ĐỘ - ĐỘ ẨM VÀ GIÁM SÁT CẢNH BÁO

### 1. Mô tả bài toán
Mô phỏng luồng telemetry của thiết bị cảm biến môi trường IoT và hệ thống giám sát cảnh báo:
- `sensor_publisher_bai2.py`: Mô phỏng cảm biến `sensor01`, sinh ngẫu nhiên nhiệt độ (25.0 - 40.0°C) và độ ẩm (30.0 - 80.0%), đóng gói JSON gửi mỗi 3 giây.
- `monitor_subscriber_bai2.py`: Lắng nghe dữ liệu, bóc tách JSON và kiểm tra ngưỡng:
  - Nếu `temperature > 35` $\rightarrow$ Xuất thông báo `CANH BAO: Nhiet do cao`.
  - Nếu `humidity < 40` $\rightarrow$ Xuất thông báo `CANH BAO: Do am thap`.

### 2. Cách chạy chương trình
- **Terminal 1 (Chạy Monitor Subscriber trước):**
  ```bash
  python monitor_subscriber_bai2.py
  ```
- **Terminal 2 (Chạy Sensor Publisher):**
  ```bash
  python sensor_publisher_bai2.py
  ```
- *Dừng chương trình:* Nhấn `Ctrl + C`.

### 3. Địa chỉ IP, cổng và URI các tài nguyên CoAP / MQTT
- **Thông số kết nối MQTT thực tế:**
  - Broker Host / IP: `test.mosquitto.org` (`54.36.178.49`)
  - Cổng kết nối (Port): `1883`
  - Topic MQTT: `iot/lab/sensor01/data`
  - Định dạng Payload: JSON:
    ```json
    {
      "device_id": "sensor01",
      "temperature": 36.8,
      "humidity": 38.2
    }
    ```
- **Ánh xạ sang URI tài nguyên CoAP tương đương (Port chuẩn `5683`):**
  - URI tài nguyên CoAP: `coap://test.mosquitto.org:5683/sensors/sensor01/data`
  - Phương thức CoAP tương đương:
    - Cảm biến đẩy dữ liệu: `POST` payload JSON.
    - Bộ giám sát theo dõi dữ liệu: `GET` kèm tùy chọn `Observe` (RFC 7641) để tự động nhận luồng cập nhật số liệu mới nhất.

### 4. Kết quả đạt được của bài 2
- Mô phỏng thành công luồng telemetry của thiết bị IoT với cấu trúc JSON chuẩn mực.
- Hệ thống giám sát bắt gói tin tức thời, giải mã an toàn (có xử lý ngoại lệ JSONDecodeError).
- Kích hoạt cảnh báo chính xác khi nhiệt độ vượt 35°C hoặc độ ẩm dưới 40%.

### 5. Hình ảnh hoặc log minh chứng chương trình hoạt động

**Terminal 2 - `sensor_publisher_bai2.py`:**
```text
Dang ket noi toi MQTT Broker...
Ket noi thanh cong!
Sensor dang gui du lieu moi 3 giay.
Nhan Ctrl+C de dung.

Da gui:
Device: sensor01
Temperature: 36.8 C
Humidity: 38.2 %
------------------------------
Da gui:
Device: sensor01
Temperature: 28.4 C
Humidity: 65.5 %
------------------------------
Da gui:
Device: sensor01
Temperature: 37.5 C
Humidity: 55.0 %
------------------------------
```

**Terminal 1 - `monitor_subscriber_bai2.py`:**
```text
Dang ket noi toi MQTT Broker...
Ket noi MQTT Broker thanh cong!
Dang lang nghe: iot/lab/sensor01/data
Cho du lieu sensor...

Device: sensor01
Temperature: 36.8 C
Humidity: 38.2 %
CANH BAO: Nhiet do cao
CANH BAO: Do am thap
------------------------------
Device: sensor01
Temperature: 28.4 C
Humidity: 65.5 %
------------------------------
Device: sensor01
Temperature: 37.5 C
Humidity: 55.0 %
CANH BAO: Nhiet do cao
------------------------------
```

---

## BÀI 3: ĐIỀU KHIỂN THIẾT BỊ HAI CHIỀU (SMART LIGHT & CONTROLLER)

### 1. Mô tả bài toán
Xây dựng hệ thống điều khiển và phản hồi trạng thái hai chiều khép kín (Closed-loop Control):
- `device_bai3.py`: Đóng vai trò đèn thông minh `light01`, đăng ký topic lệnh để chờ lệnh `ON`/`OFF`. Khi nhận lệnh hợp lệ, cập nhật trạng thái thiết bị và xuất bản JSON trạng thái hiện tại lên topic phản hồi.
- `controller_bai3.py`: Nhận lệnh người dùng nhập (`ON`, `OFF`, `EXIT`), gửi tới đèn và lắng nghe phản hồi xác nhận trạng thái từ đèn.

### 2. Cách chạy chương trình
- **Terminal 1 (Chạy thiết bị Smart Light trước):**
  ```bash
  python device_bai3.py
  ```
- **Terminal 2 (Chạy Controller để nhập lệnh điều khiển):**
  ```bash
  python controller_bai3.py
  ```
- *Tương tác tại Terminal 2:*
  - Nhập `ON` $\rightarrow$ Gửi lệnh bật đèn, chờ phản hồi xác nhận.
  - Nhập `OFF` $\rightarrow$ Gửi lệnh tắt đèn, chờ phản hồi xác nhận.
  - Nhập `EXIT` $\rightarrow$ Thoát an toàn khỏi Controller.

### 3. Địa chỉ IP, cổng và URI các tài nguyên CoAP / MQTT
- **Thông số kết nối MQTT thực tế:**
  - Broker Host / IP: `test.mosquitto.org` (`54.36.178.49`), Cổng (Port): `1883`
  - Topic gửi lệnh điều khiển (Controller $\rightarrow$ Device): `iot/lab/light01/cmd`
  - Topic phản hồi trạng thái (Device $\rightarrow$ Controller): `iot/lab/light01/status`
- **Ánh xạ sang URI tài nguyên CoAP tương đương (Port chuẩn `5683`):**
  - URI tài nguyên CoAP: `coap://test.mosquitto.org:5683/actuators/light01`
  - Phương thức CoAP tương đương:
    - Đọc trạng thái đèn: `GET` (trả về trạng thái hiện tại `{"status": "ON"}`).
    - Điều khiển bật/tắt đèn: `PUT` hoặc `POST` với payload `{"command": "ON"}` hoặc `{"status": "OFF"}`.

### 4. Kết quả đạt được của bài 3
- Thiết lập tương tác điều khiển hai chiều hoạt động trơn tru theo thời gian thực.
- Đèn cập nhật trạng thái nội bộ và phản hồi bản tin trạng thái JSON `{"device_id": "light01", "status": "ON/OFF"}` trở lại, giúp Controller hiển thị thông tin xác nhận chính xác.

### 5. Hình ảnh hoặc log minh chứng chương trình hoạt động

**Terminal 1 - `device_bai3.py` (Smart Light):**
```text
Dang ket noi toi MQTT Broker...
Smart Light da ket noi MQTT Broker.
Dang cho lenh tai: iot/lab/light01/cmd

Nhan lenh: ON
Da cap nhat den: ON
Da gui trang thai: {"device_id": "light01", "status": "ON"}
----------------------------------------
Nhan lenh: OFF
Da cap nhat den: OFF
Da gui trang thai: {"device_id": "light01", "status": "OFF"}
----------------------------------------
```

**Terminal 2 - `controller_bai3.py` (Controller):**
```text
Dang ket noi toi MQTT Broker...
Controller da ket noi MQTT Broker.
Dang lang nghe: iot/lab/light01/status

Nhap lenh (ON/OFF/EXIT): ON
Da gui lenh ON toi light01

Trang thai nhan duoc:
{"device_id": "light01", "status": "ON"}

Nhap lenh (ON/OFF/EXIT): OFF
Da gui lenh OFF toi light01

Trang thai nhan duoc:
{"device_id": "light01", "status": "OFF"}

Nhap lenh (ON/OFF/EXIT): EXIT
Dang thoat Controller...
Da ngat ket noi.
```
