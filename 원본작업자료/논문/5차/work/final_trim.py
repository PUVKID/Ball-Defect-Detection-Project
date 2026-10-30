import pathlib,json
p=pathlib.Path('work/content.json');c=json.loads(p.read_text(encoding='utf8'))
a=c['pages'][2][1]
a[1][1]='독립 현장 정답 없이 같은 데이터에서 필터를 탐색한 결과이다. 신뢰구간은 시드 불확실성과 다중 비교를 모두 반영하지 않는다. 촬영 시점·로트별 외부 평가와 내부 검증의 그룹 분리가 필요하다.'
p.write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf8')
