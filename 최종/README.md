<a id="-최종"></a>

# 최종

<!-- reading-levels17:start -->
**읽기 수준 선택** · [LEVEL 1 - Beginner](../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [LEVEL 2 - Explorer](../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [LEVEL 3 - Practitioner](../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [LEVEL 4 - Advanced](../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [LEVEL 5 - Expert](../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)
<!-- reading-levels17:end -->

**유사 영상 그룹과 교차검증을 구성하고 전처리 필터별 YOLO 검출, 볼 일치, 영역별 개수 판정과 추가 진단을 함께 계산하는 노트북입니다.**

<a id="layout18-table-1-row-1"></a>

**자료 점검**

**주요 구성**

자료 점검

**내용**

라벨·클래스 균형·128크기 축소영상의 평균 절대 차이 기반 유사 그룹을 점검합니다.

<a id="layout18-table-1-row-2"></a>

**영역 규칙**

**주요 구성**

영역 규칙

**내용**

부품 사각형 내부의 볼 중심을 위 5·왼쪽 4·아래 2·오른쪽 2 규칙에 맞춰 판정합니다.

<a id="layout18-table-1-row-3"></a>

**외부 fold**

**주요 구성**

외부 fold

**내용**

assign_folds가 유사 그룹을 같은 외부 fold에 두고 fold_split은 남은 영상에서 내부 검증을 나눕니다.

<a id="layout18-table-1-row-4"></a>

**검출 품질**

**주요 구성**

검출 품질

**내용**

ball_match_stats는 라벨 크기의 0.5배 중심 허용거리로 일대일 매칭하고 누락·추가 검출을 셉니다.

<a id="layout18-table-1-row-5"></a>

**필터 실험**

**주요 구성**

필터 실험

**내용**

train_per_filter·inference_only 모드와 결과 서명 기반 캐시를 구분합니다.


<a id="-이용-순서"></a>

## 이용 순서

1. 노트북의 설정·데이터 로드·라벨 점검 셀을 읽고 입력 경로를 준비합니다.
2. DO_TRAIN·TRAINED_WEIGHTS·FILTER_MODE·USE_CV·RUN_PRESET를 실행 목적에 맞게 확인합니다.
3. GPU 모니터·학습·출력 경로와 데이터 생성/복사 셀을 확인한 뒤 필요한 구간만 실행합니다.
4. 조건별 결과표에서 분모·fold·캐시 서명을 확인하고 mAP와 Strict Acc를 따로 봅니다.
5. 독립 OK/NG 정답 목록이 있다면 OKNG_CSV 경로와 라벨 대응을 따로 확인합니다.

| 차수·단계 · 주요 내용 · 자료 · 직전 비교 |
| --- |
| **차수·단계**<br>[최종](../docs/revisions/code-final.md)<br><br>**주요 내용**<br>[상세 설명](#layout18-table-2-row-1-field-1)<br><br>**자료**<br>[폴더](.)<br><br>**직전 비교**<br>[전체 비교](../docs/revision-diffs/code-final.diff) |

<a id="layout18-table-2-row-1-field-1"></a>

**[최종](../docs/revisions/code-final.md)**

**주요 내용**

유사 영상 그룹과 교차검증을 구성하고 전처리 필터별 YOLO 검출, 볼 일치, 영역별 개수 판정과 추가 진단을 함께 계산하는 노트북입니다.


[프로젝트](../README.md) · [전체 차수](../docs/REVISION_INDEX.md)
