# 청렴 신고 사건 조회 페이지

행안부 청렴감사관실 공개용 정적 웹페이지와 CSV 자동 요약 도구입니다.

## 포함 파일

- `index.html`
- `style.css`
- `app.js`
- `data.json`
- `vercel.json`
- `build_assets.py`

## 기능

- 청렴 신고 사건 카드 조회
- `신고유형`, `처리상태` 필터
- `결과N건` 표시
- 청렴 교육 현황 요약
- 행안부 보도자료 RSS 표시

## 데이터 생성

CSV 원본을 바탕으로 아래 파일을 생성합니다.

```bash
python build_assets.py
```

생성 결과:

- `data.json`
- `summary.json`
- `summary.csv`

## 배포

Vercel 또는 GitHub Pages에 올려서 바로 서비스할 수 있습니다.

