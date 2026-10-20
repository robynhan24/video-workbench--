from pathlib import Path
import json,re,shutil,statistics,csv
from PIL import Image,ImageDraw,ImageFont
work=Path(__file__).parent
dest=Path(r'D:\deskclaw\video-workbench-style-20261020\风格库\秋芝-豆包')
for sub in ['数据','拆解/全片概览','拆解/逐秒画面','拆解/重点拆解']:
    (dest/sub).mkdir(parents=True,exist_ok=True)
asr=json.loads((work/'asr_local.json').read_text(encoding='utf-8'))
shutil.copy2(work/'asr_local.json',dest/'数据/秋芝-豆包_机器转写.json')
shutil.copy2(work/'transcript.txt',dest/'数据/秋芝-豆包_机器转写.txt')
for p in work.glob('overview*.jpg'):shutil.copy2(p,dest/'拆解/全片概览'/p.name)
times=[3,6,15,24,36,45,57,66,87,108,129,156,180,210,234,252,300,321,339,375,405,447,462,477,480]
for t in times:shutil.copy2(work/f'frames/{t:03}.jpg',dest/f'拆解/重点拆解/{t:03}s.jpg')
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17)
for start in range(0,491,24):
    sheet=Image.new('RGB',(1920,360*6),'#151515');draw=ImageDraw.Draw(sheet)
    for i,t in enumerate(range(start,min(start+24,491))):
        x=i%4*480;y=i//4*360
        sheet.paste(Image.open(work/f'frames/{t:03}.jpg').resize((480,270)),(x,y))
        draw.text((x+6,y+273),f'{t//60:02}:{t%60:02} | {t}s',font=font,fill='#c7ff22')
        seg=next((s['text'] for s in asr['segments'] if s['start']<=t<s['end']),'')
        for n in range(0,min(len(seg),78),26):
            draw.text((x+6,y+297+(n//26)*19),seg[n:n+26],font=font,fill='white')
    sheet.save(dest/f'拆解/逐秒画面/S{start//24:02}.jpg',quality=88)
cuts=[float(x) for x in re.findall(r'pts_time:([0-9.]+)',(work/'scene_detect.log').read_text(encoding='utf-8'))]
intervals=[b-a for a,b in zip([0]+cuts,cuts+[490.52])]
chars=len(re.findall(r'[\u4e00-\u9fff]',asr['text']))
host={12,15,18,21,42,51,72,75,78,216,219,222,225,312,315,324,327,465,468,471,474,480,483,486,489}
with (dest/'数据/主播全屏_3秒抽样.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.writer(f);writer.writerow(['time_s','host_main_visual'])
    for t in range(0,491,3):writer.writerow([t,int(t in host)])
stats={'duration_s':490.52,'width':1920,'height':1080,'fps':30,'source_bytes':37749141,
       'scene_detection':{'method':'FFmpeg scale=320:-1,select=gt(scene,0.25); candidates, not validated cuts or all visual changes','candidate_count':len(cuts),'per_minute':len(cuts)/490.52*60,'median_interval_s':statistics.median(intervals),'max_interval_s':max(intervals)},
       'host_main_visual_sampling':{'interval_s':3,'samples':164,'host_samples':len(host),'percent':len(host)/164*100,'meaning':'Manual review of sampled frames; includes host with overlays, excludes circular PIP; not exact screen-time'},
       'asr':{'model':'OpenAI Whisper base (local)','han_characters':chars,'han_characters_per_total_minute':chars/490.52*60,'status':'uncorrected machine transcription; not exact speaking rate'},
       'original_mix_loudness':{'integrated_lufs':-13.53,'true_peak_dbtp':1.70,'lra_lu':3.9,'method':'FFmpeg loudnorm on original source audio; no source separation'},
       'not_measured':['isolated_music_gain','music_BPM','impact_count','frame_accurate_host_duration','validated_cut_count','exact_font_name']}
(dest/'数据/节奏统计.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
(dest/'数据/候选切点.txt').write_text('# 自动场景变化候选；阈值 0.25，非人工确认剪切点\n'+'\n'.join(f'{t:.3f}' for t in cuts),encoding='utf-8')
shutil.copy2(work/'loudness_original.log',dest/'数据/原片响度测量.log')
for p in ['extract.py','transcribe.py','package.py']:shutil.copy2(work/p,dest/'数据'/p)
print(json.dumps(stats,ensure_ascii=False,indent=2))
