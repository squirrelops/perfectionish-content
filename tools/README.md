# perfectionish media tools

- `moody.py SRC DST [strength]`: brand grade for real photos (warm, muted, lifted blacks, soft vignette, film grain). Strength 1.6 for bright daylight, 1.0 to 1.2 for indoor, 0.5 to 0.6 for photos that are already dark or polished. Output JPEG, long side 2048.
- `blur_faces.py boxes.json`: light elliptical blur over children's faces. boxes.json maps `orig/<file>` names to `[[x0,y0,x1,y1], ...]` in original pixels; writes to `blur/`. Always check a before and after crop.
- Video grade (ffmpeg, 9:16): `scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,eq=saturation=0.8:contrast=1.06,colorbalance=rs=.04:gs=.01:bs=-.07:rh=.03:bh=-.05,curves=all='0/0.055 0.5/0.5 1/0.94',vignette=PI/5,noise=alls=5:allf=t,format=yuv420p` with `-c:v libx264 -preset veryfast -crf 28`.

Never commit photos of children here. This repo is public.
