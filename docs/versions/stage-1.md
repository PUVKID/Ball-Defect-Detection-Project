<!-- language-choice:start -->
🔵 **한국어** · [English overview](../../en/README.md)
<!-- language-choice:end -->

<a id="-최종-연구코드"></a>

# 최종 연구코드

<!-- reading-levels17:start -->
<details>
<summary>읽기 수준 선택</summary>

| 레벨 | 읽는 목적 |
| --- | --- |
| [LEVEL 1 - Beginner](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) | 목적과 입력·출력을 쉬운 말로 이해하기 |
| [LEVEL 2 - Explorer](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) | 주요 기능과 전체 처리 흐름 살펴보기 |
| [LEVEL 3 - Practitioner](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) | 설정·실행 순서와 결과 확인하기 |
| [LEVEL 4 - Advanced](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) | 구현 선택과 조건·한계 비교하기 |
| [LEVEL 5 - Expert](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md) | 세부 근거와 재현 조건 검토하기 |

</details>
<!-- reading-levels17:end -->

유사 영상 그룹과 교차검증을 구성하고 전처리 필터별 YOLO 검출, 볼 일치, 영역별 개수 판정과 추가 진단을 함께 계산하는 노트북입니다.

[목적·구성·사용법·결과의 상세 안내](../revisions/code-final.md) · [프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md)

<a id="-이-자료를-읽는-순서"></a>

## 이 자료를 읽는 순서

1. 노트북의 설정·데이터 로드·라벨 점검 셀을 읽고 입력 경로를 준비합니다.
2. DO_TRAIN·TRAINED_WEIGHTS·FILTER_MODE·USE_CV·RUN_PRESET를 실행 목적에 맞게 확인합니다.
3. GPU 모니터·학습·출력 경로와 데이터 생성/복사 셀을 확인한 뒤 필요한 구간만 실행합니다.
4. 조건별 결과 표에서 분모·fold·캐시 서명을 확인하고 mAP와 Strict Acc를 따로 봅니다.
5. 독립 OK/NG 정답 목록이 있다면 OKNG_CSV 경로와 라벨 대응을 따로 확인합니다.

<a id="-연결된-내용"></a>

## 연결된 내용

| 구성 | 읽을 내용 |
| --- | --- |
| <a id="layout18-table-1-row-1"></a> 자료 점검 | 라벨·클래스 균형·128 크기 축소 영상의 평균 절대 차이 기반 유사 그룹을 점검합니다. |
| <a id="layout18-table-1-row-2"></a> 영역 규칙 | 부품 사각형 내부의 볼 중심을 위 5·왼쪽 4·아래 2·오른쪽 2 규칙에 맞춰 판정합니다. |
| <a id="layout18-table-1-row-3"></a> 외부 fold | assign_folds가 유사 그룹을 같은 외부 fold에 두고 fold_split은 남은 영상에서 내부 검증을 나눕니다. |
| <a id="layout18-table-1-row-4"></a> 검출 품질 | ball_match_stats는 라벨 크기의 0.5 배 중심 허용 거리로 일대일 매칭하고 누락·추가 검출을 셉니다. |
| <a id="layout18-table-1-row-5"></a> 필터 실험 | train_per_filter·inference_only 모드와 결과 서명 기반 캐시를 구분합니다. |


<a id="-해석-범위"></a>

## 해석 범위

Strict Acc는 모든 라벨 볼을 중심 거리 기준으로 찾고 추가 검출이 없는 영상 비율입니다.  
fold_map은 model.val의 held-out test에서 mAP50·mAP50-95를 별도로 계산합니다.

[전체 설명으로 이동](../revisions/code-final.md)
