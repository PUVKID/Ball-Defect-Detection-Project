# 📚 최종 연구코드

볼 검출 필터 비교와 영역 개수 기반 OK/NG·추가 진단을 함께 보관합니다.

- [근거 자료](../../%EC%B5%9C%EC%A2%85/%EC%97%B0%EA%B5%AC%EC%BD%94%EB%93%9C/ball_ok_ng_yolo_v7.ipynb)
- [전체 보관 기록](../VERSIONS.md) · [프로젝트 소개](../../README.md)

## 🔎 범위와 해석

노트북은 논문의 실험과 추가 진단을 함께 다룹니다.


## 🧩 주요 내용

- 근접 중복 그룹을 찾아 fold를 배정하고, 객체 검출과 규칙 기반 판정을 각각 평가합니다.
- ball_match_stats는 볼 일치를, fold_map은 검출 mAP를 집계합니다. 원고에서는 Strict Acc와 mAP50-95를 각각 보고합니다.

## 🔄 자료 구성

루트와 최종 경로에 동일한 노트북이 있습니다.

## 📍 관련 자료

- [최종/연구코드/ball_ok_ng_yolo_v7.ipynb](../../%EC%B5%9C%EC%A2%85/%EC%97%B0%EA%B5%AC%EC%BD%94%EB%93%9C/ball_ok_ng_yolo_v7.ipynb) · `def assign_folds` · 셀 30 소스 67행
- [최종/연구코드/ball_ok_ng_yolo_v7.ipynb](../../%EC%B5%9C%EC%A2%85/%EC%97%B0%EA%B5%AC%EC%BD%94%EB%93%9C/ball_ok_ng_yolo_v7.ipynb) · `def ball_match_stats` · 셀 30 소스 436행

셀 번호는 0부터, 소스 행 번호와 PDF 쪽 번호는 1부터 셉니다. 
