import sys,json
from PIL import Image, ImageFilter, ImageDraw
def blur(src,dst,boxes):
    im=Image.open(src).convert('RGB')
    for (x0,y0,x1,y1) in boxes:
        w=x1-x0; r=max(4,w/13)
        bl=im.filter(ImageFilter.GaussianBlur(r))
        m=Image.new('L',im.size,0); ImageDraw.Draw(m).ellipse([x0,y0,x1,y1],fill=255)
        m=m.filter(ImageFilter.GaussianBlur(w/10))
        im=Image.composite(bl,im,m)
    im.save(dst,quality=92)
if __name__=='__main__':
    for name,boxes in json.load(open(sys.argv[1])).items():
        blur('orig/'+name,'blur/'+name,boxes)
