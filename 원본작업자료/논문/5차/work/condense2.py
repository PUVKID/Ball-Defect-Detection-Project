import json,pathlib
p=pathlib.Path('work/content.json');c=json.loads(p.read_text(encoding='utf8'));a=c['pages']
a[1][0][5][1]=a[1][0][5][1].replace('반전·크기·위치·밝기 증강을 공통 적용하였다. ','공통 증강을 적용하였다. ')
a[1][1][0][1]=a[1][1][0][1].replace('주요 전처리 설정은 ','').replace('25% 학습 조건은 폴드당 약 90장을 사용한다. ','소량 학습에는 폴드당 약 90장을 썼다. ').replace('부품 영역과 판정 기준은 원영상에서 구한 값을 유지한다.','부품 영역은 원영상의 값을 유지한다.')
a[1][1][3][1]='시드 42·43·44로 폴드·검증 분할, 학습 난수와 잡음을 바꾸어 평균±표본 표준편차를 구했다. 신뢰구간은 영상별 시드 평균 차이를 유사 영상 그룹 단위로 5,000회 재표집한 95% 구간이다.'
a[2][1][5][1]='[1] G. Jocher, A. Chaurasia, and J. Qiu, “Ultralytics YOLOv8,” software, 2023.'
p.write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf8')
