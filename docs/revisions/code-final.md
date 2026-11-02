<div align="center">

# ⚙️ 최종 연구코드 · 볼 검출과 규칙 기반 판정

**유사 영상 그룹과 교차검증을 구성하고 전처리 필터별 YOLO 검출, 볼 일치, 영역별 개수 판정과 추가 진단을 함께 계산하는 노트북입니다.**

**기술 분류:** 컴퓨터 비전 › YOLOv8n·PyTorch › 유사 그룹·교차검증·필터 실험

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

</div>

<a name="purpose"></a>

## 🎯 이 단계에서 하는 일

루트와 최종/연구코드의 노트북은 같은 공개 바이트입니다. 영상 단위 OK/NG와 검출 지표는 다른 평가이며, 정답 경계상자에 같은 규칙을 적용한 판정과 실제 전문가 판정을 구분합니다.

<a name="features"></a>

## 🧩 주요 기능과 처리 방식

| 구성 | 실제 역할 |
| --- | --- |
| 자료 점검 | 라벨·클래스 균형·128크기 축소영상의 평균 절대 차이 기반 유사 그룹을 점검합니다. |
| 영역 규칙 | 부품 사각형 내부의 볼 중심을 위 5·왼쪽 4·아래 2·오른쪽 2 규칙에 맞춰 판정합니다. |
| 외부 fold | assign_folds가 유사 그룹을 같은 외부 fold에 두고 fold_split은 남은 영상에서 내부 검증을 나눕니다. |
| 검출 품질 | ball_match_stats는 라벨 크기의 0.5배 중심 허용거리로 일대일 매칭하고 누락·추가 검출을 셉니다. |
| 필터 실험 | train_per_filter·inference_only 모드와 결과 서명 기반 캐시를 구분합니다. |

<a name="flow"></a>

## 🔄 입력 → 처리 → 출력

| 입력 | 처리 | 출력·읽을 결과 |
| --- | --- | --- |
| 영상·YOLO 라벨 | 부품 위치·유사 그룹·fold 구성 | 학습·평가 자료 |
| 조건별 영상 | YOLO 학습·검출·중심 매칭 | 상자·누락·추가·위치 오차 |
| 정답·예측 상자 | 같은 영역 규칙과 별도 검출 mAP 집계 | 영상 판정·Strict Acc·mAP·그래프 |

<a name="files"></a>

## 📁 파일과 핵심 처리

| 파일 | 이용 방법 |
| --- | --- |
| [ball_ok_ng_yolo_v7.ipynb](../../ball_ok_ng_yolo_v7.ipynb) | 설정·함수·실행 셀 |
| [최종/연구코드/ball_ok_ng_yolo_v7.ipynb](../../%EC%B5%9C%EC%A2%85/%EC%97%B0%EA%B5%AC%EC%BD%94%EB%93%9C/ball_ok_ng_yolo_v7.ipynb) | 설정·함수·실행 셀 |

### 🔎 함수·셀로 찾아가기

아래 이름은 해당 파일의 실제 정의입니다. 위 처리 설명과 함께 설정·호출 순서·출력 경로를 따라 읽습니다.

| 파일 | 핵심 정의 |
| --- | --- |
| [ball_ok_ng_yolo_v7.ipynb](../../ball_ok_ng_yolo_v7.ipynb) | 셀 3: `GpuSampler` · `__init__` · `run` · `stop`<br>셀 4: `_bar_colors` · `plot_clean_bar`<br>셀 6: `read_yolo_boxes` · `list_dataset`<br>셀 8: `_ellipse` · `_locate_part_once` · `locate_part`<br>셀 10: `assign_region` · `judge_boxes`<br>셀 12: `_gt_worker`<br>셀 14: `find_dup_groups` · `find_root` |
| [최종/연구코드/ball_ok_ng_yolo_v7.ipynb](../../%EC%B5%9C%EC%A2%85/%EC%97%B0%EA%B5%AC%EC%BD%94%EB%93%9C/ball_ok_ng_yolo_v7.ipynb) | 셀 3: `GpuSampler` · `__init__` · `run` · `stop`<br>셀 4: `_bar_colors` · `plot_clean_bar`<br>셀 6: `read_yolo_boxes` · `list_dataset`<br>셀 8: `_ellipse` · `_locate_part_once` · `locate_part`<br>셀 10: `assign_region` · `judge_boxes`<br>셀 12: `_gt_worker`<br>셀 14: `find_dup_groups` · `find_root` |

<a name="setup"></a>

## ⚙️ 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 기본 학습 | YOLOv8n·100epoch·1280·batch8 |
| 필터 학습 | 30epoch·외부 5fold·내부 val10% |
| 추론 | 기본 conf0.25·IoU0.5 |
| 기준 시드 | 42 |
| 필수 입력 | 데이터셋·라벨·GPU·필요한 가중치 |

<a name="usage"></a>

## 🚀 준비와 사용 순서

1. 노트북의 설정·데이터 로드·라벨 점검 셀을 읽고 입력 경로를 준비합니다.
2. DO_TRAIN·TRAINED_WEIGHTS·FILTER_MODE·USE_CV·RUN_PRESET를 실행 목적에 맞게 확인합니다.
3. GPU 모니터·학습·출력 경로와 데이터 생성/복사 셀을 확인한 뒤 필요한 구간만 실행합니다.
4. 조건별 결과표에서 분모·fold·캐시 서명을 확인하고 mAP와 Strict Acc를 따로 봅니다.
5. 독립 OK/NG 정답 목록이 있다면 OKNG_CSV 경로와 라벨 대응을 따로 확인합니다.

<a name="results"></a>

## 📊 결과를 읽는 방법

Strict Acc는 모든 라벨 볼을 중심 거리 기준으로 찾고 추가 검출이 없는 영상 비율입니다. fold_map은 model.val의 held-out test에서 mAP50·mAP50-95를 별도로 계산합니다.

외부 그룹 분리와 내부 검증 분리는 같은 처리가 아닙니다. 내부 val은 이미지 단위로 나누므로 근접 중복 그룹이 겹칠 수 있습니다. OKNG_CSV가 없을 때 규칙 기반 정답과의 일치도를 전문가 판정 정확도로 부르지 않습니다.

<a name="limits"></a>

## 🛠️ 알려진 제약과 확인 지점

| 상황 | 확인할 내용 |
| --- | --- |
| 일반화 범위 | 필터·잡음 조건별 재학습 결과이며 고정 모델의 미지 촬영 조건 적응성을 입증한 것은 아닙니다. |
| 내부 분할 | 외부 평가 그룹은 분리하지만 내부 train/val에는 유사 그룹 중복이 남아 있습니다. |
| 지표 정의 | Strict Acc는 중심 거리·누락·추가 검출 규칙이며 전문가 OK/NG 판정이나 mAP와 같지 않습니다. |
| 실행 비용 | GPU 학습·여러 조건 평가·모니터 스레드와 파일 생성이 포함됩니다. 단순 열람과 전체 실행을 구분합니다. |
| 캐시 | 자료·가중치·임계값·필터 파라미터의 서명이 같을 때 결과를 재사용합니다. |

<a name="changes"></a>

## 🔀 이전 단계와의 변화

단일 필터와 복합 필터 비교, 유사 그룹·Strict Acc·여러 조건 진단을 한 노트북에 모았습니다. 논문에 보고한 범위와 노트북의 추가 진단을 구분해 읽습니다.

[🔎 직전 단계 전체 비교·구성](../revision-diffs/code-final.diff) · [📋 전체 파일 크기·해시](../revision-manifests/code-final.json)

<details>
<summary>📎 이 단계의 파일 기록과 전체 해시</summary>

아래 표는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

| 파일 | 종류 | 바이트 | SHA-256 |
|---|---|---:|---|
| [ball_ok_ng_yolo_v7.ipynb](../../ball_ok_ng_yolo_v7.ipynb) | .ipynb | 277995 | `087c1a4c6a4a7487e2b037eb622b7336e59620d2731e69e4f35cbd0cb6847188` |
| [최종/연구코드/ball_ok_ng_yolo_v7.ipynb](../../%EC%B5%9C%EC%A2%85/%EC%97%B0%EA%B5%AC%EC%BD%94%EB%93%9C/ball_ok_ng_yolo_v7.ipynb) | .ipynb | 277995 | `087c1a4c6a4a7487e2b037eb622b7336e59620d2731e69e4f35cbd0cb6847188` |
| [원본작업자료/최종/연구코드/ball_ok_ng_yolo_v7.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EC%B5%9C%EC%A2%85/%EC%97%B0%EA%B5%AC%EC%BD%94%EB%93%9C/ball_ok_ng_yolo_v7.ipynb) | .ipynb | 277994 | `fea389f8751b308129f4cfbbdc870eb7b20a025e2c0985cdeda33a1a9a3d354a` |

</details>

---

[🏠 프로젝트](../../README.md) · [🗂️ 전체 차수](../REVISION_INDEX.md) · [📁 자료 폴더](../../%EC%B5%9C%EC%A2%85)
