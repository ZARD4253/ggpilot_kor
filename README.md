# 캐릭터 데이터 완전 자동화 파이프라인

## 개요
URL에서 HTML 다운로드부터 최종 pilot.js 생성까지 **완전 자동화**된 파이프라인입니다.

## 파일 구조
```
.
├── main.py                    # 메인 실행 스크립트
├── step1_download.py          # 1단계: HTML 다운로드
├── step2_parse.py             # 2단계: 파싱 (new3.py)
├── step3_translate_names.py   # 3단계: 이름 한글화
├── step4_json_to_js.py        # 4단계: JSON → JS 변환
├── requirements.txt           # 필요 패키지
├── jp_names.xlsx              # (선택) 일본어 이름 목록
├── ko_names.xlsx              # (선택) 한국어 이름 목록
│
├── nonsp.html                 # (생성됨)
├── sp.html                    # (생성됨)
├── characters.json            # (생성됨)
├── nameTranslations.json      # (생성됨, 선택)
└── pilot.js                   # (생성됨) ★ 최종 결과물
```

## 설치

```bash
pip install -r requirements.txt
```

또는 개별 설치:
```bash
pip install beautifulsoup4 requests pandas openpyxl lxml
```

## 사용 방법

### 기본 사용 (이름 한글화 없이)

```bash
python main.py
```

### 이름 한글화 포함 사용

1. 엑셀 파일 준비:
   - `jp_names.xlsx`: 마지막 열(D열)에 일본어 이름
   - `ko_names.xlsx`: 마지막 열(D열)에 한국어 이름

2. 실행:
```bash
python main.py
```

## 자동 실행 과정

```
[1단계] HTML 다운로드
  https://appmedia.jp/ggene_eternal/78594845 → nonsp.html
  https://appmedia.jp/ggene_eternal/79406921 → sp.html
  ↓
[2단계] 파싱 및 기본 한글화 (new3.py)
  - HTML 파싱
  - 태그, 시리즈, 스킬, 어빌리티 한글화
  - characters.json 생성
  ↓
[3단계] 이름 한글화 (선택)
  - jp_names.xlsx, ko_names.xlsx 사용
  - 캐릭터 이름 한글화
  - nameTranslations.json 생성
  ↓
[4단계] JSON → JS 변환
  - characters.json → pilot.js
  - const sampleData = [...] 형식
  ↓
완료! 🎉
```

## 생성되는 파일

### 중간 파일
- `nonsp.html`: NO SP 캐릭터 HTML
- `sp.html`: SP 캐릭터 HTML
- `characters.json`: 파싱된 캐릭터 데이터
- `nameTranslations.json`: 이름 번역 매핑 (선택)

### 최종 결과물
- **`pilot.js`**: 웹 애플리케이션에서 사용할 JavaScript 파일

```javascript
const sampleData = [
  {
    "id": 1,
    "name": "아무로",
    "jp_name": "アムロ",
    "icon": "...",
    "rarity": "UR",
    "type": "내구",
    "series": "기동전사 건담",
    "tags": ["우주세기 시리즈", "주인공", ...],
    "stats": {
      "shoot": 571,
      "melee": 532,
      "awake": 658,
      "guard": 703,
      "react": 802
    },
    "skills": [...],
    "abilities": [...]
  },
  ...
];
```

## 각 단계별 실행 (필요시)

각 단계를 개별적으로 실행할 수도 있습니다:

```bash
# 1단계만
python step1_download.py

# 2단계만
python step2_parse.py

# 3단계만
python step3_translate_names.py

# 4단계만
python step4_json_to_js.py
```

## 기능

✅ **완전 자동화**: URL → HTML → JSON → JS 전체 자동화
✅ **단계별 실행**: 필요시 각 단계별 개별 실행 가능
✅ **에러 처리**: 각 단계별 상태 확인 및 복구
✅ **이중 한글화**:
   - 1차: 태그/시리즈/스킬/어빌리티 한글화 (new3.py)
   - 2차: 캐릭터 이름 한글화 (name2korean.py, 선택)
✅ **스마트 스킵**: 
   - HTML 다운로드 실패 시 기존 파일 사용
   - 엑셀 파일 없으면 이름 한글화 건너뜀

## 트러블슈팅

### HTML 다운로드 실패
네트워크 문제로 다운로드가 안 될 경우:
1. 브라우저에서 수동 다운로드:
   - https://appmedia.jp/ggene_eternal/78594845 → `nonsp.html`
   - https://appmedia.jp/ggene_eternal/79406921 → `sp.html`
2. 파일을 현재 폴더에 넣고 다시 실행

### 이름 한글화를 건너뛰려면
`jp_names.xlsx`, `ko_names.xlsx` 없이 실행하면 자동으로 건너뜁니다.

### 파싱 오류
- HTML 구조가 변경되었을 수 있습니다
- `step2_parse.py` (new3.py) 확인 필요

### 모듈 에러
```bash
pip install -r requirements.txt
```

## URL 변경

URL을 변경하려면 `step1_download.py` 수정:

```python
# 예시
nosp_url = "https://appmedia.jp/ggene_eternal/78594845"
sp_url = "https://appmedia.jp/ggene_eternal/79406921"
```

## 업데이트

새로운 데이터로 업데이트:

```bash
python main.py
```

기존 파일을 자동으로 덮어씁니다.

## 워크플로우 비교

### 이전 (수동)
```
1. 브라우저 열기
2. URL 접속 → 저장 (×2)
3. python new3.py 실행
4. 엑셀 준비
5. python name2korean.py 실행
6. JSON → JS 변환 스크립트 실행
```

### 현재 (자동)
```
python main.py
```

**6단계 → 1단계!** 🚀

## 예상 실행 시간

- HTML 다운로드: 5-10초
- 파싱: 1-2초
- 이름 한글화: 1초 미만
- JSON → JS: 1초 미만
- **총 소요 시간: 약 10-15초**

## 라이선스
MIT License
