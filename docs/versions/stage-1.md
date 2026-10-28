# 📚 최종 연구코드

볼 검출 필터 비교와 영역 개수 기반 OK/NG·추가 진단을 함께 보관합니다.

- [근거 자료](../../%EC%B5%9C%EC%A2%85/%EC%97%B0%EA%B5%AC%EC%BD%94%EB%93%9C/ball_ok_ng_yolo_v7.ipynb)
- [전체 보관 기록](../VERSIONS.md) · [프로젝트 소개](../../README.md)

## 🔎 범위와 해석

추가 진단이 모두 논문 실험에 포함되었다고 가정하지 않습니다.


## 🧩 구체적으로 살펴볼 내용

- 근접 중복 그룹을 찾고 fold를 배정하는 절차가 있습니다. 객체 검출과 규칙 기반 판정 실험의 범위를 나누어 읽습니다.
- ball_match_stats의 볼 일치 계산과 fold_map의 검출 mAP 집계는 같은 지표가 아닙니다. 원고의 Strict Acc와 mAP50-95를 혼용하지 않습니다.

## 🔄 앞선 자료와의 관계

루트와 최종 경로의 노트북은 동일 SHA로 확인되는 사본입니다. 경로가 둘이라고 새 실험 두 개로 세지 않습니다.

## 📍 파일 안에서 확인하기

- [최종/연구코드/ball_ok_ng_yolo_v7.ipynb](../../%EC%B5%9C%EC%A2%85/%EC%97%B0%EA%B5%AC%EC%BD%94%EB%93%9C/ball_ok_ng_yolo_v7.ipynb) · `def assign_folds` · 셀 30 소스 67행
- [최종/연구코드/ball_ok_ng_yolo_v7.ipynb](../../%EC%B5%9C%EC%A2%85/%EC%97%B0%EA%B5%AC%EC%BD%94%EB%93%9C/ball_ok_ng_yolo_v7.ipynb) · `def ball_match_stats` · 셀 30 소스 436행

셀 번호는 0부터, 소스 행 번호와 PDF 쪽 번호는 1부터 셉니다. 문서와 코드의 정적 대조이며, 새 학습·추론·장치 측정·공격 실행 결과는 아닙니다.
