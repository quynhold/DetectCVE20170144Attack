# Chương trình Python phát hiện tấn công CVE-2017-0144
Chương trình Python có nhiệm vụ theo dõi, giám sát lưu lượng mạng liên tục theo thời gian thực. Nó sẽ đưa ra cảnh báo lên màn hình console khi phát hiện tấn công CVE-2017-0144 (EternalBlue)
----------------------------
1. Mô hình bài lab

Lab này được thực hiện trên 3 máy ảo trong VMWare. 1 máy tấn công (Kali Linux), 1 máy nạn nhân (Windows 7 - 64bit SP1), 1 máy giám sát (Windows 10). Các máy có cùng card mạng (NAT) và đảm bảo rằng chúng có thể ping thấy nhau. Một số lưu ý:
- Máy Kali cần chú ý update lên phiên bản mới nhất ```sudo apt update```
- Máy Windows 7 tắt tường lửa
- Máy Windows 10 phải cài đặt Python

2. Các bước thực hiện

B0: Bật 3 máy trong mô hình

B1: Ở máy tấn công: Khởi động Metasploit. Có thể dùng lệnh ```msfconsole``` ở terminal để khởi động

B2: Tiếp tục ```search eternalblue``` để tìm module tấn công thích hợp. sử dụng module: ```use exploit/windows/smb/ms17_010_eternalblue```

B3: Thiết lập thông số ```set RHOST ```+ IP máy victim. 

B4: Ở máy giám sát: Chạy chương trình. Chương trình chạy sẽ ghi lại lưu lượng mạng vào file .csv, nếu phát hiện tấn công thì sẽ hiển thị thông báo lên console và ghi log lại vào file log.txt

B5: Ở máy tấn công: bắt đầu tiến hành tấn công ```exploit```

B6: Ở máy giám sát sẽ hiển thị thông báo phát hiện tấn công. Máy kali sẽ có session tới máy nạn nhân, có thể sử dụng lệnh ```shell``` để tiến hành mở CMD của victim. Hoàn thành lab.

3. Tài liệu tham khảo

Thông tin thêm về CVE-2017-0144:

 - https://en.wikipedia.org/wiki/EternalBlue

Tìm phiên bản OS phù hợp cho máy nạn nhân:
 - https://www.getmyos.com/ 
