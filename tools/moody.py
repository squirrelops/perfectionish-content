"""perfectionish moody grainy grade: warm, muted, lifted blacks, soft vignette, film grain."""
import sys, numpy as np
from PIL import Image, ImageFilter, ImageOps
def grade(src, dst, strength=1.0, max_side=2048, seed=7):
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    if max(im.size) > max_side:
        im.thumbnail((max_side, max_side), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255.0
    lum = (a @ np.array([0.299, 0.587, 0.114], np.float32))[..., None]
    a = lum + (a - lum) * (1 - 0.22 * strength)            # mute colors
    a = a * np.array([1.0 + .05*strength, 1.0 + .01*strength, 1.0 - .09*strength], np.float32)  # warm
    a = np.clip(a, 0, 1)
    a = a - 0.10*strength*(a - a*a)*(2*a - 1)*0             # placeholder keeps curve simple
    a = np.power(np.clip(a,0,1), 1 + 0.10*strength)          # deepen mids
    a = a / (1 + 0.18*strength*a)  * (1 + 0.18*strength)      # roll off highlights
    a = 0.5 + (a - 0.5) * (1 + 0.12*strength)               # filmic contrast
    gdom = np.clip((a[...,1:2] - np.maximum(a[...,0:1], a[...,2:3])) * 6, 0, 1)
    a = a + gdom * np.array([.035, -.01, -.02], np.float32) * strength   # greens toward olive
    a = 0.055*strength + a * (1 - 0.055*strength - 0.05*strength)  # lift blacks, soften whites
    lum = (np.clip(a,0,1) @ np.array([0.299, 0.587, 0.114], np.float32))[..., None]
    sh = np.clip(1 - lum*2, 0, 1); hi = np.clip(lum*2 - 1, 0, 1)
    a = a + sh * np.array([-.01, .012, .0], np.float32)*strength + hi * np.array([.025, .012, -.02], np.float32)*strength
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w/2)/(w/2))**2 + ((yy - h/2)/(h/2))**2) / 1.414
    a = a * (1 - 0.22*strength * np.clip(r - 0.35, 0, 1)**1.5)[..., None]
    rng = np.random.default_rng(seed)
    g = rng.normal(0, 1, (h, w)).astype(np.float32)
    g = np.asarray(Image.fromarray(((g*40)+128).clip(0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32)/40 - 3.2
    amt = 0.030 * strength * (max(h, w)/2048)**0.3
    a = a + (g * amt)[..., None] * (0.6 + 0.4*(1-np.clip(a.mean(axis=2, keepdims=True),0,1)))
    out = Image.fromarray((np.clip(a, 0, 1)*255).astype(np.uint8))
    out.save(dst, quality=92, subsampling=0)
if __name__ == '__main__':
    grade(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 1.0)
