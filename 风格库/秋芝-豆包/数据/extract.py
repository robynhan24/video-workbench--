from pathlib import Path
import cv2,json
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).parent
src=r'D:\Robyn\G---动物救援youtube\NN 抖音视频下载\03 秋芝-豆包.mp4'
cap=cv2.VideoCapture(src)
out=root/'frames';out.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',20)
for t in range(491):
    cap.set(cv2.CAP_PROP_POS_MSEC,t*1000)
    ok,frame=cap.read()
    if not ok:continue
    im=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
    im.resize((960,540)).save(out/f'{t:03}.jpg',quality=88)
for start in range(0,491,60):
    times=list(range(start,min(start+60,491),3))
    sheet=Image.new('RGB',(1920,300*((len(times)+3)//4)),'#151515')
    draw=ImageDraw.Draw(sheet)
    for i,t in enumerate(times):
        x=(i%4)*480;y=(i//4)*300
        sheet.paste(Image.open(out/f'{t:03}.jpg').resize((480,270)),(x,y))
        draw.text((x+8,y+272),f'{t//60:02}:{t%60:02} ({t}s)',font=font,fill='white')
    sheet.save(root/f'overview_{start:03}.jpg',quality=92)
print('extracted',len(list(out.glob('*.jpg'))))
