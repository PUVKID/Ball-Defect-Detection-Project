import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';
import {GlobalFonts} from '@napi-rs/canvas';
GlobalFonts.registerFromPath('C:/Users/PUVKID/AppData/Local/Microsoft/Windows/Fonts/NanumGothicBold.ttf');
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const p=await PresentationFile.importPptx(await FileBlob.load(path.join(root,'결과/추계학술대회_10분발표.pptx')));
for(const [i,s] of p.slides.items.entries()){
 const png=await p.export({slide:s,format:'png',scale:1.5});
 await fs.writeFile(path.join(root,'work/render',`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
 const layout=await s.export({format:'layout'});await fs.writeFile(path.join(root,'work/render',`slide-${String(i+1).padStart(2,'0')}.layout.json`),await layout.text());
}
console.log('최종 PPTX 재가져오기와 전체 15장 렌더 완료');
