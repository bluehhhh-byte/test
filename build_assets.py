import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

DOWNLOADS = Path.home() / "Downloads"
OUT_DIR = Path(__file__).resolve().parent
REPORT_NAME = "청렴신고_사건데이터.csv"
EDU_NAME = "청렴교육_현황.csv"


def find_file(filename: str) -> Path:
    matches = list(DOWNLOADS.rglob(filename))
    if not matches:
        raise FileNotFoundError(filename)
    return matches[0]


def read_csv(path: Path):
    for encoding in ("utf-8-sig", "cp949", "euc-kr"):
        try:
            with path.open("r", encoding=encoding, newline="") as f:
                return list(csv.DictReader(f))
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("csv", b"", 0, 1, f"Unable to decode {path}")


def to_int(value):
    try:
        return int(float(value)) if value not in (None, "") else None
    except ValueError:
        return None


def to_float(value):
    try:
        return float(value) if value not in (None, "") else None
    except ValueError:
        return None


def main():
    report_path = find_file(REPORT_NAME)
    edu_path = find_file(EDU_NAME)

    reports = []
    for row in read_csv(report_path):
        reports.append(
            {
                "사건ID": row.get("사건ID", ""),
                "신고일자": row.get("신고일자", ""),
                "신고유형": row.get("신고유형", ""),
                "지역": row.get("지역", ""),
                "신고자유형": row.get("신고자유형", ""),
                "처리상태": row.get("처리상태", ""),
                "처리기간_일": to_int(row.get("처리기간_일")),
                "위반금액_만원": to_int(row.get("위반금액_만원")),
                "조치결과": row.get("조치결과", ""),
            }
        )

    education = []
    for row in read_csv(edu_path):
        education.append(
            {
                "기관코드": row.get("기관코드", ""),
                "기관명": row.get("기관명", ""),
                "기관유형": row.get("기관유형", ""),
                "교육이수율": to_float(row.get("교육이수율")),
                "연간교육시간": to_int(row.get("연간교육시간")),
                "교육참여자수": to_int(row.get("교육참여자수")),
                "청렴우수기관": row.get("청렴우수기관", ""),
            }
        )

    reports.sort(key=lambda r: r["신고일자"], reverse=True)

    type_counts = Counter(r["신고유형"] for r in reports)
    status_counts = Counter(r["처리상태"] for r in reports)
    region_counts = Counter(r["지역"] for r in reports)
    valid_rates = [r["교육이수율"] for r in education if r["교육이수율"] is not None]

    summary = {
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "report": {
            "totalCases": len(reports),
            "typeCounts": dict(type_counts),
            "statusCounts": dict(status_counts),
            "regionCounts": dict(region_counts),
            "latestDate": max((r["신고일자"] for r in reports if r["신고일자"]), default=""),
        },
        "education": {
            "totalInstitutions": len(education),
            "averageCompletionRate": round(sum(valid_rates) / len(valid_rates), 1) if valid_rates else None,
            "excellentInstitutions": sum(1 for row in education if row["청렴우수기관"] == "Y"),
        },
    }

    (OUT_DIR / "data.json").write_text(
        json.dumps({"reports": reports, "education": education}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUT_DIR / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    with (OUT_DIR / "summary.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["구분", "항목", "값"])
        writer.writerow(["청렴신고", "총건수", summary["report"]["totalCases"]])
        writer.writerow(["청렴신고", "최신신고일", summary["report"]["latestDate"]])
        writer.writerow(["청렴교육", "기관수", summary["education"]["totalInstitutions"]])
        writer.writerow(["청렴교육", "평균교육이수율", summary["education"]["averageCompletionRate"]])
        writer.writerow(["청렴교육", "우수기관수", summary["education"]["excellentInstitutions"]])

    print("WROTE data.json, summary.json, summary.csv")


if __name__ == "__main__":
    main()
