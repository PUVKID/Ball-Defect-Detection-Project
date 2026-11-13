<a id="-발표자료-2차--비교-사진을-분리한-20장-발표"></a>

# 발표자료 2차 · 비교 사진을 분리한 20장 발표

필터 비교 사진과 설명을 나누고 20장·600초 본발표로 재배치한 단계입니다.

분야: 연구 발표 › 필터 비교의 전달 구성 › 슬라이드·발화·차트·자산

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

현재 발표 첨부는 완성된 최종 20장 PDF/PPTX로 연결합니다.

해당 차수에서 슬라이드 분할·발화 시간·자산의 무엇이 바뀌었는지는 기존 전체 비교와 도구에서 확인할 수 있습니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

| 구성 | 실제 역할 |
| --- | --- |
| 사진 설명 | 4~9장에 필터 비교를 나누고 14~15장에 잡음 40/80 입력 예시를 분리합니다. |
| 시간과 마무리 | 모든 20장에 발화 시간을 배정하고 마지막을 감사·질의응답으로 구성합니다. |
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
| [발표자료/2차/tools/check_presentation.py](../../%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/2%EC%B0%A8/tools/check_presentation.py) | 처리 함수와 실행 조건 |
| [발표자료/최종/추계학술대회_10분발표.pdf](../../%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/%EC%B5%9C%EC%A2%85/%EC%B6%94%EA%B3%84%ED%95%99%EC%88%A0%EB%8C%80%ED%9A%8C_10%EB%B6%84%EB%B0%9C%ED%91%9C.pdf) | 전체 원문·도표 읽기 |
| [발표자료/최종/추계학술대회_10분발표.pptx](../../%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/%EC%B5%9C%EC%A2%85/%EC%B6%94%EA%B3%84%ED%95%99%EC%88%A0%EB%8C%80%ED%9A%8C_10%EB%B6%84%EB%B0%9C%ED%91%9C.pptx) | 발표 편집 원본 |

<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

| 파일 | 핵심 정의 |
| --- | --- |
| [발표자료/2차/tools/check_presentation.py](../../%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/2%EC%B0%A8/tools/check_presentation.py) | 소스: `check` · `read_json` |

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

1차 15장 구성에서 비교 사진 설명을 확장한 20장으로 바뀌었습니다. 기존 실험 결과의 설명 방식과 시간 배정이 달라졌습니다.

[직전 단계 전체 비교·구성](../revision-diffs/talk-2.diff) · [전체 파일 크기·해시](../revision-manifests/talk-2.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 표는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| `발표자료/2차/추계학술대회_10분발표.pdf` | .pdf | 4054848 | `4a17d156c3d737e06f6424e343bcbf6f11b26ce4a64617039d508448656824f9` |
| `발표자료/2차/추계학술대회_10분발표.pptx` | .pptx | 22906083 | `a56be240bf21da2ee23457a7c480251ac0167a3c1db252c61e1fdad96c4e3b59` |
| `원본작업자료/발표자료/2차/.chart-data-rP50bc/candidate.pptx` | .pptx | 22906081 | `0578378ee469cfb850ca3f3dbfdb931a0a7c4e76949318e283be97c4e02f7105` |
| [원본작업자료/발표자료/2차/work/assemble_builder.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/2%EC%B0%A8/work/assemble_builder.py) | .py | 6090 | `c1ee20bd63cc4dd1ac89d63f709d5cb05dbebf79a8fc2733e5a40293741f592d` |
| [원본작업자료/발표자료/2차/work/build_presentation.mjs](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/2%EC%B0%A8/work/build_presentation.mjs) | .mjs | 19355 | `7bdd4ec64e89988a4872067507817511ca0a7383128c9738a305777bc1bd9150` |
| `원본작업자료/발표자료/2차/work/candidate.pptx` | .pptx | 23589246 | `1f6b9bc37275e6a2c6122c46c15809eb14632660bebc9827d23e60495ebf9769` |
| `원본작업자료/발표자료/2차/work/first-finalized.pptx` | .pptx | 22906081 | `0578378ee469cfb850ca3f3dbfdb931a0a7c4e76949318e283be97c4e02f7105` |
| [원본작업자료/발표자료/2차/work/prepare_content.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/2%EC%B0%A8/work/prepare_content.py) | .py | 16058 | `ba1f5e520953ac71ceba0cab26a539d219f25de244c17c5ccb7dd11054227fb7` |
| [원본작업자료/발표자료/2차/work/prepare_revision.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/2%EC%B0%A8/work/prepare_revision.py) | .py | 13761 | `9f956dd067bf1d08cc6ad4bce285c00bc561cb7d69334aa49ec524cd83965a6a` |

</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C/2%EC%B0%A8) · [발표자료 1차](talk-1.md) · [발표자료 3차](talk-3.md)
