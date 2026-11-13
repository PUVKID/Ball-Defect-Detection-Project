<a id="-발표자료-3차--투명-로고와-자산-보존"></a>

# 발표자료 3차 · 투명 로고와 자산 보존

2차의 20장 내용·시간을 유지하면서 투명 학교 마크와 전달 자산의 일치를 보강한 단계입니다.

분야: 연구 발표 › 필터 비교의 전달 구성 › 슬라이드·발화·차트·자산

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

현재 발표 첨부는 완성된 최종 20장 PDF/PPTX로 연결합니다. 해당 차수에서 슬라이드 분할·발화 시간·자산의 무엇이 바뀌었는지는 기존 전체 비교와 도구에서 확인할 수 있습니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

| 구성 | 실제 역할 |
| --- | --- |
| 내용 유지 | 2·3차 content.json은 같은 바이트여서 발화 내용·시간 배정은 유지됩니다. |
| 자산 점검 | RGBA 투명 로고·동봉 PNG/SVG/원본 AI와 입력 보존을 대조하는 조건을 추가합니다. |
| 원정밀도 차트 | 검사기는 JSON 수치와 PPTX 차트의 15유효자리 및 1·2자리 표시를 대조합니다. |
| 발화 대응 | 슬라이드 노트와 대본에 같은 발화문이 있는지 확인하는 경로를 포함합니다. |

<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 원고·결과표 | 슬라이드의 연구 이야기 구성 | 발표 흐름 |
| 슬라이드별 발화·차트 | 시간·원정밀도·노트 대응 | 발표와 대본 |
| 로고·예시 사진 | 배치와 동봉 자산 확인 | 전달할 발표 자료 |

<a name="files"></a>

<a id="-파일과-핵심-처리"></a>

## 파일별 역할

| 파일 | 이용 방법 |
| --- | --- |
| [발표자료/3차/tools/check_presentation.py](../../%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/3%EC%B0%A8/tools/check_presentation.py) | 처리 함수와 실행 조건 |
| [발표자료/최종/추계학술대회_10분발표.pdf](../../%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/%EC%B5%9C%EC%A2%85/%EC%B6%94%EA%B3%84%ED%95%99%EC%88%A0%EB%8C%80%ED%9A%8C_10%EB%B6%84%EB%B0%9C%ED%91%9C.pdf) | 전체 원문·도표 읽기 |
| [발표자료/최종/추계학술대회_10분발표.pptx](../../%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/%EC%B5%9C%EC%A2%85/%EC%B6%94%EA%B3%84%ED%95%99%EC%88%A0%EB%8C%80%ED%9A%8C_10%EB%B6%84%EB%B0%9C%ED%91%9C.pptx) | 발표 편집 원본 |

<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

| 파일 | 핵심 정의 |
| --- | --- |
| [발표자료/3차/tools/check_presentation.py](../../%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/3%EC%B0%A8/tools/check_presentation.py) | 소스: `check` · `read_json` |

<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 읽기 도구 | PDF 뷰어·PowerPoint 호환 프로그램 |
| 검사 도구 | Python·Pillow·PPTX ZIP/XML |
| 입력 조건 | content/data·원자료·차트·사진 manifest와 발표 파일 |

<a name="usage"></a>

<a id="-읽고-활용하는-순서"></a>

## 원고 읽기

1. 이 차수의 변경 설명을 읽고 현재 최종 PDF에서 대응되는 발표 흐름을 봅니다.
2. 도입·방법·필터 비교·잡음·한계가 어떤 순서로 전달되는지 확인합니다.
3. PPTX 노트와 완성 대본의 장별 발화를 확인합니다.
4. 검사 도구를 이용하려면 입력 JSON·원자료·발표 파일의 경로를 먼저 준비합니다.

<a name="results"></a>

<a id="-결과를-읽는-방법"></a>

## 결과와 해석

600초는 슬라이드에 배정한 목표 시간입니다. 실제 발화 시간이나 발표 평가 점수를 뜻하지 않으므로 리허설에서 확인합니다.

원정밀도 결과와 표시용 차트, 논문에 보고한 범위를 함께 읽습니다. 슬라이드 수가 늘었다고 새 연구 실험이 추가된 것은 아닙니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

| 상황 | 확인할 내용 |
| --- | --- |
| 현재 첨부 | 이전 발표 사본을 중복 첨부하지 않고 최종 발표로 연결합니다. |
| 도구 입력 | 공개 검사기 외에 그 차수의 content/data·근거 JSON 등이 필요합니다. |
| 수치 해석 | Strict Acc와 mAP, 일반·잡음·반복 결과를 구분합니다. |

<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

2차에서 연구 결과·발화 내용은 유지하고 투명 로고·자산·이전 입력 보존 조건을 보강했습니다.

[직전 단계 전체 비교·구성](../revision-diffs/talk-3.diff) · [전체 파일 크기·해시](../revision-manifests/talk-3.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 표는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| `발표자료/3차/추계학술대회_10분발표.pdf` | .pdf | 4071884 | `2c418f9bea55f538b0fe94c1c6b5f0b6ef9ceaebf17fffa8c9ae540f3e9d802c` |
| `발표자료/3차/추계학술대회_10분발표.pptx` | .pptx | 22926957 | `45d6582f1f77fde70fea519d2dd573f3aec03b4c78f09388da8b46732900441a` |
| [원본작업자료/발표자료/3차/work/assemble_builder.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/3%EC%B0%A8/work/assemble_builder.py) | .py | 6090 | `c1ee20bd63cc4dd1ac89d63f709d5cb05dbebf79a8fc2733e5a40293741f592d` |
| [원본작업자료/발표자료/3차/work/build_presentation.mjs](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/3%EC%B0%A8/work/build_presentation.mjs) | .mjs | 20386 | `7be42c491627147dcfea30e4d1e115e1d258895169e85c04786f87290081e0c0` |
| `원본작업자료/발표자료/3차/work/candidate.pptx` | .pptx | 23610412 | `6755b1005934faf9246443502523ffd0dcb176f19643b29c543a0e6987d20146` |
| [원본작업자료/발표자료/3차/work/design_revision.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/3%EC%B0%A8/work/design_revision.py) | .py | 9921 | `dbaf1a66f8070bd35ec9f33056d8d2dd3cc7a62a529e2771af97de860b153367` |
| [원본작업자료/발표자료/3차/work/prepare_content.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/3%EC%B0%A8/work/prepare_content.py) | .py | 16058 | `ba1f5e520953ac71ceba0cab26a539d219f25de244c17c5ccb7dd11054227fb7` |
| [원본작업자료/발표자료/3차/work/prepare_revision.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/3%EC%B0%A8/work/prepare_revision.py) | .py | 13761 | `9f956dd067bf1d08cc6ad4bce285c00bc561cb7d69334aa49ec524cd83965a6a` |

</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/3%EC%B0%A8) · [발표자료 2차](talk-2.md) · [발표자료 4차](talk-4.md) · [발표자료 최종](talk-final.md)
