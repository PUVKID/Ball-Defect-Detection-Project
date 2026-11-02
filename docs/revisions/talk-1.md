<div align="center">

# 🎤 발표자료 1차 · 12장 본발표와 3장 부록

**필터 비교 연구를 12장 본발표 600초와 3장 부록으로 설명한 초기 발표 구성입니다.**

**기술 분류:** 연구 발표 › 필터 비교의 전달 구성 › 슬라이드·발화·차트·자산

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

</div>

<a name="purpose"></a>

## 🎯 이 단계에서 하는 일

현재 발표 첨부는 완성된 최종 20장 PDF/PPTX로 연결합니다. 해당 차수에서 슬라이드 분할·발화 시간·자산의 무엇이 바뀌었는지는 기존 전체 비교와 도구에서 확인할 수 있습니다.

<a name="features"></a>

## 🧩 주요 기능과 처리 방식

| 구성 | 실제 역할 |
| --- | --- |
| 연구 이야기 | 자료·그룹 평가→필터→mAP/Strict Acc→잡음·시드→한계 순서로 설명합니다. |
| 발표 분량 | 검사기는 15장, 앞 12장 시간 합계 600초와 부록 0초를 확인합니다. |
| 원정밀도 차트 | 검사기는 JSON 수치와 PPTX 차트의 15유효자리 및 1·2자리 표시를 대조합니다. |
| 발화 대응 | 슬라이드 노트와 대본에 같은 발화문이 있는지 확인하는 경로를 포함합니다. |

<a name="flow"></a>

## 🔄 입력 → 처리 → 출력

| 입력 | 처리 | 출력·읽을 결과 |
| --- | --- | --- |
| 원고·결과표 | 슬라이드의 연구 이야기 구성 | 발표 흐름 |
| 슬라이드별 발화·차트 | 시간·원정밀도·노트 대응 | 발표와 대본 |
| 로고·예시 사진 | 배치와 동봉 자산 확인 | 전달할 발표 자료 |

<a name="files"></a>

## 📁 파일과 핵심 처리

| 파일 | 이용 방법 |
| --- | --- |
| [발표자료/1차/tools/check_presentation.py](../../%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/1%EC%B0%A8/tools/check_presentation.py) | 처리 함수와 실행 조건 |
| [발표자료/최종/추계학술대회_10분발표.pdf](../../%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/%EC%B5%9C%EC%A2%85/%EC%B6%94%EA%B3%84%ED%95%99%EC%88%A0%EB%8C%80%ED%9A%8C_10%EB%B6%84%EB%B0%9C%ED%91%9C.pdf) | 전체 원문·도표 읽기 |
| [발표자료/최종/추계학술대회_10분발표.pptx](../../%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/%EC%B5%9C%EC%A2%85/%EC%B6%94%EA%B3%84%ED%95%99%EC%88%A0%EB%8C%80%ED%9A%8C_10%EB%B6%84%EB%B0%9C%ED%91%9C.pptx) | 발표 편집 원본 |

### 🔎 함수·셀로 찾아가기

아래 이름은 해당 파일의 실제 정의입니다. 위 처리 설명과 함께 설정·호출 순서·출력 경로를 따라 읽습니다.

| 파일 | 핵심 정의 |
| --- | --- |
| [발표자료/1차/tools/check_presentation.py](../../%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/1%EC%B0%A8/tools/check_presentation.py) | 소스: `check` · `read_json` |

<a name="setup"></a>

## ⚙️ 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 읽기 도구 | PDF 뷰어·PowerPoint 호환 프로그램 |
| 검사 도구 | Python·Pillow·PPTX ZIP/XML |
| 입력 조건 | content/data·원자료·차트·사진 manifest와 발표 파일 |

<a name="usage"></a>

## 📖 읽고 활용하는 순서

1. 이 차수의 변경 설명을 읽고 현재 최종 PDF에서 대응되는 발표 흐름을 봅니다.
2. 도입·방법·필터 비교·잡음·한계가 어떤 순서로 전달되는지 확인합니다.
3. PPTX 노트와 완성 대본의 장별 발화를 확인합니다.
4. 검사 도구를 이용하려면 입력 JSON·원자료·발표 파일의 경로를 먼저 준비합니다.

<a name="results"></a>

## 📊 결과를 읽는 방법

600초는 슬라이드에 배정한 목표 시간입니다. 실제 발화 시간이나 발표 평가 점수를 뜻하지 않으므로 리허설에서 확인합니다.

원정밀도 결과와 표시용 차트, 논문에 보고한 범위를 함께 읽습니다. 슬라이드 수가 늘었다고 새 연구 실험이 추가된 것은 아닙니다.

<a name="limits"></a>

## 🛠️ 알려진 제약과 확인 지점

| 상황 | 확인할 내용 |
| --- | --- |
| 현재 첨부 | 이전 발표 사본을 중복 첨부하지 않고 최종 발표로 연결합니다. |
| 도구 입력 | 공개 검사기 외에 그 차수의 content/data·근거 JSON 등이 필요합니다. |
| 수치 해석 | Strict Acc와 mAP, 일반·잡음·반복 결과를 구분합니다. |

<a name="changes"></a>

## 🔀 이전 단계와의 변화

논문의 표·그림을 발표 흐름으로 구성했습니다.2차에서는 비교 사진과 설명을 나누어 20장으로 바뀝니다.

[🔎 직전 단계 전체 비교·구성](../revision-diffs/talk-1.diff) · [📋 전체 파일 크기·해시](../revision-manifests/talk-1.json)

<details>
<summary>📎 이 단계의 파일 기록과 전체 해시</summary>

아래 표는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| `발표자료/1차/추계학술대회_10분발표.pdf` | .pdf | 455095 | `38af2a7abe54e010ad98fb3af06c1c6055e48a144c3ffee5a07f48d12a891644` |
| `발표자료/1차/추계학술대회_10분발표.pptx` | .pptx | 1879971 | `046e20d7ea256844fa4b80b83d317cbe3edfcba95ac157cf35bbeaac911956df` |
| `원본작업자료/발표자료/1차/.chart-data-AHQFVI/candidate.pptx` | .pptx | 1880011 | `b74ec39288db7fb1c0e8027c8d6cd77f6c56c333fcac633105f95ac2215cb24e` |
| `원본작업자료/발표자료/1차/.chart-data-KMLEaC/candidate.pptx` | .pptx | 1879923 | `f09ca68bbc1c9da7f8e31f80a871d180f861f0c53c52f3d7f464d351c85d2ede` |
| `원본작업자료/발표자료/1차/.chart-data-utlr4E/candidate.pptx` | .pptx | 1879940 | `8a580409738abc0f822e85498c34703c816767f3eaae9ef67ebfce867ed55640` |
| `원본작업자료/발표자료/1차/.chart-data-znEH9j/candidate.pptx` | .pptx | 1879995 | `53e7c7f151b51f71820f3bb9ac72cfd88f7d124433d471379945808fda1efe55` |
| [원본작업자료/발표자료/1차/work/authoring_adjust.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/1%EC%B0%A8/work/authoring_adjust.py) | .py | 992 | `da385a8f2570445735d5ac05dc0042ae97211c53838c5aabff9414c451cf87e5` |
| `원본작업자료/발표자료/1차/work/before-smoothing-finalized.pptx` | .pptx | 1879940 | `8a580409738abc0f822e85498c34703c816767f3eaae9ef67ebfce867ed55640` |
| [원본작업자료/발표자료/1차/work/build_presentation.mjs](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/1%EC%B0%A8/work/build_presentation.mjs) | .mjs | 17436 | `d01e71cb8e2d1c179c87c42a8f0aaf6b327451669d7d0909d1b95bca6dc45419` |
| `원본작업자료/발표자료/1차/work/candidate.pptx` | .pptx | 1870774 | `ff2e96f50d0e1e4f6da42fcb73b462b76f9875e5b1fce3f8aa3ba272fe053806` |
| `원본작업자료/발표자료/1차/work/initial-finalized.pptx` | .pptx | 1879995 | `53e7c7f151b51f71820f3bb9ac72cfd88f7d124433d471379945808fda1efe55` |
| [원본작업자료/발표자료/1차/work/prepare_content.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/1%EC%B0%A8/work/prepare_content.py) | .py | 16058 | `ba1f5e520953ac71ceba0cab26a539d219f25de244c17c5ccb7dd11054227fb7` |
| [원본작업자료/발표자료/1차/work/render_final.mjs](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/1%EC%B0%A8/work/render_final.mjs) | .mjs | 1009 | `fe387a9a8c298c3711003fb252e697b32ad7a85ca475b0b55115fff894adb59f` |

</details>

---

[🏠 프로젝트](../../README.md) · [🗂️ 전체 차수](../REVISION_INDEX.md) · [📁 자료 폴더](../../%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/1%EC%B0%A8) · [➡️ 발표자료 2차](talk-2.md)
