import numpy as np
from imPixelate import pix
import numba

@numba.njit()
def _crook(image, coef=0.5, RTL=True):
    [h, w] = image.shape
    fixed_image = image.copy()
    hh = h
    ww = int(w+ coef*h - coef)
    crooked_image = np.zeros((hh, ww))
    for i in range(h):
        coefi = int(coef*i)
        if RTL:
            crooked_image[i, 0+coefi:w+coefi] = image[i, :]
        else:
            crooked_image[i, ww-w-coefi:ww-coefi] = image[i, :]
    return crooked_image

@numba.njit()
def _decrook(crooked_image, ww, coef=0.5, RTL=True):                  
    [h, w] = crooked_image.shape
    hh = h
    fixed_image = np.zeros((hh, ww))
    for i in range(h):
        coefi = int(coef*i)
        if RTL:
            fixed_image[i, :] = crooked_image[i, 0+coefi:ww+coefi]
        else:
            fixed_image[i, :] = crooked_image[i, w-ww-coefi:w-coefi]
    return fixed_image

@numba.njit()
def triangle(image, r = 0, coef=0.5):
    h = image.shape[0]
    w = image.shape[1]
    if r==0:
        r = min(h, w)//150
    image_crooked_left = _crook(image, coef=coef, RTL=True)
    image_pix_crooked_left = pix(image_crooked_left, r)
    image_pix_decrooked_left = _decrook(image_pix_crooked_left, w, coef=coef, RTL=True)
    
    image_crooked_right = _crook(image, coef=coef, RTL=False)
    image_pix_crooked_right = pix(image_crooked_right, r)
    image_pix_decrooked_right = _decrook(image_pix_crooked_right, w, coef=coef, RTL=False)
    
    return ((image_pix_decrooked_right+image_pix_decrooked_left)//2).astype(image.dtype)




