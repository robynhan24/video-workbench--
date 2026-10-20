import os,json,whisper
from pathlib import Path
root=Path(__file__).parent
os.environ['PATH']=r'D:\deskclaw\tools\ffmpeg\bin;'+os.environ['PATH']
model=whisper.load_model(r'D:\deskclaw\C-drive-cleanup-quarantine-20260702-142242\user_cache_whisper\base.pt')
result=model.transcribe(str(root/'audio.mp3'),language='zh',word_timestamps=True,fp16=False,verbose=False)
(root/'asr_local.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'transcript.txt').write_text('\n'.join(f"[{s['start']:.2f}-{s['end']:.2f}] {s['text']}" for s in result['segments']),encoding='utf-8')
