# imTriangle
This snippet of code attempts to put triangle pixelation effect on images.

## Installation

Run the following to install:

```python
pip install imTriangle
```

## Usage
```python
import cv2
import numpy as np
from imTriangle import triangle

img_fullname = 'assets/lotus.jpg'

img = cv2.imread(img_fullname)
img_out = img.copy()

[h, w, d] = img.shape
for i in range(d):
    img_out[:, :, i] = triangle(img[:, :, i].copy())
    
cv2.imwrite('assets/lotus-triangled.jpg', img_out)
```  
Or  
```console
imTriangle --input 'assets/lotus.jpg' --output 'assets/lotus-triangled.jpg'
```

## Output
This is a sample image:  
![lotus.jpg](https://raw.githubusercontent.com/Mamdasn/imTriangle/main/assets/lotus.jpg "lotus.jpg")  
The sample image after tirangle pixelation effect:  
![lotus-triangled.jpg](https://raw.githubusercontent.com/Mamdasn/imTriangle/main/assets/lotus-triangled.jpg "lotus-triangled.jpg")  
