# Webcrawling → Google Sheets Daily Report Automation
Whatap(웹 콘솔)에서 운영 지표를 **Selenium으로 자동 수집**하고, 집계된 값을 **Google Sheets 일일 보고 템플릿**에 자동 기입한 뒤  
결과 요약을 **Google Chat(Webhook)** 으로 전송하는 운영 자동화 스크립트입니다.

> “매일 같은 시간대 지표를 확인 → 표로 정리 → 시트에 붙여넣기 → 공유”  
> 이 반복 작업을 **한 번의 실행으로 끝내는** 것이 목표입니다.

---

## Features
- **Whatap 웹 콘솔 자동 로그인 + OTP(2FA)**
  - ID/PW 입력 후 TOTP(OTP) 생성(`pyotp`)로 2FA 단계까지 자동 처리
- **지표 자동 수집**
  - APM Metrics: **Active User(동시접속) 최대값 + 발생 시간**
  - Infra Report: WEB/WAS/DB 별 **CPU/Memory 평균 & 최대**
  - Network Metrics: **Inbound/Outbound 최대값**(단위 변환 포함)
- **자동 집계 및 출력**
  - stdout에 요약 테이블 출력(운영자가 바로 확인 가능)
- **Google Sheets 자동 기록**
  - 일자별 시트가 없으면 **템플릿 시트를 복제**하여 생성
  - 지정 범위 초기화 후(배치 클리어) **정해진 셀 위치에 값 업데이트**
  - 실행 시간에 따라 오전/오후 입력 위치 자동 분기
- **Webhook 알림**
  - 성공/실패 결과를 Google Chat(Webhook)으로 전송

---

## Flow / Architecture
(Cron / Scheduler). 
│. 
▼. 
Python Script. 
├─ Selenium: Whatap 로그인(ID/PW + OTP). 
├─ Crawl: APM / Infra Report / Network Metrics 수집. 
├─ Stats: 평균/최대 계산. 
├─ GSheet: 템플릿 복제 → 범위 초기화 → 셀 업데이트. 
└─ Webhook: 결과 요약/에러 알림 전송. 

---

## Collects
- **APM**
  - Active User 최대값 (예: 312명)
  - 최대값 발생 시간 (예: 09:41)
- **Infra (WEB/WAS/DB)**
  - CPU 평균/최대
  - Memory 평균/최대
- **Network**
  - Inbound Max, Outbound Max
  - (코드 기준) Byte → GB 변환 후 표기

---

## Requirements
- Python **3.9+** 권장
- Google Chrome
- ChromeDriver (Chrome 버전과 호환되는 버전)

### Python dependencies
- `selenium`
- `pyotp`
- `gspread`
- `oauth2client`
- `requests`