# Bible Quiz — Trắc nghiệm Kinh Thánh (APK Android, Capacitor)

App song ngữ Anh–Việt (Việt 1925 + Anh KJV): vừa tra cứu 66 sách, vừa trắc
nghiệm 1.101 câu, mỗi lượt thi rút 30 câu ngẫu nhiên không lặp. Lần đầu mở
app cho chọn ngôn ngữ (mặc định English), lựa chọn được nhớ trên thiết bị,
muốn đổi phải vào Cài đặt.

- Bản web gốc: artifact `trac-nghiem-kinh-thanh`, export
  `workspace/your_files/trac-nghiem-kinh-thanh/trac-nghiem-kinh-thanh.html`
  — file này được dùng nguyên văn làm `www/index.html`, không viết lại.
- **Chạy offline:** toàn bộ nội dung câu hỏi + tra cứu nằm trong file HTML
  duy nhất. Chỉ có font Google Fonts là tải ngoài (có font dự phòng khi
  offline) và 2 link nguồn trong phần giới thiệu — không cần mạng cho quiz
  hay tra cứu.
- App: appId `com.tranphong.biblequiz`, appName `Bible Quiz`,
  versionCode 1, versionName 1.0, minSdk 24, targetSdk 36.

## Build

Đẩy lên `main` là GitHub Actions tự build APK debug
(`.github/workflows/build-apk.yml`): `npm install` → `npx cap add android`
→ `npx cap sync android` → ép minSdk 24 / targetSdk 36 (AGP 8.9.1 +
Gradle 8.11.1) → icon launcher → `./gradlew assembleDebug`.
Artifact: `bible-quiz-apk` (`app-debug.apk`).

Build tay ở máy: `npm install && npx cap add android && npx cap sync android`
rồi `cd android && ./gradlew assembleDebug`.
