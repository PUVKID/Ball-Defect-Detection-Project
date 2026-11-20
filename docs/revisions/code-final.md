<a id="️-최종-연구코드--볼-검출과-규칙-기반-판정"></a>

# 최종 연구코드 · 볼 검출과 규칙 기반 판정

<!-- reading-levels17:start -->
**읽기 수준** · [LEVEL 1](#reading-level-1) · [LEVEL 2](#reading-level-2) · [LEVEL 3](#reading-level-3) · [LEVEL 4](#reading-level-4) · [LEVEL 5](#reading-level-5)

<a id="reading-level-1"></a>

## LEVEL 1 - Beginner

<a id="semantic-local-code-final-level-1"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | 유사 영상 그룹과 교차검증을 구성하고 전처리 필터별 YOLO 검출, 볼 일치, 영역별 개수 판정과 추가 진단을 함께 계산하는 노트북입니다. |
| 변경 | 단일 필터와 복합 필터 비교, 유사 그룹·Strict Acc·여러 조건 진단을 한 노트북에 모았습니다.<br>논문에 보고한 범위와 노트북의 추가 진단을 구분해 읽습니다. |
| 조건 | 500장 사진과 볼 위치 표시를 준비하고 원본·필터 사진으로 모델을 학습합니다.<br>예측한 볼 상자를 정답과 비교한 뒤 영상의 배치 규칙을 확인합니다.<br>서로 비슷한 사진은 바깥 평가 묶음에서 함께 취급합니다. |
| 동작 | 1.<br>노트북의 설정·데이터 로드·라벨 점검 셀을 읽고 입력 경로를 준비합니다. |
| 결과 | Strict Acc는 모든 라벨 볼을 중심 거리 기준으로 찾고 추가 검출이 없는 영상 비율입니다. fold_map은 model.val의 held-out test에서 mAP50·mAP50-95를 별도로 계산합니다. |

### LEVEL 1 · 검출과 별도 개수판정의 노트북

**검출과 별도 개수판정의 노트북**을 읽는 단계입니다.

영상과 YOLO 상자에서 필터별 검출 지표를 계산하고 별도 중앙 영역/위치별 개수 규칙으로 OK/NG를 비교합니다.

원영상과 가중치는 별도로 필요합니다.

먼저 자료의 역할을 확인한 뒤 아래의 확인 점을 따라가세요.

뒤 차수의 변경을 이 단계에서 이미 완료한 일로 바꾸지 않습니다.

| 조건·자료 | 의미와 확인 방법 |
| --- | --- |
| <a id="layout18-table-1-row-1"></a> 당시의 대상·조건 | 영상과 YOLO 상자에서 필터별 검출 지표를 계산하고 별도 중앙 영역/위치별 개수 규칙으로 OK/NG를 비교합니다.<br>원영상과 가중치는 별도로 필요합니다. |
| <a id="layout18-table-1-row-2"></a> 사용·확인·한계 | 검출 mAP·Strict와 라벨에 같은 개수 규칙을 적용한 정답의 일치율을 나눕니다. 100epoch 기준 실험·가상볼추가·임계값 진단을 논문 주비교와 구분합니다. |

[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md)

<a id="reading-level-2"></a>

## LEVEL 2 - Explorer

<a id="semantic-local-code-final-level-2"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | 유사 영상 그룹과 교차검증을 구성하고 전처리 필터별 YOLO 검출, 볼 일치, 영역별 개수 판정과 추가 진단을 함께 계산하는 노트북입니다. |
| 변경 | 단일 필터와 복합 필터 비교, 유사 그룹·Strict Acc·여러 조건 진단을 한 노트북에 모았습니다.<br>논문에 보고한 범위와 노트북의 추가 진단을 구분해 읽습니다. |
| 조건 | 유사 영상 그룹 기반 외부 5 겹 분할 →조건별 학습 →검출 →중심 매칭 →영상 판정·mAP 집계 순서입니다.<br>단일 10 종·순차 복합 5 종 필터와 원본을 비교합니다.<br>잡음 실험은 일반 조건과 별도로 읽습니다. |
| 동작 | 1.<br>노트북의 설정·데이터 로드·라벨 점검 셀을 읽고 입력 경로를 준비합니다. |
| 결과 | Strict Acc는 모든 라벨 볼을 중심 거리 기준으로 찾고 추가 검출이 없는 영상 비율입니다. fold_map은 model.val의 held-out test에서 mAP50·mAP50-95를 별도로 계산합니다. |

### LEVEL 2 · 검출과 별도 개수판정의 노트북

검출과 별도 개수 판정의 노트북에서는 입력 자료와 결과물 사이의 연결을 봅니다.

검출 mAP·Strict와 라벨에 같은 개수 규칙을 적용한 정답의 일치율을 나눕니다. 100epoch 기준 실험·가상볼추가·임계값 진단을 논문 주비교와 구분합니다.

각 산출물이 연구·계산·설명 중 어느 역할인지 나누면 차수의 의미가 분명해집니다.

| 조건·자료 | 의미와 확인 방법 |
| --- | --- |
| <a id="layout18-table-6-row-1"></a> 당시의 대상·조건 | 영상과 YOLO 상자에서 필터별 검출 지표를 계산하고 별도 중앙 영역/위치별 개수 규칙으로 OK/NG를 비교합니다.<br>원영상과 가중치는 별도로 필요합니다. |
| <a id="layout18-table-6-row-2"></a> 사용·확인·한계 | 검출 mAP·Strict와 라벨에 같은 개수 규칙을 적용한 정답의 일치율을 나눕니다. 100epoch 기준 실험·가상볼추가·임계값 진단을 논문 주비교와 구분합니다. |

[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md)

<a id="reading-level-3"></a>

## LEVEL 3 - Practitioner

<a id="semantic-local-code-final-level-3"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | 유사 영상 그룹과 교차검증을 구성하고 전처리 필터별 YOLO 검출, 볼 일치, 영역별 개수 판정과 추가 진단을 함께 계산하는 노트북입니다. |
| 변경 | 단일 필터와 복합 필터 비교, 유사 그룹·Strict Acc·여러 조건 진단을 한 노트북에 모았습니다.<br>논문에 보고한 범위와 노트북의 추가 진단을 구분해 읽습니다. |
| 조건 | A +B는 A 뒤 B 적용 순서입니다.<br>일반 영상은 원본·단일·복합, 노이즈는 원본·단일 필터 범위입니다.<br>파라미터는 원문 설정이며 모든 역 순·가능 조합이나 최적 값 탐색을 뜻하지 않습니다. |
| 동작 | 1.<br>노트북의 설정·데이터 로드·라벨 점검 셀을 읽고 입력 경로를 준비합니다. |
| 결과 | Strict Acc는 모든 라벨 볼을 중심 거리 기준으로 찾고 추가 검출이 없는 영상 비율입니다. fold_map은 model.val의 held-out test에서 mAP50·mAP50-95를 별도로 계산합니다. |

### LEVEL 3 · 검출과 별도 개수판정의 노트북

이 단계의 파일을 열고 입력 준비 →처리 →결과 확인 순서로 읽으세요.

영상과 YOLO 상자에서 필터별 검출 지표를 계산하고 별도 중앙 영역/위치별 개수 규칙으로 OK/NG를 비교합니다.

원영상과 가중치는 별도로 필요합니다.

검출 mAP·Strict와 라벨에 같은 개수 규칙을 적용한 정답의 일치율을 나눕니다. 100epoch 기준 실험·가상볼추가·임계값 진단을 논문 주비교와 구분합니다.

필요한 입력이 없으면 실행/검토를 완료했다고 보고하지 않습니다.

| 조건·자료 | 의미와 확인 방법 |
| --- | --- |
| <a id="layout18-table-11-row-1"></a> 당시의 대상·조건 | 영상과 YOLO 상자에서 필터별 검출 지표를 계산하고 별도 중앙 영역/위치별 개수 규칙으로 OK/NG를 비교합니다.<br>원영상과 가중치는 별도로 필요합니다. |
| <a id="layout18-table-11-row-2"></a> 사용·확인·한계 | 검출 mAP·Strict와 라벨에 같은 개수 규칙을 적용한 정답의 일치율을 나눕니다. 100epoch 기준 실험·가상볼추가·임계값 진단을 논문 주비교와 구분합니다. |

[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md)

<a id="reading-level-4"></a>

## LEVEL 4 - Advanced

<a id="semantic-local-code-final-level-4"></a>

| 항목 | 이 차수의 내용 |
| --- | --- |
| 목적 | 유사 영상 그룹과 교차검증을 구성하고 전처리 필터별 YOLO 검출, 볼 일치, 영역별 개수 판정과 추가 진단을 함께 계산하는 노트북입니다. |
| 변경 | 단일 필터와 복합 필터 비교, 유사 그룹·Strict Acc·여러 조건 진단을 한 노트북에 모았습니다.<br>논문에 보고한 범위와 노트북의 추가 진단을 구분해 읽습니다. |
| 조건 | assign_folds는 유사 그룹을 같은 외부 fold에 배치하고 fold_split은 남은 영상의 내부 검증을 나눕니다. ball_match_stats는 라벨 크기의 0.5 배 중심 거리로 일대일 매칭합니다.<br>외부 그룹 보존이 내부 그룹 분리까지 보장하지 않습니다. |
| 동작 | 1.<br>노트북의 설정·데이터 로드·라벨 점검 셀을 읽고 입력 경로를 준비합니다. |
| 결과 | Strict Acc는 모든 라벨 볼을 중심 거리 기준으로 찾고 추가 검출이 없는 영상 비율입니다. fold_map은 model.val의 held-out test에서 mAP50·mAP50-95를 별도로 계산합니다. |

### LEVEL 4 · 검출과 별도 개수판정의 노트북

검출과 별도 개수 판정의 노트북의 변경 경계는 아래 두 조건입니다.

원자료·계산 결과·표시·전달 자료를 구분하며, 직전 비교에서 작은 문장·파일 변화도 확인합니다.

검출 mAP·Strict와 라벨에 같은 개수 규칙을 적용한 정답의 일치율을 나눕니다. 100epoch 기준 실험·가상볼추가·임계값 진단을 논문 주비교와 구분합니다.

| 조건·자료 | 의미와 확인 방법 |
| --- | --- |
| <a id="layout18-table-16-row-1"></a> 당시의 대상·조건 | 영상과 YOLO 상자에서 필터별 검출 지표를 계산하고 별도 중앙 영역/위치별 개수 규칙으로 OK/NG를 비교합니다.<br>원영상과 가중치는 별도로 필요합니다. |
| <a id="layout18-table-16-row-2"></a> 사용·확인·한계 | 검출 mAP·Strict와 라벨에 같은 개수 규칙을 적용한 정답의 일치율을 나눕니다. 100epoch 기준 실험·가상볼추가·임계값 진단을 논문 주비교와 구분합니다. |

[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md)

<a id="reading-level-5"></a>

## LEVEL 5 - Expert

<a id="semantic-local-code-final-level-5"></a>

### LEVEL 5 · 검출과 별도 개수판정의 노트북

이 단계의 수락 범위는 해당 자료의 역할과 조건에 한정됩니다.

영상과 YOLO 상자에서 필터별 검출 지표를 계산하고 별도 중앙 영역/위치별 개수 규칙으로 OK/NG를 비교합니다.

원영상과 가중치는 별도로 필요합니다.

검출 mAP·Strict와 라벨에 같은 개수 규칙을 적용한 정답의 일치율을 나눕니다. 100epoch 기준 실험·가상볼추가·임계값 진단을 논문 주비교와 구분합니다.

독립적인 성능 재현·공개 승인·새 실험 완료로 확대하지 않습니다.

| 조건·자료 | 의미와 확인 방법 |
| --- | --- |
| <a id="layout18-table-21-row-1"></a> 당시의 대상·조건 | 영상과 YOLO 상자에서 필터별 검출 지표를 계산하고 별도 중앙 영역/위치별 개수 규칙으로 OK/NG를 비교합니다.<br>원영상과 가중치는 별도로 필요합니다. |
| <a id="layout18-table-21-row-2"></a> 사용·확인·한계 | 검출 mAP·Strict와 라벨에 같은 개수 규칙을 적용한 정답의 일치율을 나눕니다. 100epoch 기준 실험·가상볼추가·임계값 진단을 논문 주비교와 구분합니다. |

[동일 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)

<!-- reading-levels17:end -->

**유사 영상 그룹과 교차검증을 구성하고 전처리 필터별 YOLO 검출, 볼 일치, 영역별 개수 판정과 추가 진단을 함께 계산하는 노트북입니다.**

분야: 컴퓨터 비전 › YOLOv8n·PyTorch › 유사 그룹·교차검증·필터 실험

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

루트와 최종/연구 코드의 노트북은 같은 공개 바이트입니다. 영상 단위 OK/NG와 검출 지표는 다른 평가이며, 정답 경계 상자에 같은 규칙을 적용한 판정과 실제 전문가 판정을 구분합니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

| 구성 | 실제 역할 |
| --- | --- |
| <a id="layout18-table-22-row-1"></a> 자료 점검 | 라벨·클래스 균형·128 크기 축소 영상의 평균 절대 차이 기반 유사 그룹을 점검합니다. |
| <a id="layout18-table-22-row-2"></a> 영역 규칙 | 부품 사각형 내부의 볼 중심을 위 5·왼쪽 4·아래 2·오른쪽 2 규칙에 맞춰 판정합니다. |
| <a id="layout18-table-22-row-3"></a> 외부 fold | assign_folds가 유사 그룹을 같은 외부 fold에 두고 fold_split은 남은 영상에서 내부 검증을 나눕니다. |
| <a id="layout18-table-22-row-4"></a> 검출 품질 | ball_match_stats는 라벨 크기의 0.5 배 중심 허용 거리로 일대일 매칭하고 누락·추가 검출을 셉니다. |
| <a id="layout18-table-22-row-5"></a> 필터 실험 | train_per_filter·inference_only 모드와 결과 서명 기반 캐시를 구분합니다. |


<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

| 입력 | 처리 | 출력 |
| --- | --- | --- |
| 영상·YOLO 라벨 | 부품 위치·유사 그룹·fold 구성 | 학습·평가 자료 |
| 조건별 영상 | YOLO 학습·검출·중심 매칭 | 상자·누락·추가·위치 오차 |
| 정답·예측 상자 | 같은 영역 규칙과 별도 검출 mAP 집계 | 영상 판정·Strict Acc·mAP·그래프 |

<a name="files"></a>

<a id="-파일과-핵심-처리"></a>

## 파일별 역할

| 파일 | 이용 방법 |
| --- | --- |
| [ball_ok_ng_yolo_v7.ipynb](../../ball_ok_ng_yolo_v7.ipynb) | 설정·함수·실행 셀 |
| [최종/연구코드/ball_ok_ng_yolo_v7.ipynb](../../%EC%B5%9C%EC%A2%85/%EC%97%B0%EA%B5%AC%EC%BD%94%EB%93%9C/ball_ok_ng_yolo_v7.ipynb) | 설정·함수·실행 셀 |

<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

| 파일 | 핵심 정의 |
| --- | --- |
| <a id="layout18-table-25-row-1"></a> [ball_ok_ng_yolo_v7.ipynb](../../ball_ok_ng_yolo_v7.ipynb) | 셀 3: `GpuSampler` · `__init__` · `run` · `stop`<br>셀 4: `_bar_colors` · `plot_clean_bar`<br>셀 6: `read_yolo_boxes` · `list_dataset`<br>셀 8: `_ellipse` · `_locate_part_once` · `locate_part`<br>셀 10: `assign_region` · `judge_boxes`<br>셀 12: `_gt_worker`<br>셀 14: `find_dup_groups` · `find_root` |
| <a id="layout18-table-25-row-2"></a> [최종/연구코드/ball_ok_ng_yolo_v7.ipynb](../../%EC%B5%9C%EC%A2%85/%EC%97%B0%EA%B5%AC%EC%BD%94%EB%93%9C/ball_ok_ng_yolo_v7.ipynb) | 셀 3: `GpuSampler` · `__init__` · `run` · `stop`<br>셀 4: `_bar_colors` · `plot_clean_bar`<br>셀 6: `read_yolo_boxes` · `list_dataset`<br>셀 8: `_ellipse` · `_locate_part_once` · `locate_part`<br>셀 10: `assign_region` · `judge_boxes`<br>셀 12: `_gt_worker`<br>셀 14: `find_dup_groups` · `find_root` |


<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

| 항목 | 조건·기본값 |
| --- | --- |
| 기본 학습 | YOLOv8n·100epoch·1280·batch8 |
| 필터 학습 | 30epoch·외부 5fold·내부 val10% |
| 추론 | 기본 conf0.25·IoU0.5 |
| 기준 시드 | 42 |
| 필수 입력 | 데이터셋·라벨·GPU·필요한 가중치 |

<a name="usage"></a>

<a id="-준비와-사용-순서"></a>

## 실행 순서

1. 노트북의 설정·데이터 로드·라벨 점검 셀을 읽고 입력 경로를 준비합니다.
2. DO_TRAIN·TRAINED_WEIGHTS·FILTER_MODE·USE_CV·RUN_PRESET를 실행 목적에 맞게 확인합니다.
3. GPU 모니터·학습·출력 경로와 데이터 생성/복사 셀을 확인한 뒤 필요한 구간만 실행합니다.
4. 조건별 결과 표에서 분모·fold·캐시 서명을 확인하고 mAP와 Strict Acc를 따로 봅니다.
5. 독립 OK/NG 정답 목록이 있다면 OKNG_CSV 경로와 라벨 대응을 따로 확인합니다.

<a name="results"></a>

<a id="-결과를-읽는-방법"></a>

## 결과와 해석

Strict Acc는 모든 라벨 볼을 중심 거리 기준으로 찾고 추가 검출이 없는 영상 비율입니다. fold_map은 model.val의 held-out test에서 mAP50·mAP50-95를 별도로 계산합니다.

외부 그룹 분리와 내부 검증 분리는 같은 처리가 아닙니다. 내부 val은 이미지 단위로 나누므로 근접 중복 그룹이 겹칠 수 있습니다.

OKNG_CSV가 없을 때 규칙 기반 정답과의 일치 도를 전문가 판정 정확도로 부르지 않습니다.

<a name="limits"></a>

<a id="️-알려진-제약과-확인-지점"></a>

## 제약과 확인 사항

| 상황 | 확인할 내용 |
| --- | --- |
| <a id="layout18-table-27-row-1"></a> 일반화 범위 | 필터·잡음 조건별 재학습 결과이며 고정 모델의 미지 촬영 조건 적응성을 입증한 것은 아닙니다. |
| <a id="layout18-table-27-row-2"></a> 내부 분할 | 외부 평가 그룹은 분리하지만 내부 train/val에는 유사 그룹 중복이 남아 있습니다. |
| <a id="layout18-table-27-row-3"></a> 지표 정의 | Strict Acc는 중심 거리·누락·추가 검출 규칙이며 전문가 OK/NG 판정이나 mAP와 같지 않습니다. |
| <a id="layout18-table-27-row-4"></a> 실행 비용 | GPU 학습·여러 조건 평가·모니터 스레드와 파일 생성이 포함됩니다.<br>단순 열람과 전체 실행을 구분합니다. |
| <a id="layout18-table-27-row-5"></a> 캐시 | 자료·가중치·임계값·필터 파라미터의 서명이 같을 때 결과를 재사용합니다. |


<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

단일 필터와 복합 필터 비교, 유사 그룹·Strict Acc·여러 조건 진단을 한 노트북에 모았습니다. 논문에 보고한 범위와 노트북의 추가 진단을 구분해 읽습니다.

[직전 단계 전체 비교·구성](../revision-diffs/code-final-%EC%97%B4%EB%9E%8C.md) · [전체 파일 크기·해시](../revision-manifests/code-final.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 내용는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

| 파일 | 종류 | 바이트 | SHA-256 |
| --- | --- | --- | --- |
| <a id="layout18-table-28-row-1"></a> [ball_ok_ng_yolo_v7.ipynb](../../ball_ok_ng_yolo_v7.ipynb) | .ipynb | 277995 | `087c1a4c6a4a7487e2b037eb622b7336e59620d2731e69e4f35cbd0cb6847188` |
| <a id="layout18-table-28-row-2"></a> [최종/연구코드/ball_ok_ng_yolo_v7.ipynb](../../%EC%B5%9C%EC%A2%85/%EC%97%B0%EA%B5%AC%EC%BD%94%EB%93%9C/ball_ok_ng_yolo_v7.ipynb) | .ipynb | 277995 | `087c1a4c6a4a7487e2b037eb622b7336e59620d2731e69e4f35cbd0cb6847188` |
| <a id="layout18-table-28-row-3"></a> [원본작업자료/최종/연구코드/ball_ok_ng_yolo_v7.ipynb](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EC%B5%9C%EC%A2%85/%EC%97%B0%EA%B5%AC%EC%BD%94%EB%93%9C/ball_ok_ng_yolo_v7.ipynb) | .ipynb | 277994 | `fea389f8751b308129f4cfbbdc870eb7b20a025e2c0985cdeda33a1a9a3d354a` |


</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EC%B5%9C%EC%A2%85)


<a id="layout18-table-10-row-1"></a><a id="layout18-table-10-row-2"></a><a id="layout18-table-10-row-3"></a><a id="layout18-table-10-row-4"></a><a id="layout18-table-10-row-5"></a><a id="layout18-table-12-row-1"></a><a id="layout18-table-12-row-2"></a><a id="layout18-table-12-row-3"></a><a id="layout18-table-12-row-4"></a><a id="layout18-table-12-row-5"></a><a id="layout18-table-15-row-1"></a><a id="layout18-table-15-row-2"></a><a id="layout18-table-15-row-3"></a><a id="layout18-table-15-row-4"></a><a id="layout18-table-15-row-5"></a><a id="layout18-table-17-row-1"></a><a id="layout18-table-17-row-2"></a><a id="layout18-table-17-row-3"></a><a id="layout18-table-17-row-4"></a><a id="layout18-table-17-row-5"></a><a id="layout18-table-2-row-1"></a><a id="layout18-table-2-row-2"></a><a id="layout18-table-2-row-3"></a><a id="layout18-table-2-row-4"></a><a id="layout18-table-2-row-5"></a><a id="layout18-table-20-row-1"></a><a id="layout18-table-20-row-2"></a><a id="layout18-table-20-row-3"></a><a id="layout18-table-20-row-4"></a><a id="layout18-table-20-row-5"></a><a id="layout18-table-5-row-1"></a><a id="layout18-table-5-row-2"></a><a id="layout18-table-5-row-3"></a><a id="layout18-table-5-row-4"></a><a id="layout18-table-5-row-5"></a><a id="layout18-table-7-row-1"></a><a id="layout18-table-7-row-2"></a><a id="layout18-table-7-row-3"></a><a id="layout18-table-7-row-4"></a><a id="layout18-table-7-row-5"></a>
