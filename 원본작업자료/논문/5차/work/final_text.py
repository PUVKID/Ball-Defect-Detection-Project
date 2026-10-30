import json,pathlib
p=pathlib.Path('work/content.json');c=json.loads(p.read_text(encoding='utf8'));a=c['pages'][2][1]
a[0][1]=a[0][1].replace('외부 평가 폴드와 그룹 중복은 없지만 내부 학습·검증 사이에는 폴드별 9~20개 중복 그룹이 존재하였다.','외부 평가와 중복은 없으나 내부 학습·검증 간에는 9~20개 중복 그룹이 있었다.')
a[1][1]=a[1][1].replace('독립 현장 정답이 없고 동일 데이터에서 여러 전처리를 탐색했으므로 탐색적 비교로 해석한다.','독립 현장 정답 없이 같은 데이터에서 필터를 탐색했으므로 탐색적 비교로 해석한다.')
p.write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf8')
