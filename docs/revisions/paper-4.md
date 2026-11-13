<a id="-논문-4차--원고-수치와-근거를-대조하는-도구"></a>

# 논문 4차 · 원고 수치와 근거를 대조하는 도구

<!-- reading-levels17:start -->
**읽기 수준 선택** · [LEVEL 1 - Beginner](#reading-level-1) · [LEVEL 2 - Explorer](#reading-level-2) · [LEVEL 3 - Practitioner](#reading-level-3) · [LEVEL 4 - Advanced](#reading-level-4) · [LEVEL 5 - Expert](#reading-level-5)

<a id="reading-level-1"></a>

## LEVEL 1 - Beginner

<!-- semantic-revision17:level-1:start -->

<a id="semantic-local-paper-4-level-1"></a>

### LEVEL 1 · 10개 검토 항목과 제출 준비의 구분

**10개 검토 항목과 제출 준비의 구분**을 읽는 단계입니다. check_review.py는10항목과 원고·근거해시,단일16조건8000행/반복39조건19500행의 영상별 결과를 대조합니다.500영상·368그룹·154유사쌍과 외부중복0/내부9~20그룹도 확인조건입니다. 먼저 자료의 역할을 확인한 뒤 아래의 확인점을 따라가세요. 뒤 차수의 변경을 이 단계에서 이미 완료한 일로 바꾸지 않습니다.

<a id="layout18-table-1-row-1"></a>

**당시의 대상·조건**

**조건·자료**

당시의 대상·조건

**의미와 확인 방법**

check_review.py는10항목과 원고·근거해시,단일16조건8000행/반복39조건19500행의 영상별 결과를 대조합니다.500영상·368그룹·154유사쌍과 외부중복0/내부9~20그룹도 확인조건입니다.

<a id="layout18-table-1-row-2"></a>

**사용·확인·한계**

**조건·자료**

사용·확인·한계

**의미와 확인 방법**

paper_ready_for_submission=False를 요구하며 PASS·주의·수정필요·확인불가를 구분합니다.약96dpi HWP그림·이중반올림·전체렌더 범위는 별도 확인이고,검사 통과가 제출승인이나 새 성능은 아닙니다.


<!-- semantic-revision17:level-1:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨1.md)

### LEVEL 1 · 목적과 대상

**이 차수의 목적과 실제 구성**

새 모델을 학습하는 대신 원고의 표·그림·문장과 저장된 원정밀도 결과를 대조한 검토 도구 단계입니다.

<a id="layout18-table-2-row-1"></a>

**원문 결합**

**구성**

원문 결합

**실제 역할**

원고 SHA와 입력·근거 파일 해시를 대조합니다.

<a id="layout18-table-2-row-2"></a>

**결과 계산**

**구성**

결과 계산

**실제 역할**

단일 16조건 8000행·반복 39조건 19500행의 영상별 결과를 집계하는 조건이 있습니다.

<a id="layout18-table-2-row-3"></a>

**분할 점검**

**구성**

분할 점검

**실제 역할**

500영상·368유사그룹·154유사쌍, 외부 중복 0과 내부 9~20그룹 중복을 확인하는 조건을 포함합니다.

<a id="layout18-table-2-row-4"></a>

**표시·서술**

**구성**

표시·서술

**실제 역할**

이중 반올림, HWP 그림 해상도, 인용·사사·원고 문장을 대조합니다.


부품 사진에서 작은 볼의 상자를 찾고, 볼이 정해진 배치·개수 규칙을 만족하는지 살피는 연구입니다. **결함 위치 자체를 직접 찾는 모델은 아닙니다.** 사진을 미리 처리하는 필터가 볼 검출과 영상 판정에 주는 영향을 비교합니다.

### LEVEL 1 · 달라진 내용과 차수 관계

3차/최종 원고와 실험 근거를 대조한 단계입니다. 새 원고·모델 학습이 아니라 수치·표현·그림 조건을 점검하는 기능으로 구분합니다.

[직전 단계 전체 비교·구성](../revision-diffs/paper-4.diff) · [전체 파일 크기·해시](../revision-manifests/paper-4.json)

볼이 하나 빠지거나 엉뚱한 위치에 추가로 보이면 영상 판정이 달라질 수 있습니다. 위 5·왼쪽 4·아래 2·오른쪽 2라는 규칙에 볼 중심을 맞춰 봅니다. 상자를 잘 찾는 일과 사람이 판단한 불량을 맞추는 일은 같지 않습니다.

### LEVEL 1 · 입력과 실행 조건

**입력**

원고·결과·점검 JSON

**처리**

해시와 항목 구성 확인

**출력**

근거가 연결된 점검 항목


**입력**

영상별 CSV

**처리**

지표·평균·표준편차 재계산

**출력**

원고 표와 원정밀도 차이


**입력**

그림·서술

**처리**

표시·해상도·문장 대조

**출력**

주의·수정 필요·확인 범위



<a id="layout18-table-4-row-1"></a>

**도구**

**항목**

도구

**조건·기본값**

Python·NumPy와 CSV/JSON

<a id="layout18-table-4-row-2"></a>

**입력**

**항목**

입력

**조건·기본값**

audit.json·원고·결과 CSV·recalculated·container_dataset·main_findings 등

<a id="layout18-table-4-row-3"></a>

**역할**

**항목**

역할

**조건·기본값**

입력 자료의 근거와 완결성을 대조


500장 사진과 볼 위치 표시를 준비하고 원본·필터 사진으로 모델을 학습합니다. 예측한 볼 상자를 정답과 비교한 뒤 영상의 배치 규칙을 확인합니다. 서로 비슷한 사진은 바깥 평가 묶음에서 함께 취급합니다.

### LEVEL 1 · 처리 절차

1. check_review.py의 ROOT와 처음 읽는 입력 목록을 확인합니다.
2. 원고·영상별 결과·근거 JSON을 같은 기록에 맞게 준비합니다.
3. 검사 조건에서 결과 계산·분할 중복·표시 차이를 각각 구분해 읽습니다.
4. 공개 도구에 없는 원본 근거를 준비하지 않은 상태에서는 전체 점검을 실행한 결과로 간주하지 않습니다.

원고와 저장 결과를 먼저 읽고 새 학습이 필요한지 판단합니다. 그래프를 다시 그리는 것과 모델을 다시 학습하는 것은 다릅니다. 여러 조건의 학습에는 별도 제조 영상과 GPU 환경이 필요합니다.

### LEVEL 1 · 결과를 확인하는 방법

도구는 paper_ready_for_submission=False를 요구하며 PASS·주의·수정필요·확인불가 상태를 구분합니다. 도구가 보존됐다는 사실만으로 원고가 수정됐거나 새 시험이 완료됐다고 보지 않습니다.

특히 원고 그림의 이중 반올림과 HWP 내장 그림 약 96dpi, 전체 문서 렌더 확인 범위가 별도 항목으로 연결됩니다. 이 단계의 발견과 현재 원고의 상태는 직전 비교와 함께 읽습니다.

mAP50-95는 볼 상자가 정답 위치와 얼마나 잘 맞는지 보는 지표입니다. Strict Acc는 한 사진의 볼을 모두 찾고 추가 검출도 없는 사진 비율입니다. 둘 중 하나가 높다고 다른 하나도 같은 수치라는 뜻은 아닙니다.

### LEVEL 1 · 주의할 범위

**상황**

의존 자료

**확인할 내용**

스크립트 외의 audit·근거 JSON·원고·결과 원자료가 필요합니다.


**상황**

평가 누수

**확인할 내용**

외부 그룹 분리와 내부 train/val 그룹 중복을 별개로 확인합니다.


**상황**

원고 보존

**확인할 내용**

발견한 차이를 숨기거나 원고 숫자를 임의 수정하는 도구가 아닙니다.



비슷한 사진이 학습과 내부 검증에 남을 수 있어 결과가 낙관적으로 보일 수 있습니다. 다른 촬영 로트에서의 확인은 후속 과제입니다. 원영상 전체와 모델 가중치는 별도로 필요합니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-2"></a>

## LEVEL 2 - Explorer

<!-- semantic-revision17:level-2:start -->

<a id="semantic-local-paper-4-level-2"></a>

### LEVEL 2 · 10개 검토 항목과 제출 준비의 구분

10개 검토 항목과 제출 준비의 구분에서는 입력자료와 결과물 사이의 연결을 봅니다. paper_ready_for_submission=False를 요구하며 PASS·주의·수정필요·확인불가를 구분합니다.약96dpi HWP그림·이중반올림·전체렌더 범위는 별도 확인이고,검사 통과가 제출승인이나 새 성능은 아닙니다. 각 산출물이 연구·계산·설명 중 어느 역할인지 나누면 차수의 의미가 분명해집니다.

<a id="layout18-table-6-row-1"></a>

**당시의 대상·조건**

**조건·자료**

당시의 대상·조건

**의미와 확인 방법**

check_review.py는10항목과 원고·근거해시,단일16조건8000행/반복39조건19500행의 영상별 결과를 대조합니다.500영상·368그룹·154유사쌍과 외부중복0/내부9~20그룹도 확인조건입니다.

<a id="layout18-table-6-row-2"></a>

**사용·확인·한계**

**조건·자료**

사용·확인·한계

**의미와 확인 방법**

paper_ready_for_submission=False를 요구하며 PASS·주의·수정필요·확인불가를 구분합니다.약96dpi HWP그림·이중반올림·전체렌더 범위는 별도 확인이고,검사 통과가 제출승인이나 새 성능은 아닙니다.


<!-- semantic-revision17:level-2:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A82.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨2.md)

### LEVEL 2 · 목적과 대상

**이 차수의 목적과 실제 구성**

새 모델을 학습하는 대신 원고의 표·그림·문장과 저장된 원정밀도 결과를 대조한 검토 도구 단계입니다.

<a id="layout18-table-7-row-1"></a>

**원문 결합**

**구성**

원문 결합

**실제 역할**

원고 SHA와 입력·근거 파일 해시를 대조합니다.

<a id="layout18-table-7-row-2"></a>

**결과 계산**

**구성**

결과 계산

**실제 역할**

단일 16조건 8000행·반복 39조건 19500행의 영상별 결과를 집계하는 조건이 있습니다.

<a id="layout18-table-7-row-3"></a>

**분할 점검**

**구성**

분할 점검

**실제 역할**

500영상·368유사그룹·154유사쌍, 외부 중복 0과 내부 9~20그룹 중복을 확인하는 조건을 포함합니다.

<a id="layout18-table-7-row-4"></a>

**표시·서술**

**구성**

표시·서술

**실제 역할**

이중 반올림, HWP 그림 해상도, 인용·사사·원고 문장을 대조합니다.


YOLOv8n 볼 검출과 영상 단위 OK/NG 규칙을 구분합니다. 전처리는 모델에 넣기 전 사진의 밝기·대비·무늬 등을 바꾸는 단계입니다. 검출 상자의 품질과 모든 볼을 빠짐없이 찾는 비율은 다른 지표입니다.

### LEVEL 2 · 달라진 내용과 차수 관계

3차/최종 원고와 실험 근거를 대조한 단계입니다. 새 원고·모델 학습이 아니라 수치·표현·그림 조건을 점검하는 기능으로 구분합니다.

[직전 단계 전체 비교·구성](../revision-diffs/paper-4.diff) · [전체 파일 크기·해시](../revision-manifests/paper-4.json)

부품 사각형 안에서 볼 중심의 영역별 개수를 확인합니다. 모델이 예측한 상자와 정답 상자에 같은 규칙을 적용해 판정할 수 있습니다. 전문가 판정 CSV가 없는 경우에는 이 규칙 일치도를 전문가 정확도로 부르지 않습니다.

### LEVEL 2 · 입력과 실행 조건

**입력**

원고·결과·점검 JSON

**처리**

해시와 항목 구성 확인

**출력**

근거가 연결된 점검 항목


**입력**

영상별 CSV

**처리**

지표·평균·표준편차 재계산

**출력**

원고 표와 원정밀도 차이


**입력**

그림·서술

**처리**

표시·해상도·문장 대조

**출력**

주의·수정 필요·확인 범위



<a id="layout18-table-9-row-1"></a>

**도구**

**항목**

도구

**조건·기본값**

Python·NumPy와 CSV/JSON

<a id="layout18-table-9-row-2"></a>

**입력**

**항목**

입력

**조건·기본값**

audit.json·원고·결과 CSV·recalculated·container_dataset·main_findings 등

<a id="layout18-table-9-row-3"></a>

**역할**

**항목**

역할

**조건·기본값**

입력 자료의 근거와 완결성을 대조


유사 영상 그룹 기반 외부 5겹 분할→조건별 학습→검출→중심 매칭→영상 판정·mAP 집계 순서입니다. 단일 10종·순차 복합 5종 필터와 원본을 비교합니다. 잡음 실험은 일반 조건과 별도로 읽습니다.

### LEVEL 2 · 처리 절차

1. check_review.py의 ROOT와 처음 읽는 입력 목록을 확인합니다.
2. 원고·영상별 결과·근거 JSON을 같은 기록에 맞게 준비합니다.
3. 검사 조건에서 결과 계산·분할 중복·표시 차이를 각각 구분해 읽습니다.
4. 공개 도구에 없는 원본 근거를 준비하지 않은 상태에서는 전체 점검을 실행한 결과로 간주하지 않습니다.

최종 노트북과 이전 도커 결과를 구분하고 설정·캐시·출력 파일을 확인합니다. 원고·발표·검토 도구는 각 차수의 목적이 다릅니다. 발표 시간은 실제 리허설로 확인해야 합니다.

### LEVEL 2 · 결과를 확인하는 방법

도구는 paper_ready_for_submission=False를 요구하며 PASS·주의·수정필요·확인불가 상태를 구분합니다. 도구가 보존됐다는 사실만으로 원고가 수정됐거나 새 시험이 완료됐다고 보지 않습니다.

특히 원고 그림의 이중 반올림과 HWP 내장 그림 약 96dpi, 전체 문서 렌더 확인 범위가 별도 항목으로 연결됩니다. 이 단계의 발견과 현재 원고의 상태는 직전 비교와 함께 읽습니다.

일반 영상 단일 시드에서 원고는 Gamma0.3 mAP50-95 96.70%, Original 96.53%를 보고합니다. 차이는 0.17%p입니다. 작은 차이를 모든 촬영 환경에서의 우위로 확대하지 않습니다.

### LEVEL 2 · 주의할 범위

**상황**

의존 자료

**확인할 내용**

스크립트 외의 audit·근거 JSON·원고·결과 원자료가 필요합니다.


**상황**

평가 누수

**확인할 내용**

외부 그룹 분리와 내부 train/val 그룹 중복을 별개로 확인합니다.


**상황**

원고 보존

**확인할 내용**

발견한 차이를 숨기거나 원고 숫자를 임의 수정하는 도구가 아닙니다.



외부 그룹 분리와 내부 검증 분리는 다릅니다. 필터·잡음마다 모델을 다시 학습했기 때문에 처음 보는 환경에 같은 모델을 바로 쓰는 시험과도 다릅니다. 전문가 OK/NG 정답의 유무도 확인합니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-3"></a>

## LEVEL 3 - Practitioner

<!-- semantic-revision17:level-3:start -->

<a id="semantic-local-paper-4-level-3"></a>

### LEVEL 3 · 10개 검토 항목과 제출 준비의 구분

이 단계의 파일을 열고 입력 준비→처리→결과 확인 순서로 읽으세요. check_review.py는10항목과 원고·근거해시,단일16조건8000행/반복39조건19500행의 영상별 결과를 대조합니다.500영상·368그룹·154유사쌍과 외부중복0/내부9~20그룹도 확인조건입니다. paper_ready_for_submission=False를 요구하며 PASS·주의·수정필요·확인불가를 구분합니다.약96dpi HWP그림·이중반올림·전체렌더 범위는 별도 확인이고,검사 통과가 제출승인이나 새 성능은 아닙니다. 필요한 입력이 없으면 실행/검토를 완료했다고 보고하지 않습니다.

<a id="layout18-table-11-row-1"></a>

**당시의 대상·조건**

**조건·자료**

당시의 대상·조건

**의미와 확인 방법**

check_review.py는10항목과 원고·근거해시,단일16조건8000행/반복39조건19500행의 영상별 결과를 대조합니다.500영상·368그룹·154유사쌍과 외부중복0/내부9~20그룹도 확인조건입니다.

<a id="layout18-table-11-row-2"></a>

**사용·확인·한계**

**조건·자료**

사용·확인·한계

**의미와 확인 방법**

paper_ready_for_submission=False를 요구하며 PASS·주의·수정필요·확인불가를 구분합니다.약96dpi HWP그림·이중반올림·전체렌더 범위는 별도 확인이고,검사 통과가 제출승인이나 새 성능은 아닙니다.


<!-- semantic-revision17:level-3:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A83.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨3.md)

### LEVEL 3 · 목적과 대상

**이 차수의 목적과 실제 구성**

새 모델을 학습하는 대신 원고의 표·그림·문장과 저장된 원정밀도 결과를 대조한 검토 도구 단계입니다.

<a id="layout18-table-12-row-1"></a>

**원문 결합**

**구성**

원문 결합

**실제 역할**

원고 SHA와 입력·근거 파일 해시를 대조합니다.

<a id="layout18-table-12-row-2"></a>

**결과 계산**

**구성**

결과 계산

**실제 역할**

단일 16조건 8000행·반복 39조건 19500행의 영상별 결과를 집계하는 조건이 있습니다.

<a id="layout18-table-12-row-3"></a>

**분할 점검**

**구성**

분할 점검

**실제 역할**

500영상·368유사그룹·154유사쌍, 외부 중복 0과 내부 9~20그룹 중복을 확인하는 조건을 포함합니다.

<a id="layout18-table-12-row-4"></a>

**표시·서술**

**구성**

표시·서술

**실제 역할**

이중 반올림, HWP 그림 해상도, 인용·사사·원고 문장을 대조합니다.


실행 노트북·저장 CSV/JSON·원고·발표를 연결해 결과를 읽는 자료입니다. 일반 영상과 잡음 조건, 단일 실험과 세 시드 반복을 나눕니다. 노트북의 추가 진단을 논문의 보고 범위에 소급하지 않습니다.

### LEVEL 3 · 달라진 내용과 차수 관계

3차/최종 원고와 실험 근거를 대조한 단계입니다. 새 원고·모델 학습이 아니라 수치·표현·그림 조건을 점검하는 기능으로 구분합니다.

[직전 단계 전체 비교·구성](../revision-diffs/paper-4.diff) · [전체 파일 크기·해시](../revision-manifests/paper-4.json)

OKNG_CSV의 유무와 정답 정의를 먼저 확인합니다. 경계상자 라벨 기반 판정, mAP, 누락·추가·위치 오류를 별도로 읽으세요. 어떤 지표가 실제 전문가 라벨과 비교했는지 기록해야 합니다.

### LEVEL 3 · 입력과 실행 조건

**입력**

원고·결과·점검 JSON

**처리**

해시와 항목 구성 확인

**출력**

근거가 연결된 점검 항목


**입력**

영상별 CSV

**처리**

지표·평균·표준편차 재계산

**출력**

원고 표와 원정밀도 차이


**입력**

그림·서술

**처리**

표시·해상도·문장 대조

**출력**

주의·수정 필요·확인 범위



<a id="layout18-table-14-row-1"></a>

**도구**

**항목**

도구

**조건·기본값**

Python·NumPy와 CSV/JSON

<a id="layout18-table-14-row-2"></a>

**입력**

**항목**

입력

**조건·기본값**

audit.json·원고·결과 CSV·recalculated·container_dataset·main_findings 등

<a id="layout18-table-14-row-3"></a>

**역할**

**항목**

역할

**조건·기본값**

입력 자료의 근거와 완결성을 대조


A+B는 A 뒤 B 적용 순서입니다. 일반 영상은 원본·단일·복합, 노이즈는 원본·단일 필터 범위입니다. 파라미터는 원문 설정이며 모든 역순·가능 조합이나 최적값 탐색을 뜻하지 않습니다.

### LEVEL 3 · 처리 절차

1. check_review.py의 ROOT와 처음 읽는 입력 목록을 확인합니다.
2. 원고·영상별 결과·근거 JSON을 같은 기록에 맞게 준비합니다.
3. 검사 조건에서 결과 계산·분할 중복·표시 차이를 각각 구분해 읽습니다.
4. 공개 도구에 없는 원본 근거를 준비하지 않은 상태에서는 전체 점검을 실행한 결과로 간주하지 않습니다.

train_per_filter와 inference_only 모드, 자료·가중치·임계값·필터 서명 기반 캐시를 확인합니다. 기존 결과 열람과 재실행을 분리하세요. 단순 도구 검사 통과를 논문 제출이나 성능 승인으로 바꾸지 않습니다.

### LEVEL 3 · 결과를 확인하는 방법

도구는 paper_ready_for_submission=False를 요구하며 PASS·주의·수정필요·확인불가 상태를 구분합니다. 도구가 보존됐다는 사실만으로 원고가 수정됐거나 새 시험이 완료됐다고 보지 않습니다.

특히 원고 그림의 이중 반올림과 HWP 내장 그림 약 96dpi, 전체 문서 렌더 확인 범위가 별도 항목으로 연결됩니다. 이 단계의 발견과 현재 원고의 상태는 직전 비교와 함께 읽습니다.

원고의 단일·반복·잡음 결과를 각각 해당 분할·시드와 연결해 읽습니다. Strict Acc의 누락·추가 조건을 확인하고 mAP와 구분합니다. 표시된 그래프보다 CSV/JSON의 원정밀도와 조건이 우선 근거입니다.

### LEVEL 3 · 주의할 범위

**상황**

의존 자료

**확인할 내용**

스크립트 외의 audit·근거 JSON·원고·결과 원자료가 필요합니다.


**상황**

평가 누수

**확인할 내용**

외부 그룹 분리와 내부 train/val 그룹 중복을 별개로 확인합니다.


**상황**

원고 보존

**확인할 내용**

발견한 차이를 숨기거나 원고 숫자를 임의 수정하는 도구가 아닙니다.



내부 9~20그룹 중복과 독립 로트 부재를 결과 옆에 기록합니다. 캐시와 저장 결과의 실행 조건을 확인하고 없는 제조 자료를 제공된 입력처럼 쓰지 않습니다. 지표 이름이 같아도 다른 실행을 합치지 않습니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-4"></a>

## LEVEL 4 - Advanced

<!-- semantic-revision17:level-4:start -->

<a id="semantic-local-paper-4-level-4"></a>

### LEVEL 4 · 10개 검토 항목과 제출 준비의 구분

10개 검토 항목과 제출 준비의 구분의 변경 경계는 아래 두 조건입니다. 원자료·계산결과·표시·전달자료를 구분하며,직전 비교에서 작은 문장·파일 변화도 확인합니다. paper_ready_for_submission=False를 요구하며 PASS·주의·수정필요·확인불가를 구분합니다.약96dpi HWP그림·이중반올림·전체렌더 범위는 별도 확인이고,검사 통과가 제출승인이나 새 성능은 아닙니다.

<a id="layout18-table-16-row-1"></a>

**당시의 대상·조건**

**조건·자료**

당시의 대상·조건

**의미와 확인 방법**

check_review.py는10항목과 원고·근거해시,단일16조건8000행/반복39조건19500행의 영상별 결과를 대조합니다.500영상·368그룹·154유사쌍과 외부중복0/내부9~20그룹도 확인조건입니다.

<a id="layout18-table-16-row-2"></a>

**사용·확인·한계**

**조건·자료**

사용·확인·한계

**의미와 확인 방법**

paper_ready_for_submission=False를 요구하며 PASS·주의·수정필요·확인불가를 구분합니다.약96dpi HWP그림·이중반올림·전체렌더 범위는 별도 확인이고,검사 통과가 제출승인이나 새 성능은 아닙니다.


<!-- semantic-revision17:level-4:end -->

[이 수준의 프로젝트 전체 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A84.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨4.md)

### LEVEL 4 · 목적과 대상

**이 차수의 목적과 실제 구성**

새 모델을 학습하는 대신 원고의 표·그림·문장과 저장된 원정밀도 결과를 대조한 검토 도구 단계입니다.

<a id="layout18-table-17-row-1"></a>

**원문 결합**

**구성**

원문 결합

**실제 역할**

원고 SHA와 입력·근거 파일 해시를 대조합니다.

<a id="layout18-table-17-row-2"></a>

**결과 계산**

**구성**

결과 계산

**실제 역할**

단일 16조건 8000행·반복 39조건 19500행의 영상별 결과를 집계하는 조건이 있습니다.

<a id="layout18-table-17-row-3"></a>

**분할 점검**

**구성**

분할 점검

**실제 역할**

500영상·368유사그룹·154유사쌍, 외부 중복 0과 내부 9~20그룹 중복을 확인하는 조건을 포함합니다.

<a id="layout18-table-17-row-4"></a>

**표시·서술**

**구성**

표시·서술

**실제 역할**

이중 반올림, HWP 그림 해상도, 인용·사사·원고 문장을 대조합니다.


필터·잡음 조건별 재학습 비교와 규칙 판정이 결합된 구조입니다. 외부 평가 그룹은 분리하지만 내부 train/val의 근접 중복은 남을 수 있습니다. 전처리의 효과와 분할·학습 정책의 효과를 함께 고려해야 합니다.

### LEVEL 4 · 달라진 내용과 차수 관계

3차/최종 원고와 실험 근거를 대조한 단계입니다. 새 원고·모델 학습이 아니라 수치·표현·그림 조건을 점검하는 기능으로 구분합니다.

[직전 단계 전체 비교·구성](../revision-diffs/paper-4.diff) · [전체 파일 크기·해시](../revision-manifests/paper-4.json)

영역 규칙은 검출기 출력의 후처리입니다. 중심 거리 매칭과 영역별 개수 판정은 다른 기준이며 파라미터 변화가 각 지표에 다르게 작용할 수 있습니다. 검출과 판정의 오류를 나누어 추적합니다.

### LEVEL 4 · 입력과 실행 조건

**입력**

원고·결과·점검 JSON

**처리**

해시와 항목 구성 확인

**출력**

근거가 연결된 점검 항목


**입력**

영상별 CSV

**처리**

지표·평균·표준편차 재계산

**출력**

원고 표와 원정밀도 차이


**입력**

그림·서술

**처리**

표시·해상도·문장 대조

**출력**

주의·수정 필요·확인 범위



<a id="layout18-table-19-row-1"></a>

**도구**

**항목**

도구

**조건·기본값**

Python·NumPy와 CSV/JSON

<a id="layout18-table-19-row-2"></a>

**입력**

**항목**

입력

**조건·기본값**

audit.json·원고·결과 CSV·recalculated·container_dataset·main_findings 등

<a id="layout18-table-19-row-3"></a>

**역할**

**항목**

역할

**조건·기본값**

입력 자료의 근거와 완결성을 대조


assign_folds는 유사 그룹을 같은 외부 fold에 배치하고 fold_split은 남은 영상의 내부 검증을 나눕니다. ball_match_stats는 라벨 크기의 0.5배 중심 거리로 일대일 매칭합니다. 외부 그룹 보존이 내부 그룹 분리까지 보장하지 않습니다.

### LEVEL 4 · 처리 절차

1. check_review.py의 ROOT와 처음 읽는 입력 목록을 확인합니다.
2. 원고·영상별 결과·근거 JSON을 같은 기록에 맞게 준비합니다.
3. 검사 조건에서 결과 계산·분할 중복·표시 차이를 각각 구분해 읽습니다.
4. 공개 도구에 없는 원본 근거를 준비하지 않은 상태에서는 전체 점검을 실행한 결과로 간주하지 않습니다.

재현에는 분할·시드·전처리 순서·가중치·캐시 서명이 필요합니다. 서로 다른 실행 결과를 섞어 그래프를 만들지 않습니다. 발표자료의 그림·발화·대본 수정은 새 모델 실험을 뜻하지 않습니다.

### LEVEL 4 · 결과를 확인하는 방법

도구는 paper_ready_for_submission=False를 요구하며 PASS·주의·수정필요·확인불가 상태를 구분합니다. 도구가 보존됐다는 사실만으로 원고가 수정됐거나 새 시험이 완료됐다고 보지 않습니다.

특히 원고 그림의 이중 반올림과 HWP 내장 그림 약 96dpi, 전체 문서 렌더 확인 범위가 별도 항목으로 연결됩니다. 이 단계의 발견과 현재 원고의 상태는 직전 비교와 함께 읽습니다.

Strict Acc는 모든 라벨 볼의 중심 거리 매칭과 추가 검출 부재를 함께 요구합니다. mAP는 별도 검출 평가입니다. 조건별 재학습 성능이 좋아도 고정 모델에 처음 보는 촬영 조건을 넣었을 때의 강건성을 입증한 것은 아닙니다.

### LEVEL 4 · 주의할 범위

**상황**

의존 자료

**확인할 내용**

스크립트 외의 audit·근거 JSON·원고·결과 원자료가 필요합니다.


**상황**

평가 누수

**확인할 내용**

외부 그룹 분리와 내부 train/val 그룹 중복을 별개로 확인합니다.


**상황**

원고 보존

**확인할 내용**

발견한 차이를 숨기거나 원고 숫자를 임의 수정하는 도구가 아닙니다.



분할 누수·재학습 정책·대리 정답·조건별 비용이 주요 트레이드오프입니다. 필터 파라미터는 비교 설정이며 최적값이 아닙니다. 더 높은 한 지표만 골라 전체 조건의 우위를 주장하지 않습니다.

[표·코드·실행 설정·파일 전체 비교를 포함한 공통 상세](#reading-level-5)

<a id="reading-level-5"></a>

## LEVEL 5 - Expert

<!-- semantic-revision17:level-5:start -->

<a id="semantic-local-paper-4-level-5"></a>

### LEVEL 5 · 10개 검토 항목과 제출 준비의 구분

이 단계의 수락 범위는 해당 자료의 역할과 조건에 한정됩니다. check_review.py는10항목과 원고·근거해시,단일16조건8000행/반복39조건19500행의 영상별 결과를 대조합니다.500영상·368그룹·154유사쌍과 외부중복0/내부9~20그룹도 확인조건입니다. paper_ready_for_submission=False를 요구하며 PASS·주의·수정필요·확인불가를 구분합니다.약96dpi HWP그림·이중반올림·전체렌더 범위는 별도 확인이고,검사 통과가 제출승인이나 새 성능은 아닙니다. 독립적인 성능 재현·공개 승인·새 실험 완료로 확대하지 않습니다.

<a id="layout18-table-21-row-1"></a>

**당시의 대상·조건**

**조건·자료**

당시의 대상·조건

**의미와 확인 방법**

check_review.py는10항목과 원고·근거해시,단일16조건8000행/반복39조건19500행의 영상별 결과를 대조합니다.500영상·368그룹·154유사쌍과 외부중복0/내부9~20그룹도 확인조건입니다.

<a id="layout18-table-21-row-2"></a>

**사용·확인·한계**

**조건·자료**

사용·확인·한계

**의미와 확인 방법**

paper_ready_for_submission=False를 요구하며 PASS·주의·수정필요·확인불가를 구분합니다.약96dpi HWP그림·이중반올림·전체렌더 범위는 별도 확인이고,검사 통과가 제출승인이나 새 성능은 아닙니다.


<!-- semantic-revision17:level-5:end -->

[전문가 수준 프로젝트 안내](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md) · [같은 수준 프로필](https://github.com/PUVKID/PUVKID/blob/main/docs/읽기안내/레벨5.md)

**기존 전체 상세** — 다음 본문은 이 차수의 원래 방법·조건·결과·실패·한계와 전체 비교입니다. 위 수준의 설명에 필요한 공통 근거도 모두 여기서 확인할 수 있습니다.
<!-- reading-levels17:end -->

**새 모델을 학습하는 대신 원고의 표·그림·문장과 저장된 원정밀도 결과를 대조한 검토 도구 단계입니다.**

분야: 연구 보조 도구 › 원고·결과 대조 › JSON·CSV·수치·표현 검사

[목적](#purpose) · [기능](#features) · [입출력](#flow) · [구성](#files) · [준비](#setup) · [사용법](#usage) · [결과](#results) · [제약](#limits) · [변경](#changes)

<a name="purpose"></a>

<a id="-이-단계에서-하는-일"></a>

## 연구 목적

check_review.py는 10개 항목과 원고·결과 자료의 해시, 단일·반복 결과의 지표, 분할 중복과 그림의 표시 정밀도 등을 확인합니다.

도구의 조건을 만족하는 것과 논문 제출·성능을 승인하는 것은 구분합니다.

<a name="features"></a>

<a id="-주요-기능과-처리-방식"></a>

## 방법과 구현

<a id="layout18-table-22-row-1"></a>

**원문 결합**

**구성**

원문 결합

**실제 역할**

원고 SHA와 입력·근거 파일 해시를 대조합니다.

<a id="layout18-table-22-row-2"></a>

**결과 계산**

**구성**

결과 계산

**실제 역할**

단일 16조건 8000행·반복 39조건 19500행의 영상별 결과를 집계하는 조건이 있습니다.

<a id="layout18-table-22-row-3"></a>

**분할 점검**

**구성**

분할 점검

**실제 역할**

500영상·368유사그룹·154유사쌍, 외부 중복 0과 내부 9~20그룹 중복을 확인하는 조건을 포함합니다.

<a id="layout18-table-22-row-4"></a>

**표시·서술**

**구성**

표시·서술

**실제 역할**

이중 반올림, HWP 그림 해상도, 인용·사사·원고 문장을 대조합니다.


<a name="flow"></a>

<a id="-입력--처리--출력"></a>

## 입력·처리·출력

**입력**

원고·결과·점검 JSON

**처리**

해시와 항목 구성 확인

**출력**

근거가 연결된 점검 항목


**입력**

영상별 CSV

**처리**

지표·평균·표준편차 재계산

**출력**

원고 표와 원정밀도 차이


**입력**

그림·서술

**처리**

표시·해상도·문장 대조

**출력**

주의·수정 필요·확인 범위



<a name="files"></a>

<a id="-파일과-핵심-처리"></a>

## 파일별 역할

| 내용 |
| --- |
| **파일**<br>[논문/4차/tools/check_review.py](../../%EB%85%BC%EB%AC%B8/4%EC%B0%A8/tools/check_review.py)<br><br>**이용 방법**<br>처리 함수와 실행 조건 |
| **파일**<br>[논문/최종_논문.pdf](../../%EB%85%BC%EB%AC%B8/%EC%B5%9C%EC%A2%85_%EB%85%BC%EB%AC%B8.pdf)<br><br>**이용 방법**<br>전체 원문·도표 읽기 |

<a id="-함수셀로-찾아가기"></a>

### 관련 함수와 셀

관련 함수와 셀을 파일별로 정리했습니다. 실행 전 설정과 호출 순서, 출력 경로를 확인하세요.

| 내용 |
| --- |
| **파일**<br>[논문/4차/tools/check_review.py](../../%EB%85%BC%EB%AC%B8/4%EC%B0%A8/tools/check_review.py)<br><br>**핵심 정의**<br>소스: `rows` |

<a name="setup"></a>

<a id="️-환경과-설정"></a>

## 실행 환경과 설정

<a id="layout18-table-26-row-1"></a>

**도구**

**항목**

도구

**조건·기본값**

Python·NumPy와 CSV/JSON

<a id="layout18-table-26-row-2"></a>

**입력**

**항목**

입력

**조건·기본값**

audit.json·원고·결과 CSV·recalculated·container_dataset·main_findings 등

<a id="layout18-table-26-row-3"></a>

**역할**

**항목**

역할

**조건·기본값**

입력 자료의 근거와 완결성을 대조


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

**상황**

의존 자료

**확인할 내용**

스크립트 외의 audit·근거 JSON·원고·결과 원자료가 필요합니다.


**상황**

평가 누수

**확인할 내용**

외부 그룹 분리와 내부 train/val 그룹 중복을 별개로 확인합니다.


**상황**

원고 보존

**확인할 내용**

발견한 차이를 숨기거나 원고 숫자를 임의 수정하는 도구가 아닙니다.



<a name="changes"></a>

<a id="-이전-단계와의-변화"></a>

## 직전 단계와 비교

3차/최종 원고와 실험 근거를 대조한 단계입니다. 새 원고·모델 학습이 아니라 수치·표현·그림 조건을 점검하는 기능으로 구분합니다.

[직전 단계 전체 비교·구성](../revision-diffs/paper-4.diff) · [전체 파일 크기·해시](../revision-manifests/paper-4.json)

<details>
<summary>이 단계의 파일 기록과 전체 해시</summary>

아래 내용는 해당 단계가 기록될 당시의 파일 정보입니다. 현재 첨부는 [프로젝트 자료 안내](../PAPERS.md)에서 확인할 수 있습니다.

<a id="layout18-table-28-row-1"></a>

**[논문/4차/tools/check_review.py](../../%EB%85%BC%EB%AC%B8/4%EC%B0%A8/tools/check_review.py)**

**파일**

[논문/4차/tools/check_review.py](../../%EB%85%BC%EB%AC%B8/4%EC%B0%A8/tools/check_review.py)

**종류**

.py

**바이트**

9435

**SHA-256**

`4279a2748567df1bbc899cb17ae2673df9d8912748e78d465a9d254e3c117d3c`

<a id="layout18-table-28-row-2"></a>

**[원본작업자료/논문/4차/work/main_layout_inspect.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/main_layout_inspect.py)**

**파일**

[원본작업자료/논문/4차/work/main_layout_inspect.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/main_layout_inspect.py)

**종류**

.py

**바이트**

4217

**SHA-256**

`b2507d2b88667f60dc0f99346f0037d76c989869f2ada7025f91a88ffda2f033`

<a id="layout18-table-28-row-3"></a>

**항목 3**

**파일**

[원본작업자료/논문/4차/work/evidence/build_audit_report.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/build_audit_report.py)

**종류**

.py

**바이트**

22369

**SHA-256**

`54e83b637fbd994d4a0c88fd07dd46b448f79be6035d212c11af2a3a7abad1bc`

<a id="layout18-table-28-row-4"></a>

**항목 4**

**파일**

[원본작업자료/논문/4차/work/evidence/check_metrics_code.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/check_metrics_code.py)

**종류**

.py

**바이트**

2309

**SHA-256**

`8272fc359a85f9498fc864f24b7a3a0307159b6d3e663543f1defcdbc969a154`

<a id="layout18-table-28-row-5"></a>

**항목 5**

**파일**

[원본작업자료/논문/4차/work/evidence/container_readonly.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/container_readonly.py)

**종류**

.py

**바이트**

2729

**SHA-256**

`5f5f3de67bfb7d09485107c31352690427e73edc2979a5edf2be1f33e1bef422`

<a id="layout18-table-28-row-6"></a>

**항목 6**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_01.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_01.py)

**종류**

.py

**바이트**

4127

**SHA-256**

`4fa0dc8d1cfcb958a5090aed8f4845f05e5ad794cd3a7fe8b67c0d43988517a9`

<a id="layout18-table-28-row-7"></a>

**항목 7**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_03.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_03.py)

**종류**

.py

**바이트**

1394

**SHA-256**

`c54f67171b17d961b7789eb9eafe0a2494ab6804cbe5adf871932324b873f71e`

<a id="layout18-table-28-row-8"></a>

**항목 8**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_04.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_04.py)

**종류**

.py

**바이트**

3647

**SHA-256**

`d29046dbe5639d8cf54380c6fd7d9729929f21144baff979d111b8df2176e3a2`

<a id="layout18-table-28-row-9"></a>

**항목 9**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_06.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_06.py)

**종류**

.py

**바이트**

2739

**SHA-256**

`c4829d3da01e92090bf37d978adca14b31f92895d06f4ae8ce7df9b9d4186149`

<a id="layout18-table-28-row-10"></a>

**항목 10**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_08.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_08.py)

**종류**

.py

**바이트**

3789

**SHA-256**

`ff6e52dac5030eeec279c0d8078aed6219345aa2c46eb79b07fb9676d7e2da73`

<a id="layout18-table-28-row-11"></a>

**항목 11**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_10.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_10.py)

**종류**

.py

**바이트**

1188

**SHA-256**

`8676e423e0b658be4a5699dd7ad9b037e5b51cd6ddf289f223aa9b44020a727f`

<a id="layout18-table-28-row-12"></a>

**항목 12**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_12.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_12.py)

**종류**

.py

**바이트**

1322

**SHA-256**

`3f37601042220db3b6b944b7688a0427ebdead07c328d7011dbb033b40f4c004`

<a id="layout18-table-28-row-13"></a>

**항목 13**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_14.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_14.py)

**종류**

.py

**바이트**

4129

**SHA-256**

`41df59dcdd1690890c85244532477d81d4455172318060fc3d545a1a31d34222`

<a id="layout18-table-28-row-14"></a>

**항목 14**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_16.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_16.py)

**종류**

.py

**바이트**

4152

**SHA-256**

`ac33bc5c969feb669ad2a2bf725803bd44ba451b1b189fc02fa0b3bd37ad2840`

<a id="layout18-table-28-row-15"></a>

**항목 15**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_18.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_18.py)

**종류**

.py

**바이트**

3399

**SHA-256**

`da1fa465e55b5b8a53eab83c53b5dcaf2d1105dc6c99add9534738304e7a2d9b`

<a id="layout18-table-28-row-16"></a>

**항목 16**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_20.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_20.py)

**종류**

.py

**바이트**

3218

**SHA-256**

`8da48e2214d853593639d0efc9a1106611ed82bb7d823594a1de3b6d8ad9b3de`

<a id="layout18-table-28-row-17"></a>

**항목 17**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_22.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_22.py)

**종류**

.py

**바이트**

1521

**SHA-256**

`85af7852c25f6b6dc67b0a8933ee5cac5e31480d7f31b426d729df58967b997c`

<a id="layout18-table-28-row-18"></a>

**항목 18**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_24.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_24.py)

**종류**

.py

**바이트**

2009

**SHA-256**

`5cbae2d11991a6e930068bece2f1ebb8a129a739b75b61b1f2cdcf1d5c247ad1`

<a id="layout18-table-28-row-19"></a>

**항목 19**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_26.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_26.py)

**종류**

.py

**바이트**

4528

**SHA-256**

`7c4ab9835d97cbe1d0d6f97f8f6e2e2b3c382b4caf17426dd88a34853405320d`

<a id="layout18-table-28-row-20"></a>

**항목 20**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_28.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_28.py)

**종류**

.py

**바이트**

1811

**SHA-256**

`4dec7aa81995939d0bcb0b2185bd6b324bc3850fb587ccb2a48e656450bf6dea`

<a id="layout18-table-28-row-21"></a>

**항목 21**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_30.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_30.py)

**종류**

.py

**바이트**

36779

**SHA-256**

`4a84a56cb7fceb2309b2732f08b8abe2a9dc169218e2c4a05867b76b22fe6299`

<a id="layout18-table-28-row-22"></a>

**항목 22**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_32.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_32.py)

**종류**

.py

**바이트**

6213

**SHA-256**

`37c420449e4170701dec73f875498021e11fa42e545b9d9917358c23207ca4dd`

<a id="layout18-table-28-row-23"></a>

**항목 23**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_34.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_34.py)

**종류**

.py

**바이트**

8950

**SHA-256**

`ab1815b25b625b1e4f4d8f22929573b3589289b1df413eb1dceacde82bb21078`

<a id="layout18-table-28-row-24"></a>

**항목 24**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_36.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_36.py)

**종류**

.py

**바이트**

835

**SHA-256**

`3f645ba36af67a6b7335243937d216cc030fe52a33853804b5a045a3b73f06d6`

<a id="layout18-table-28-row-25"></a>

**항목 25**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_38.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_38.py)

**종류**

.py

**바이트**

203

**SHA-256**

`2c5c22b47b8749d258438928847d54db7a0a174fbb82802cfd6902764e740c09`

<a id="layout18-table-28-row-26"></a>

**항목 26**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_40.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_40.py)

**종류**

.py

**바이트**

245

**SHA-256**

`044cdda32def1c8e7d3a18822cb522c0cd01a1b15298f17eb3afb2006bd2408d`

<a id="layout18-table-28-row-27"></a>

**항목 27**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_42.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_42.py)

**종류**

.py

**바이트**

205

**SHA-256**

`f4c07a5f31400a3223aa6fb91f852d9f5f8cfb65800eec2bd0476e9d50d4d85b`

<a id="layout18-table-28-row-28"></a>

**항목 28**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_44.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_44.py)

**종류**

.py

**바이트**

245

**SHA-256**

`d4d8b750340802aee40b09aa9a75e50c2dd648709f7bac925281bbd62c48354a`

<a id="layout18-table-28-row-29"></a>

**항목 29**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_46.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_46.py)

**종류**

.py

**바이트**

4058

**SHA-256**

`8d116612c8a7ba101f5bf97dc1693873eadc28b2c7448536da4857dec67fd7b3`

<a id="layout18-table-28-row-30"></a>

**항목 30**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_48.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_48.py)

**종류**

.py

**바이트**

4674

**SHA-256**

`675d3c3f2db513fe76b703b69f90872b30466d753cfa4262669f4dc462675e5b`

<a id="layout18-table-28-row-31"></a>

**항목 31**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_51.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_51.py)

**종류**

.py

**바이트**

5135

**SHA-256**

`39340c112c5cec0194f3483f33e1883219402f3938dcd56ce7f966c6544c05ac`

<a id="layout18-table-28-row-32"></a>

**항목 32**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_53.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_53.py)

**종류**

.py

**바이트**

1725

**SHA-256**

`5f9560f2449fe4b27505052c1c13dae62edbc1e35ac43e06075b3ba893b4fa6c`

<a id="layout18-table-28-row-33"></a>

**항목 33**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_55.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_55.py)

**종류**

.py

**바이트**

20559

**SHA-256**

`7088eab66a8164ad32d035d04a836b7b50769cba849994652dc268999b86454d`

<a id="layout18-table-28-row-34"></a>

**항목 34**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_57.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_57.py)

**종류**

.py

**바이트**

13286

**SHA-256**

`aacf9ef4b13e381b26209eb34312d0f57253aea7c2583e4f6d76a20440c2e951`

<a id="layout18-table-28-row-35"></a>

**항목 35**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_58.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_58.py)

**종류**

.py

**바이트**

4850

**SHA-256**

`38708a830269e0ca457f3de440b604c8fbd077333b43ad79ba80d42f27ad18fb`

<a id="layout18-table-28-row-36"></a>

**항목 36**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_60.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_60.py)

**종류**

.py

**바이트**

1582

**SHA-256**

`3f48d1454fe9aa108147423dc3eaaf4bee1818b34d44e199cdaaaf689fac5488`

<a id="layout18-table-28-row-37"></a>

**항목 37**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_61.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_61.py)

**종류**

.py

**바이트**

3600

**SHA-256**

`434a431747e347ad662c4bf073cc35600dc98f9dc413a02098eb32c66facc28b`

<a id="layout18-table-28-row-38"></a>

**항목 38**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_62.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_62.py)

**종류**

.py

**바이트**

2448

**SHA-256**

`cd50df02812b63164971c80e45b78ac36c980dc11c7f32b4f8eeb7bbf6682daa`

<a id="layout18-table-28-row-39"></a>

**항목 39**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_63.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_63.py)

**종류**

.py

**바이트**

1186

**SHA-256**

`5809532940e18bea66694e5a8024522e231bc84b14b7bb24bb78c485fa54dc23`

<a id="layout18-table-28-row-40"></a>

**항목 40**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_65.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_65.py)

**종류**

.py

**바이트**

6754

**SHA-256**

`7e4054e2cdbc015db2cb7f4b0a11ef3b305e3c80d377a9a5eb51fcec008ba200`

<a id="layout18-table-28-row-41"></a>

**항목 41**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_66.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_66.py)

**종류**

.py

**바이트**

7285

**SHA-256**

`6326593ba272c497a9fde4fa7fbc61e31fc3d5e6233aec392a2d579fec0f6f03`

<a id="layout18-table-28-row-42"></a>

**항목 42**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_67.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_67.py)

**종류**

.py

**바이트**

3810

**SHA-256**

`96486facb829716afded68960720255f6523b49837a76e4171ec3427d497b38c`

<a id="layout18-table-28-row-43"></a>

**항목 43**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_69.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_69.py)

**종류**

.py

**바이트**

7373

**SHA-256**

`ac3d5bb06e21ab6151ea971944e379f0d3a9398285b2bde4e36bf08262c54468`

<a id="layout18-table-28-row-44"></a>

**항목 44**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_71.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_71.py)

**종류**

.py

**바이트**

7174

**SHA-256**

`734baffa5896f5a5a4ac631a59140d1613a046c424e95658ae56462a854a443e`

<a id="layout18-table-28-row-45"></a>

**항목 45**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_72.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_72.py)

**종류**

.py

**바이트**

5431

**SHA-256**

`01e694b71e8f78660fde6bae5ddde1fb72978e89278eee0c5963d05518eab216`

<a id="layout18-table-28-row-46"></a>

**항목 46**

**파일**

[원본작업자료/논문/4차/work/evidence/notebook_cell_74.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/notebook_cell_74.py)

**종류**

.py

**바이트**

3086

**SHA-256**

`ecb09c737b469bd66b9688531f22db44f699907a32473576854f46af11257bfd`

<a id="layout18-table-28-row-47"></a>

**[원본작업자료/논문/4차/work/evidence/recompute_saved.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/recompute_saved.py)**

**파일**

[원본작업자료/논문/4차/work/evidence/recompute_saved.py](../../%EC%9B%90%EB%B3%B8%EC%9E%91%EC%97%85%EC%9E%90%EB%A3%8C/%EB%85%BC%EB%AC%B8/4%EC%B0%A8/work/evidence/recompute_saved.py)

**종류**

.py

**바이트**

8308

**SHA-256**

`5b8ef5c8e768941c813d95d83b523a9908284e977930be476bc33790dfb82f83`


</details>

---

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [자료 폴더](../../%EB%85%BC%EB%AC%B8/4%EC%B0%A8/tools) · [논문 3차](paper-3.md) · [논문 5차 · 재구성 패키지](paper-5.md)
