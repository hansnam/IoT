# Bài 1. Ứng dụng gửi và nhận thông điệp MQTT cơ bản

## Mô tả

Ứng dụng Python sử dụng giao thức MQTT theo mô hình Publisher/Subscriber.

- `publisher_bai1.py`: Kết nối MQTT Broker và gửi message đến topic iot/lab/message mỗi 2 giây.
- `subscriber_bai1.py`: Đăng ký topic iot/lab/message, nhận và hiển thị message cùng thời gian nhận.
- Nhấn `Ctrl+C` để dừng chương trình.

## Cài đặt

pip install paho-mqtt

##  Chạy chương trình

<b>Terminal 1:</b>
```bash
python subscriber_bai1.py
```
Terminal 2:</b>
```bash
python publisher_bai1.py
```
## MQTT

- Broker: broker.emqx.io
-  Port: 1883
- Topic: iot/lab/message


# Bài 2 - Mô phỏng cảm biến nhiệt độ và độ ẩm bằng MQTT

## Mô tả

Mô phỏng nhiều thiết bị IoT gửi dữ liệu nhiệt độ và độ ẩm qua MQTT.

* `sensor_publisher_bai2.py`: Mô phỏng các sensor và gửi dữ liệu JSON mỗi 3 giây.
* `monitoring_subscriber_bai2.py`: Nhận dữ liệu, hiển thị và kiểm tra ngưỡng cảnh báo.

## MQTT

* Broker: `test.mosquitto.org`
* Port: `1883`
* Topic: `iot/lab/sensor/data`

## Dữ liệu

```json
{
  "device_id": "sensor01",
  "temperature": 28.5,
  "humidity": 65.2
}
```

## Cảnh báo

* Nhiệt độ > 35°C → `CANH BAO: Nhiet do cao`
* Độ ẩm < 40% → `CANH BAO: Do am thap`

## Chạy chương trình

<b>Terminal 1:</b>
```bash
python monitoring_subscriber_bai2.py
```
<b>Terminal 2:</b>
```bash
python sensor_publisher_bai2.py
```

Nhấn `Ctrl+C` để dừng chương trình.


# Bài 3 - Điều khiển đèn thông minh qua MQTT

## Mô tả

Mô phỏng hệ thống điều khiển đèn thông minh hai chiều bằng MQTT.

* `smart_light_bai3.py`: Mô phỏng thiết bị đèn, nhận lệnh ON/OFF và gửi trạng thái.
* `controller_bai3.py`: Gửi lệnh điều khiển và nhận trạng thái từ đèn.

## MQTT

* Broker: `test.mosquitto.org`
* Port: `1883`
* Command Topic: `iot/lab/light01/cmd`
* Status Topic: `iot/lab/light01/status`

## Lệnh

* `ON`: Bật đèn.
* `OFF`: Tắt đèn.
* `EXIT`: Thoát Controller.

## Chạy chương trình

<b>Terminal 1:</b>
```bash
python smart_light_bai3.py
```
<b>Terminal 2:</b>
```bash
python controller_bai3.py
```

Sau đó nhập `ON`, `OFF` hoặc `EXIT`.

## Ví dụ

```text
Nhap lenh: ON
Da gui lenh ON toi light01

Trang thai nhan duoc:
{"device_id":"light01","status":"ON"}
```

Nhấn `Ctrl+C` để dừng chương trình.

