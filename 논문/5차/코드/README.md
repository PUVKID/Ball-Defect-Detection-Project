<a id="-논문5차코드"></a>

# 논문/5차/코드

<!-- reading-levels17:start -->
**읽기 수준 선택** · [LEVEL 1 - Beginner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [LEVEL 2 - Explorer](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [LEVEL 3 - Practitioner](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [LEVEL 4 - Advanced](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [LEVEL 5 - Expert](../../../docs/%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)
<!-- reading-levels17:end -->

**보존된 결과표와 노트북을 논문용 도표·참조 코드·전달 패키지로 구성한 단계입니다.** 모델을 다시 학습하는 경로와 저장 결과를 다시 그리는 경로를 분리합니다.

<a id="layout18-table-1-row-1"></a>

**논문 그림**

**주요 구성**

논문 그림

**내용**

paper_filter_figures.py가 단일·복합·잡음 CSV에서 3개 논문용 그림을 구성합니다.

<a id="layout18-table-1-row-2"></a>

**스타일 함수**

**주요 구성**

스타일 함수

**내용**

reference_plot_style.py가 글꼴·색·막대·레이블·이웃 텍스트 배치를 공통 처리합니다.

<a id="layout18-table-1-row-3"></a>

**결과 재렌더**

**주요 구성**

결과 재렌더

**내용**

render_saved_figures.py가 저장 JSON·CSV와 참조 노트북의 그림 함수를 이용합니다.

<a id="layout18-table-1-row-4"></a>

**입력 연결**

**주요 구성**

입력 연결

**내용**

재작성한 그림에 사용한 원자료 SHA를 기록하는 처리를 포함합니다.


<a id="-이용-순서"></a>

## 이용 순서

1. 각 스크립트가 읽는 CSV/JSON과 결과 폴더를 먼저 확인합니다.
2. 참조 스타일의 글꼴·레이블·색 설정과 실제 파일 경로를 준비합니다.
3. 논문용 3개 그림 또는 저장 결과 전체 재렌더 중 목적에 맞는 스크립트를 선택합니다.
4. 출력 그림의 값·조건명·표시 자릿수를 입력 표와 대조합니다.

| 차수·단계 | 주요 내용 | 자료 | 직전 비교 |
| --- | --- | --- | --- |
| [논문 5차 · 재구성 패키지](../../../docs/revisions/paper-5.md) | [상세 설명](#layout18-table-2-row-1-field-1) | [폴더](.) | [전체 비교](../../../docs/revision-diffs/paper-5.diff) |

<a id="layout18-table-2-row-1-field-1"></a>

**[논문 5차 · 재구성 패키지](../../../docs/revisions/paper-5.md)**

**주요 내용**

보존된 결과표와 노트북을 논문용 도표·참조 코드·전달 패키지로 구성한 단계입니다. 모델을 다시 학습하는 경로와 저장 결과를 다시 그리는 경로를 분리합니다.


[프로젝트](../../../README.md) · [전체 차수](../../../docs/REVISION_INDEX.md)
