from pathlib import Path
import json, math, re, shutil, html, argparse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
import fitz

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT
W,H=432,648
for folder in ['ARTES','EDITAVEIS','COLORIDAS','PROVAS','ORIGINAIS']:
    (OUT/folder).mkdir(parents=True,exist_ok=True)
for name,file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Title','DejaVuSerif.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
BG='#101010'; GOLD='#E2BD78'; WHITE='#F4EEE3'; MUTED='#C6BCA9'; LINE='#725936'; RED='#32191D'

class Plate:
    def __init__(self,slug,title,subtitle='',tag='MÉTODO POSICIONE-SE · SOL LIMA'):
        self.slug=slug; self.title=title; self.subtitle=subtitle
        self.pdf=OUT/'PROVAS'/f'{slug}.pdf'
        self.c=canvas.Canvas(str(self.pdf),pagesize=(W,H))
        self.c.setTitle(title+' | Reposicione-se'); self.c.setAuthor('Sol Lima')
        self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="1800" height="2700">',f'<title>{html.escape(title)}</title>',f'<desc>{html.escape(subtitle)}</desc>']
        self.rect(0,0,W,H,BG)
        self.text(tag,30,29,8.1,'Bold',GOLD)
        title_size=25
        while pdfmetrics.stringWidth(title,'Title',title_size)>372:
            title_size-=.5
        y=self.text(title,30,65,title_size,'Title',GOLD,372)
        if subtitle: self.text(subtitle,30,y+19,10.1,'Body',MUTED,372)
        self.line(30,110,402,110,LINE,.7)
    def rect(self,x,y,w,h,fill=None,stroke=None,r=0):
        self.c.setFillColor(HexColor(fill or BG)); self.c.setStrokeColor(HexColor(stroke or fill or BG))
        self.c.setLineWidth(.7)
        self.c.roundRect(x,H-y-h,w,h,r,stroke=int(bool(stroke)),fill=int(bool(fill)))
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill or "none"}" stroke="{stroke or "none"}" stroke-width=".7"/>')
    def line(self,x1,y1,x2,y2,color=GOLD,width=1):
        self.c.setStrokeColor(HexColor(color));self.c.setLineWidth(width);self.c.line(x1,H-y1,x2,H-y2)
        self.svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>')
    def circle(self,x,y,r,fill=RED,stroke=GOLD):
        self.c.setFillColor(HexColor(fill));self.c.setStrokeColor(HexColor(stroke));self.c.circle(x,H-y,r,stroke=1,fill=1)
        self.svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}"/>')
    def text(self,s,x,y,size=11,font='Body',color=WHITE,width=None,leading=None):
        leading=leading or size*1.3; lines=[]
        for para in str(s).split('\n'):
            line=''
            for word in para.split(' '):
                test=(line+' '+word).strip()
                if width and line and pdfmetrics.stringWidth(test,font,size)>width:
                    lines.append(line);line=word
                else:line=test
            lines.append(line)
        self.c.setFillColor(HexColor(color));self.c.setFont(font,size)
        family='DejaVu Serif' if font=='Title' else 'DejaVu Sans'
        for i,line in enumerate(lines):
            yy=y+i*leading
            if yy>627:raise ValueError(f'Overflow {self.slug}: {line}')
            self.c.drawString(x,H-yy,line)
            self.svg.append(f'<text x="{x}" y="{yy}" fill="{color}" font-size="{size}" font-family="{family}" font-weight="{700 if font=="Bold" else 400}">{html.escape(line)}</text>')
        return y+(len(lines)-1)*leading
    def arrow(self,x1,y1,x2,y2,color=GOLD):
        self.line(x1,y1,x2,y2,color,1.1);a=math.atan2(y2-y1,x2-x1)
        for b in [-.55,.55]:self.line(x2,y2,x2-5*math.cos(a+b),y2-5*math.sin(a+b),color,1.1)
    def art(self,key,x,y,w,h):
        file=next((OUT/'ARTES').glob(key+'.*'))
        ir=ImageReader(str(file));iw,ih=ir.getSize();scale=min(w/iw,h/ih);dw,dh=iw*scale,ih*scale
        xx=x+(w-dw)/2;yy=y+(h-dh)/2
        self.c.drawImage(ir,xx,H-yy-dh,width=dw,height=dh,mask='auto')
        self.svg.append(f'<image x="{xx}" y="{yy}" width="{dw}" height="{dh}" xlink:href="../ARTES/{file.name}"/>')
    def box(self,x,y,w,h,title,body='',num=None):
        self.rect(x,y,w,h,RED,LINE,6)
        tx=x+13
        if num is not None:
            self.circle(x+20,y+21,11);self.text(str(num),x+16,y+24,9,'Bold',GOLD);tx=x+39
        end=self.text(title,tx,y+21,11.2,'Bold',GOLD,w-(tx-x)-12,13.3)
        if body:self.text(body,tx,end+17,9.4,'Body',WHITE,w-(tx-x)-12,12.5)
    def finish(self,footer='Observe. Examine. Pratique. Reveja os frutos.'):
        self.line(30,609,402,609,LINE,.6)
        self.text(footer,30,626,8,'Body',MUTED,372)
        self.c.showPage();self.c.save();self.svg.append('</svg>')
        (OUT/'EDITAVEIS'/f'{self.slug}.svg').write_text('\n'.join(self.svg))
        doc=fitz.open(self.pdf);doc[0].get_pixmap(matrix=fitz.Matrix(300/72,300/72),alpha=False).save(OUT/'COLORIDAS'/f'{self.slug}.png');doc.close()
        return self.pdf

def journey():
    p=Plate('01_mapa_da_travessia','Mapa da travessia','Sete Partes para transformar percepção em prática.')
    rows=[('I','Reconheça sua posição','Que fruto se repete? O que acontece de fato?','Cap. 1–4'),('II','Investigue o cultivo','Semente, Solo e Raízes: o que você planta e sustenta?','Cap. 5–8'),('III','Fortaleça o Tronco','Que valores, limites e acordos você pratica?','Cap. 9–12'),('IV','Observe os Galhos','Em quais áreas da vida isso aparece?','Cap. 13–16'),('V','Examine Pragas e Jaulas','O que drena, influencia ou restringe seu movimento?','Cap. 17–21'),('VI','Suba ao Mirante e filtre','Como chegou à conclusão? O que a contradiz?','Cap. 22–24'),('VII','Pode, plante e sustente','Qual passo cabe agora? Que frutos precisa rever?','Cap. 25–28')]
    for i,(part,title,q,chap) in enumerate(rows):
        y=130+i*62;p.rect(54,y,348,54,RED,LINE,5);p.circle(30,y+20,13)
        p.text(part,23 if len(part)<3 else 19,y+24,9,'Bold',GOLD)
        p.text(title,68,y+19,11.1,'Bold',GOLD,319)
        p.text(q,68,y+35,9.1,'Body',WHITE,318)
        p.text(chap,68,y+47,7.5,'Body',MUTED)
        if i<6:p.arrow(30,y+34,30,y+62-14)
    p.text('O mapa orienta a leitura. A aplicação permite voltar,\nrever hipóteses e preservar aquilo que já funciona.',30,582,10,'Body',WHITE,372)
    return p.finish('Reposicione-se · Livro completo, com apoio do Workbook.')

def cycle():
    p=Plate('02_percurso_de_aplicacao','Da percepção à prática','Um percurso para trabalhar uma situação real.')
    p.box(66,132,300,54,'1  OBSERVE UM FRUTO','Descreva o resultado, o Galho e o período.')
    p.arrow(216,186,216,205)
    p.box(66,205,300,59,'2  INVESTIGUE A ÁRVORE E O AMBIENTE','Separe fatos, hipóteses, recursos e restrições.')
    p.arrow(216,264,216,283)
    p.box(66,283,300,67,'3  PASSE PELO FILTRO','O que sustenta e contradiz sua leitura?\nHá condições para um movimento possível?')
    p.line(216,350,216,363);p.line(116,363,316,363);p.arrow(116,363,116,383);p.arrow(316,363,316,383)
    p.box(30,383,178,79,'SIM: PRATIQUE','Converse, ajuste um acordo, faça uma Poda específica ou plante uma nova atitude.')
    p.box(224,383,178,79,'AINDA NÃO: PREPARE','Busque informação, recurso ou apoio. Defina o que falta e quando revisar.')
    p.line(116,462,116,480);p.line(316,462,316,480);p.line(116,480,316,480);p.arrow(216,480,216,497)
    p.box(66,497,300,60,'4  REVEJA OS FRUTOS','O que mudou? O que manter? O que ajustar?\nCompare o resultado com o registro inicial.')
    p.line(66,529,17,529);p.line(17,529,17,158);p.arrow(17,158,66,158)
    p.text('Cada volta incorpora experiência e novos dados.',45,588,10.1,'Body',GOLD,357)
    return p.finish('Preparar condições também é uma ação do método.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');args=parser.parse_args()
    pages=[journey(),cycle()]
    merged=fitz.open()
    for file in pages:
        with fitz.open(file) as src:merged.insert_pdf(src)
    merged.save(OUT/'Mapas_da_Travessia_Coloridos.pdf',deflate=True);merged.close()
    print(json.dumps({'pages':len(pages),'output':str(OUT)},ensure_ascii=False))
