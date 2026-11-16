"""Build the management media pack from its editable JSON source.
Media-only dependencies: pillow python-pptx edge-tts imageio-ffmpeg.
Run: python scripts/build_company_presentation.py [--work-dir PATH]
Only narration text is sent to Microsoft's online Edge speech service.
"""
import argparse, asyncio, hashlib, html, json, re, subprocess, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import edge_tts, imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1]; DOC=ROOT/'docs'
p=argparse.ArgumentParser();p.add_argument('--work-dir',default='/tmp/big-tiny-company');args=p.parse_args()
WORK=Path(args.work_dir);WORK.mkdir(parents=True,exist_ok=True)
slides=json.loads((DOC/'company-presentation-slides.json').read_text());ff=imageio_ffmpeg.get_ffmpeg_exe()
BG='#101f2b';FG='#f3f5ef';MUTED='#b8c9ce';TEAL='#5cdbc0';GOLD='#ecc879'
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
prs=Presentation();prs.slide_width=Inches(16);prs.slide_height=Inches(9)
def run(cmd):return subprocess.run(cmd,check=True,capture_output=True,text=True)
def duration(path):
 r=subprocess.run([ff,'-i',str(path)],capture_output=True,text=True)
 m=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',r.stderr);return int(m[1])*3600+int(m[2])*60+float(m[3])
def stamp(s):
 n=round(s*1000);h,n=divmod(n,3600000);m,n=divmod(n,60000);sec,ms=divmod(n,1000);return f'{h:02}:{m:02}:{sec:02},{ms:03}'
def clock(s):return f'{int(s)//60:02}:{int(s)%60:02}'
async def speech():
 sem=asyncio.Semaphore(3)
 async def one(i,s):
  path=WORK/f'{i:02}.mp3';key=hashlib.sha256((s['narration']+'en-SG-LunaNeural-5%').encode()).hexdigest();cache=path.with_suffix('.sha')
  if path.exists() and cache.exists() and cache.read_text()==key:return
  async with sem:
   for attempt in range(3):
    try:
     await edge_tts.Communicate(s['narration'],'en-SG-LunaNeural',rate='-5%').save(str(path));cache.write_text(key);print('voice',i,flush=True);return
    except Exception:
     if attempt==2:raise
     await asyncio.sleep(2)
 await asyncio.gather(*(one(i,s) for i,s in enumerate(slides,1)))
asyncio.run(speech())
transcript=['# Big Tiny: AI across the business','','28-slide management discussion · 16 November 2026','', '[Narrated MP4](company-presentation.mp4) · [Editable PowerPoint](company-presentation.pptx) · [Browser slides](company-presentation.html) · [Subtitles](company-presentation.srt)','', 'Female synthetic Singapore English narration: Microsoft en-SG-LunaNeural, generated with edge-tts. Only the public presentation script was sent to the online speech service. Departmental use cases and benefits are proposals; internal structures, data availability and productivity gains have not been verified. The earlier real-GX10 demonstration is preserved in [executive-demo.mp4](executive-demo.mp4).','']
srt=[];timeline=[];time=0;segments=[];htmlslides=[]
for i,s in enumerate(slides,1):
 im=Image.new('RGB',(1920,1080),BG);draw=ImageDraw.Draw(im)
 slide=prs.slides.add_slide(prs.slide_layouts[6]);slide.background.fill.solid();slide.background.fill.fore_color.rgb=RGBColor.from_string(BG[1:])
 def block(txt,x,y,w,size,color=FG,heavy=False):
  f=ImageFont.truetype(bold if heavy else font,size);lines=[]
  for para in txt.split('\n'):
   line=''
   for word in para.split():
    candidate=(line+' '+word).strip()
    if draw.textlength(candidate,font=f)>w and line:lines.append(line);line=word
    else:line=candidate
   lines.append(line)
  for j,line in enumerate(lines):draw.text((x,y+j*size*1.28),line,font=f,fill=color)
  box=slide.shapes.add_textbox(Inches(x/120),Inches(y/120),Inches(w/120),Inches((len(lines)*size*1.28+16)/120));tf=box.text_frame;tf.word_wrap=False
  for j,line in enumerate(lines):
   q=tf.paragraphs[0] if j==0 else tf.add_paragraph();q.text=line;q.font.name='DejaVu Sans';q.font.size=Pt(size*.6);q.font.bold=heavy;q.font.color.rgb=RGBColor.from_string(color[1:]);q.space_after=Pt(0)
  return y+len(lines)*size*1.28
 block('BIG TINY  /  AI ACROSS THE BUSINESS',85,43,1600,22,TEAL,True)
 block(s['section'],85,100,1700,24,GOLD,True)
 block(s['title'],85,157,1730,58,FG,True)
 block('THE TOOL / OUTPUT',85,343,1700,22,TEAL,True)
 end=block(s['example'],85,382,1720,32)
 if end>510:raise ValueError(f'Example overflow slide {i}: {end}')
 for label,key,x,w in [('FOR STAFF','staff',85,810),('FOR CUSTOMERS / PARTNERS','customer',1000,820)]:
  block(label,x,540,w,22,TEAL,True);end=block(s[key],x,578,w,30)
  if end>730:raise ValueError(f'Benefits overflow slide {i}')
 block('DATA NEEDED',85,743,250,20,GOLD,True);end=block(s['inputs'],360,740,1465,24,MUTED)
 if end>825:raise ValueError(f'Inputs overflow slide {i}')
 block('HUMAN DECISION',85,826,260,20,GOLD,True);end=block(s['approval'],360,823,1465,24,MUTED)
 if end>910:raise ValueError(f'Approval overflow slide {i}')
 block('VALUE TEST',85,922,250,20,TEAL,True);block(s['metric'],360,919,1465,24,MUTED)
 block(f'MANAGEMENT DISCUSSION  •  16 NOV 2026                                                   {i:02} / {len(slides)}',85,1020,1750,20,MUTED)
 png=WORK/f'{i:02}.png';im.save(png)
 slide.notes_slide.notes_text_frame.text=s['narration']+'\n\nPublic context sources: https://www.bigtiny.com.sg/ ; https://www.bigtiny.com.sg/aboutbigtiny ; https://www.owntinyhouse.sg/ . Proposed functional map; not a confirmed internal organisation chart.'
 audio=WORK/f'{i:02}.mp3';voice_duration=duration(audio);dur=voice_duration+1.2
 timeline.append({'slide':i,'start':time,'duration':dur,'narration_duration':voice_duration,'title':s['title'].replace('\n',' ')})
 # Short, readable subtitle cues rather than a full paragraph on screen.
 chunks=textwrap.wrap(s['narration'],94);weights=[len(c) for c in chunks];offset=time
 for chunk,weight in zip(chunks,weights):
  span=voice_duration*weight/sum(weights);srt.append(f'{len(srt)+1}\n{stamp(offset)} --> {stamp(offset+span)}\n'+ '\n'.join(textwrap.wrap(chunk,48))+'\n');offset+=span
 transcript += [f"## {clock(time)} · {i:02} · {s['title'].replace(chr(10),' ')}",'',s['narration'],'',f"**Example:** {s['example']}",'',f"**Data:** {s['inputs']}",'',f"**Human decision:** {s['approval']}",'',f"**Staff:** {s['staff']} **Customer:** {s['customer']}",'',f"**Evaluate:** {s['metric']}",'']
 seg=WORK/f'{i:02}.mp4';segments.append(seg)
 run([ff,'-y','-v','error','-loop','1','-framerate','10','-i',str(png),'-i',str(audio),'-t',str(dur),'-vf','format=yuv420p','-c:v','libx264','-preset','ultrafast','-tune','stillimage','-crf','25','-c:a','aac','-b:a','128k','-af','apad','-movflags','+faststart',str(seg)])
 print('rendered',i,clock(time),flush=True);time+=dur
 def e(key):return html.escape(s[key]).replace('\n','<br>')
 htmlslides.append(f'<section><small>{e("section")}</small><h1>{e("title")}</h1><h3>THE TOOL / OUTPUT</h3><p class="example">{e("example")}</p><div class="benefits"><article><h3>FOR STAFF</h3><p>{e("staff")}</p></article><article><h3>FOR CUSTOMERS / PARTNERS</h3><p>{e("customer")}</p></article></div><dl><dt>Data needed</dt><dd>{e("inputs")}</dd><dt>Human decision</dt><dd>{e("approval")}</dd><dt>Value test</dt><dd>{e("metric")}</dd></dl><details><summary>Narration</summary><p>{e("narration")}</p></details><footer>{i:02} / 28 · MANAGEMENT DISCUSSION</footer></section>')
prs.save(DOC/'company-presentation.pptx')
(DOC/'company-presentation.srt').write_text('\n'.join(srt))
transcript[3:3]=[f'Duration: {clock(time)} · 1920 × 1080 H.264 + AAC · 28 slides.','']
transcript+=['## Sources and interpretation','','Public company context (checked 16 November 2026): [Big Tiny](https://www.bigtiny.com.sg/), [About Big Tiny](https://www.bigtiny.com.sg/aboutbigtiny), [Own Tiny House](https://www.owntinyhouse.sg/). These establish public business context, not internal systems, confirmed departmental ownership or measured AI results. The proposed functional map is for validation with department heads.','','[Detailed use-case catalogue](company-use-cases.md) · [Editable slide source](company-presentation-slides.json) · [Build script](../scripts/build_company_presentation.py)','']
(DOC/'company-presentation.md').write_text('\n'.join(transcript))
(WORK/'timeline.json').write_text(json.dumps(timeline,indent=2))
(WORK/'concat.txt').write_text('\n'.join(f"file '{x}'" for x in segments))
metadata=[';FFMETADATA1','title=Big Tiny - AI across the business']
for t in timeline:metadata+=['[CHAPTER]','TIMEBASE=1/1000',f'START={round(t["start"]*1000)}',f'END={round((t["start"]+t["duration"])*1000)}','title='+t['title']]
(WORK/'chapters.txt').write_text('\n'.join(metadata))
run([ff,'-y','-v','error','-f','concat','-safe','0','-i',str(WORK/'concat.txt'),'-f','ffmetadata','-i',str(WORK/'chapters.txt'),'-i',str(DOC/'company-presentation.srt'),'-map','0:v','-map','0:a','-map','2:0','-map_metadata','1','-map_chapters','1','-c:v','copy','-c:a','copy','-c:s','mov_text','-metadata:s:s:0','language=eng','-movflags','+faststart',str(DOC/'company-presentation.mp4')])
# The bundled FFmpeg 8 muxer may write QT chapter references to track ID zero
# when chapters and mov_text subtitles coexist, while its valid Nero chpl atom
# contains all chapters. Neutralise only those invalid zero-ID references in
# place. Same-size free atoms preserve every sample offset and media byte.
def repair_zero_chapter_references(path):
 import struct
 data=bytearray(path.read_bytes());repairs=0
 def walk(lo,hi):
  nonlocal repairs
  while lo+8<=hi:
   size,tag=struct.unpack_from('>I4s',data,lo)
   if size<8 or lo+size>hi:break
   if tag==b'chap' and size==12 and data[lo+8:lo+12]==b'\0'*4:
    data[lo+4:lo+8]=b'free';repairs+=1
   if tag in (b'moov',b'trak',b'tref'):walk(lo+8,lo+size)
   lo+=size
 walk(0,len(data))
 if repairs:path.write_bytes(data)
 return repairs
print('Repaired invalid zero-ID chapter references:',repair_zero_chapter_references(DOC/'company-presentation.mp4'),flush=True)
Image.open(WORK/'01.png').save(DOC/'company-presentation-cover.jpg',quality=90)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Big Tiny — AI across the business</title><style>body{margin:0;background:#101f2b;color:#f3f5ef;font:20px system-ui}section{box-sizing:border-box;max-width:1280px;min-height:100vh;padding:48px 6vw;margin:auto;border-bottom:1px solid #46606b;scroll-snap-align:start}small{color:#ecc879;letter-spacing:.08em}h1{font-size:clamp(32px,4vw,58px);line-height:1.12;margin:24px 0}h3{font-size:15px;letter-spacing:.08em;color:#5cdbc0}.example{font-size:26px}.benefits{display:grid;grid-template-columns:1fr 1fr;gap:40px}dl{display:grid;grid-template-columns:170px 1fr;gap:16px;font-size:17px;color:#b8c9ce}dt{color:#ecc879}dd{margin:0}footer{font-size:13px;color:#b8c9ce;margin-top:30px}details{font-size:16px}nav{position:fixed;bottom:12px;right:15px;z-index:3}button{background:#5cdbc0;border:0;padding:12px;margin:3px;cursor:pointer}a{color:#5cdbc0}@media(max-width:650px){.benefits{grid-template-columns:1fr;gap:0}dl{grid-template-columns:1fr;gap:8px}section{padding:28px}}</style><nav><button onclick="move(-1)" aria-label="Previous slide">←</button><button onclick="move(1)" aria-label="Next slide">→</button></nav>'''+''.join(htmlslides)+'''<section><h1>Sources and supporting material</h1><p>Public business context: <a href="https://www.bigtiny.com.sg/">Big Tiny</a>, <a href="https://www.bigtiny.com.sg/aboutbigtiny">About Big Tiny</a>, <a href="https://www.owntinyhouse.sg/">Own Tiny House</a>. Checked 16 November 2026. Functional map and benefits are proposals, not a confirmed organisation chart or measured results.</p><p><a href="company-presentation.mp4">Narrated video</a> · <a href="company-presentation.pptx">Editable PowerPoint</a> · <a href="company-presentation.md">Chapter transcript</a></p></section><script>function move(d){let a=[...document.querySelectorAll('section')];let i=a.reduce((best,s,j)=>Math.abs(s.getBoundingClientRect().top)<Math.abs(a[best].getBoundingClientRect().top)?j:best,0);a[Math.max(0,Math.min(a.length-1,i+d))].scrollIntoView({behavior:'smooth'});}addEventListener('keydown',e=>{if(['ArrowRight','PageDown','ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();move(['ArrowRight','PageDown'].includes(e.key)?1:-1)}})</script></html>'''
(DOC/'company-presentation.html').write_text(page)
run([ff,'-v','error','-i',str(DOC/'company-presentation.mp4'),'-f','null','-'])
print(json.dumps({'slides':len(slides),'duration_seconds':duration(DOC/'company-presentation.mp4'),'size_bytes':(DOC/'company-presentation.mp4').stat().st_size,'full_decode':'passed'}),flush=True)
