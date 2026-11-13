<a id="-논문-4차--원고-수치와-근거를-대조하는-도구"></a>

# 논문 4차 · 원고 수치와 근거를 대조하는 도구

새 모델을 학습하는 대신 원고의 표·그림·문장과 저장된 원정밀도 결과를 대조한 검토 도구 단계입니다.

분야: 연구 보조 도구 › 원고·결과 대조 › JSON·CSV·수치·표현 검사

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

check_review.py는 10개 항목과 원고·결과 자료의 해시, 단일·반복 결과의 지표, 분할 중복과 그림의 표시 정밀도 등을 확인합니다. 도구의 조건을 만족하는 것과 논문 제출·성능을 승인하는 것은 구분합니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

| 구성 | 실제 역할 |
| --- | --- |
| 원문 결합 | 원고 SHA와 입력·근거 파일 해시를 대조합니다. |
| 결과 계산 | 단일 16조건 8000행·반복 39조건 19500행의 영상별 결과를 집계하는 조건이 있습니다. |
| 분할 점검 | 500영상·368유사그룹·154유사쌍, 외부 중복 0과 내부 9~20그룹 중복을 확인하는 조건을 포함합니다. |
| 표시·서술 | 이중 반올림, HWP 그림 해상도, 인용·사사·원고 문장을 대조합니다. |

<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 원고·결과·점검 JSON | 해시와 항목 구성 확인 | 근거가 연결된 점검 항목 |
| 영상별 CSV | 지표·평균·표준편차 재계산 | 원고 표와 원정밀도 차이 |
| 그림·서술 | 표시·해상도·문장 대조 | 주의·수정 필요·확인 범위 |

<a name="files"></a>

<a id="-파일과-핵심-처리"></a>

## 파일별 역할

| 파일 | 이용 방법 |
| --- | --- |
| [논문/4차/tools/check_review.py](../../%EB%85%BC%EB%AC%B8/4%EC%B0%A8/tools/check_review.py) | 처리 함수와 실행 조건 |
| [논문/최종_논문.pdf](../../%EB%85%BC%EB%AC%B8/%EC%B5%9C%EC%A2%85_%EB%85%BC%EB%AC%B8.pdf) | 전체 원문·도표 읽기 |

<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

| 파일 | 핵심 정의 |
| --- | --- |
| [논문/4차/tools/check_review.py](../../%EB%85%BC%EB%AC%B8/4%EC%B0%A8/tools/check_review.py) | 소스: `rows` |

<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 도구 | Python·NumPy와 CSV/JSON |
| 입력 | audit.json·원고·결과 CSV·recalculated·container_dataset·main_findings 등 |
| 역할 | 입력 자료의 근거와 완결성을 대조 |

<a name="usage"></a>

<a id="-준비와-사용-순서"></a>

## 실행 순서

1. check_review.py의 ROOT와 처음 읽는 입력 목록을 확인합니다.
2. 원고·영상별 결과·근거 JSON을 같은 기록에 맞게 준비합니다.
3. 검사 조건에서 결과 계산·분할 중복·표시 차이를 각각 구분해 읽습니다.
4. 공개 도구에 없는 원본 근거를 준비하지 않은 상태에서는 전체 점검을 실행한 결과로 간주하지 않습니다.

<a name="results"></a>

<a id="-결과를-읽는-방법"></a>

## 결과와 해석

도구는 paper_ready_for_submission=False를 요구하며 PASS·주의·수정필요·확인불가 상태를 구분합니다. 도구가 보존됐다는 사실만으로 원고가 수정됐거나 새 시험이 완료됐다고 보지 않습니다.

특히 원고 그림의 이중 반올림과 HWP 내장 그림 약 96dpi, 전체 문서 렌더 확인 범위가 별도 항목으로 연결됩니다. 이 단계의 발견과 현재 원고의 상태는 직전 비교와 함께 읽습니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

| 상황 | 확인할 내용 |
| --- | --- |
| 의존 자료 | 스크립트 외의 audit·근거 JSON·원고·결과 원자료가 필요합니다. |
| 평가 누수 | 외부 그룹 분리와 내부 train/val 그룹 중복을 별개로 확인합니다. |
| 원고 보존 | 발견한 차이를 숨기거나 원고 숫자를 임의 수정하는 도구가 아닙니다. |

<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

3차/최종 원고와 실험 근거를 대조한 단계입니다. 새 원고·모델 학습이 아니라 수치·표현·그림 조건을 점검하는 기능으로 구분합니다.

[직전 단계 전체 비교·구성](../revision-diffs/paper-4.diff) · [전체 파일 크기·해시](../revision-manifests/paper-4.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 표는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [논문/4차/tools/check_review.py](../../%EB%85%BC%EB%AC%B8/4%EC%B0%A8/tools/check_review.py) | .py | 9435 | `4279a2748567df1bbc899cb17ae2673df9d8912748e78d465a9d254e3c117d3c` |
| [원본작업자료/논문/4차/work/main_layout_inspect.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/main_layout_inspect.py) | .py | 4217 | `b2507d2b88667f60dc0f99346f0037d76c989869f2ada7025f91a88ffda2f033` |
| [원본작업자료/논문/4차/work/evidence/build_audit_report.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/build_audit_report.py) | .py | 22369 | `54e83b637fbd994d4a0c88fd07dd46b448f79be6035d212c11af2a3a7abad1bc` |
| [원본작업자료/논문/4차/work/evidence/check_metrics_code.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/check_metrics_code.py) | .py | 2309 | `8272fc359a85f9498fc864f24b7a3a0307159b6d3e663543f1defcdbc969a154` |
| [원본작업자료/논문/4차/work/evidence/container_readonly.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/container_readonly.py) | .py | 2729 | `5f5f3de67bfb7d09485107c31352690427e73edc2979a5edf2be1f33e1bef422` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_01.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_01.py) | .py | 4127 | `4fa0dc8d1cfcb958a5090aed8f4845f05e5ad794cd3a7fe8b67c0d43988517a9` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_03.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_03.py) | .py | 1394 | `c54f67171b17d961b7789eb9eafe0a2494ab6804cbe5adf871932324b873f71e` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_04.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_04.py) | .py | 3647 | `d29046dbe5639d8cf54380c6fd7d9729929f21144baff979d111b8df2176e3a2` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_06.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_06.py) | .py | 2739 | `c4829d3da01e92090bf37d978adca14b31f92895d06f4ae8ce7df9b9d4186149` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_08.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_08.py) | .py | 3789 | `ff6e52dac5030eeec279c0d8078aed6219345aa2c46eb79b07fb9676d7e2da73` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_10.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_10.py) | .py | 1188 | `8676e423e0b658be4a5699dd7ad9b037e5b51cd6ddf289f223aa9b44020a727f` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_12.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_12.py) | .py | 1322 | `3f37601042220db3b6b944b7688a0427ebdead07c328d7011dbb033b40f4c004` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_14.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_14.py) | .py | 4129 | `41df59dcdd1690890c85244532477d81d4455172318060fc3d545a1a31d34222` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_16.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_16.py) | .py | 4152 | `ac33bc5c969feb669ad2a2bf725803bd44ba451b1b189fc02fa0b3bd37ad2840` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_18.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_18.py) | .py | 3399 | `da1fa465e55b5b8a53eab83c53b5dcaf2d1105dc6c99add9534738304e7a2d9b` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_20.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_20.py) | .py | 3218 | `8da48e2214d853593639d0efc9a1106611ed82bb7d823594a1de3b6d8ad9b3de` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_22.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_22.py) | .py | 1521 | `85af7852c25f6b6dc67b0a8933ee5cac5e31480d7f31b426d729df58967b997c` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_24.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_24.py) | .py | 2009 | `5cbae2d11991a6e930068bece2f1ebb8a129a739b75b61b1f2cdcf1d5c247ad1` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_26.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_26.py) | .py | 4528 | `7c4ab9835d97cbe1d0d6f97f8f6e2e2b3c382b4caf17426dd88a34853405320d` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_28.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_28.py) | .py | 1811 | `4dec7aa81995939d0bcb0b2185bd6b324bc3850fb587ccb2a48e656450bf6dea` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_30.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_30.py) | .py | 36779 | `4a84a56cb7fceb2309b2732f08b8abe2a9dc169218e2c4a05867b76b22fe6299` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_32.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_32.py) | .py | 6213 | `37c420449e4170701dec73f875498021e11fa42e545b9d9917358c23207ca4dd` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_34.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_34.py) | .py | 8950 | `ab1815b25b625b1e4f4d8f22929573b3589289b1df413eb1dceacde82bb21078` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_36.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_36.py) | .py | 835 | `3f645ba36af67a6b7335243937d216cc030fe52a33853804b5a045a3b73f06d6` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_38.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_38.py) | .py | 203 | `2c5c22b47b8749d258438928847d54db7a0a174fbb82802cfd6902764e740c09` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_40.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_40.py) | .py | 245 | `044cdda32def1c8e7d3a18822cb522c0cd01a1b15298f17eb3afb2006bd2408d` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_42.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_42.py) | .py | 205 | `f4c07a5f31400a3223aa6fb91f852d9f5f8cfb65800eec2bd0476e9d50d4d85b` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_44.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_44.py) | .py | 245 | `d4d8b750340802aee40b09aa9a75e50c2dd648709f7bac925281bbd62c48354a` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_46.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_46.py) | .py | 4058 | `8d116612c8a7ba101f5bf97dc1693873eadc28b2c7448536da4857dec67fd7b3` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_48.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_48.py) | .py | 4674 | `675d3c3f2db513fe76b703b69f90872b30466d753cfa4262669f4dc462675e5b` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_51.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_51.py) | .py | 5135 | `39340c112c5cec0194f3483f33e1883219402f3938dcd56ce7f966c6544c05ac` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_53.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_53.py) | .py | 1725 | `5f9560f2449fe4b27505052c1c13dae62edbc1e35ac43e06075b3ba893b4fa6c` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_55.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_55.py) | .py | 20559 | `7088eab66a8164ad32d035d04a836b7b50769cba849994652dc268999b86454d` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_57.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_57.py) | .py | 13286 | `aacf9ef4b13e381b26209eb34312d0f57253aea7c2583e4f6d76a20440c2e951` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_58.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_58.py) | .py | 4850 | `38708a830269e0ca457f3de440b604c8fbd077333b43ad79ba80d42f27ad18fb` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_60.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_60.py) | .py | 1582 | `3f48d1454fe9aa108147423dc3eaaf4bee1818b34d44e199cdaaaf689fac5488` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_61.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_61.py) | .py | 3600 | `434a431747e347ad662c4bf073cc35600dc98f9dc413a02098eb32c66facc28b` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_62.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_62.py) | .py | 2448 | `cd50df02812b63164971c80e45b78ac36c980dc11c7f32b4f8eeb7bbf6682daa` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_63.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_63.py) | .py | 1186 | `5809532940e18bea66694e5a8024522e231bc84b14b7bb24bb78c485fa54dc23` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_65.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_65.py) | .py | 6754 | `7e4054e2cdbc015db2cb7f4b0a11ef3b305e3c80d377a9a5eb51fcec008ba200` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_66.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_66.py) | .py | 7285 | `6326593ba272c497a9fde4fa7fbc61e31fc3d5e6233aec392a2d579fec0f6f03` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_67.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_67.py) | .py | 3810 | `96486facb829716afded68960720255f6523b49837a76e4171ec3427d497b38c` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_69.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_69.py) | .py | 7373 | `ac3d5bb06e21ab6151ea971944e379f0d3a9398285b2bde4e36bf08262c54468` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_71.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_71.py) | .py | 7174 | `734baffa5896f5a5a4ac631a59140d1613a046c424e95658ae56462a854a443e` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_72.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_72.py) | .py | 5431 | `01e694b71e8f78660fde6bae5ddde1fb72978e89278eee0c5963d05518eab216` |
| [원본작업자료/논문/4차/work/evidence/notebook_cell_74.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_74.py) | .py | 3086 | `ecb09c737b469bd66b9688531f22db44f699907a32473576854f46af11257bfd` |
| [원본작업자료/논문/4차/work/evidence/recompute_saved.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/recompute_saved.py) | .py | 8308 | `5b8ef5c8e768941c813d95d83b523a9908284e977930be476bc33790dfb82f83` |

</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EB%85%BC%EB%AC%B8/4%EC%B0%A8/tools) · [논문 3차](paper-3.md) · [논문 5차 · 재구성 패키지](paper-5.md)
