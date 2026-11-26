<!-- language-choice:start -->
🔵 **한국어** · [English overview](../../../en/README.md)
<!-- language-choice:end -->

<a id="-논문4차tools"></a>

# 논문/4차/tools

<!-- reading-levels17:start -->
<details>
<summary>읽기 수준 선택</summary>

| 레벨 | 읽는 목적 |
| --- | --- |
| [LEVEL 1 - Beginner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) | 목적과 입력·출력을 쉬운 말로 이해하기 |
| [LEVEL 2 - Explorer](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) | 주요 기능과 전체 처리 흐름 살펴보기 |
| [LEVEL 3 - Practitioner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) | 설정·실행 순서와 결과 확인하기 |
| [LEVEL 4 - Advanced](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) | 구현 선택과 조건·한계 비교하기 |
| [LEVEL 5 - Expert](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md) | 세부 근거와 재현 조건 검토하기 |

</details>
<!-- reading-levels17:end -->

새 모델을 학습하는 대신 원고의 표·그림·문장과 저장된 원정밀도 결과를 대조한 검토 도구 단계입니다.

| 주요 구성 | 내용 |
| --- | --- |
| <a id="layout18-table-1-row-1"></a> 원문 결합 | 원고 SHA와 입력·근거 파일 해시를 대조합니다. |
| <a id="layout18-table-1-row-2"></a> 결과 계산 | 단일 16 조건 8000 행·반복 39 조건 19500 행의 영상별 결과를 집계하는 조건이 있습니다. |
| <a id="layout18-table-1-row-3"></a> 분할 점검 | 500 영상·368 유사 그룹·154 유사 쌍, 외부 중복 0 과 내부 9~20 그룹 중복을 확인하는 조건을 포함합니다. |
| <a id="layout18-table-1-row-4"></a> 표시·서술 | 이중 반올림, HWP 그림 해상도, 인용·사사·원고 문장을 대조합니다. |


<a id="-이용-순서"></a>

## 이용 순서

1. check_review.py의 ROOT와 처음 읽는 입력 목록을 확인합니다.
2. 원고·영상별 결과·근거 JSON을 같은 기록에 맞게 준비합니다.
3. 검사 조건에서 결과 계산·분할 중복·표시 차이를 각각 구분해 읽습니다.
4. 공개 도구에 없는 원본 근거를 준비하지 않은 상태에서는 전체 점검을 실행한 결과로 간주하지 않습니다.

| 차수·단계 | 주요 내용 | 자료 | 직전 비교 |
| --- | --- | --- | --- |
| [논문 4차 · 검토 도구](../../../docs/revisions/paper-4.md) | <a id="layout18-table-2-row-1-field-1"></a>새 모델을 학습하는 대신 원고의 표·그림·문장과 저장된 원정밀도 결과를 대조한 검토 도구 단계입니다. | [폴더](.) | [전체 비교](../../../docs/revision-diffs/paper-4-%EC%97%B4%EB%9E%8C.md) |


[프로젝트](../../../README.md) · [전체 차수](../../../docs/REVISION_INDEX.md)
