<a id="-논문4차tools"></a>

# 논문/4차/tools

<!-- reading-levels17:start -->
**읽기 수준 선택** · [LEVEL 1 - Beginner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [LEVEL 2 - Explorer](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [LEVEL 3 - Practitioner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [LEVEL 4 - Advanced](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [LEVEL 5 - Expert](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)
<!-- reading-levels17:end -->

**새 모델을 학습하는 대신 원고의 표·그림·문장과 저장된 원정밀도 결과를 대조한 검토 도구 단계입니다.**

<a id="layout18-table-1-row-1"></a>

**원문 결합**

**주요 구성**

원문 결합

**내용**

원고 SHA와 입력·근거 파일 해시를 대조합니다.

<a id="layout18-table-1-row-2"></a>

**결과 계산**

**주요 구성**

결과 계산

**내용**

단일 16조건 8000행·반복 39조건 19500행의 영상별 결과를 집계하는 조건이 있습니다.

<a id="layout18-table-1-row-3"></a>

**분할 점검**

**주요 구성**

분할 점검

**내용**

500영상·368유사그룹·154유사쌍, 외부 중복 0과 내부 9~20그룹 중복을 확인하는 조건을 포함합니다.

<a id="layout18-table-1-row-4"></a>

**표시·서술**

**주요 구성**

표시·서술

**내용**

이중 반올림, HWP 그림 해상도, 인용·사사·원고 문장을 대조합니다.


<a id="-이용-순서"></a>

## 이용 순서

1. check_review.py의 ROOT와 처음 읽는 입력 목록을 확인합니다.
2. 원고·영상별 결과·근거 JSON을 같은 기록에 맞게 준비합니다.
3. 검사 조건에서 결과 계산·분할 중복·표시 차이를 각각 구분해 읽습니다.
4. 공개 도구에 없는 원본 근거를 준비하지 않은 상태에서는 전체 점검을 실행한 결과로 간주하지 않습니다.

| 차수·단계 · 주요 내용 · 자료 · 직전 비교 |
| --- |
| **차수·단계**<br>[논문 4차 · 검토 도구](../../../docs/revisions/paper-4.md)<br><br>**주요 내용**<br>[상세 설명](#layout18-table-2-row-1-field-1)<br><br>**자료**<br>[폴더](.)<br><br>**직전 비교**<br>[전체 비교](../../../docs/revision-diffs/paper-4.diff) |

<a id="layout18-table-2-row-1-field-1"></a>

**[논문 4차 · 검토 도구](../../../docs/revisions/paper-4.md)**

**주요 내용**

새 모델을 학습하는 대신 원고의 표·그림·문장과 저장된 원정밀도 결과를 대조한 검토 도구 단계입니다.


[프로젝트](../../../README.md) · [전체 차수](../../../docs/REVISION_INDEX.md)
