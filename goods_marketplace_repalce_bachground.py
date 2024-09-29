# from PIL import Image
import numpy as np

import cv2
from rembg import remove


def draw_new_back(image_filename, background_color=None, background_img_filename=None, save_img_new=None):
  image = cv2.imread(image_filename)
  image = remove(image)
  image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR) if image.shape[2] == 4 else image

  mask = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
  _, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)

  image_mask = cv2.bitwise_and(np.array(image), np.array(image), mask=mask)
  inverse_mask = cv2.bitwise_not(mask)

  if background_img_filename:
    background_img = cv2.imread(background_img_filename)
    background_img = np.array(background_img)
    backgr = cv2.resize(background_img, 
                        tuple(reversed(np.array(image).shape[:2])))
  elif background_color:
    if isinstance(background_color, str):
      background_color = background_color.lstrip('#')
      background_color = tuple(int(background_color[i:i+2], 16) for i in (0, 2, 4))
    backgr = background_color
  else:
    return image

  new_back = np.full(np.array(image).shape, backgr, dtype=np.uint8)
  
  background = cv2.bitwise_and(new_back, new_back, mask=inverse_mask)

  result = cv2.add(image_mask, background)
  
  pred_img_res = Image.fromarray(result.astype(np.uint8))
  output_filename = f"{input_img.rstrip(input_img.split('/')[-1])}output_{input_img.split('/')[-1].split('.')[0]}.png"
  pred_img_res.save(output_filename, 'PNG')
  print(output_filename)

  

  

if __name__ == "__main__":
  background_color = (210, 180, 170) # персиковый
  background_img = '' # путь до файла с новым фоном
  
  input_img = '/Users/alyonapashnina/computer_vision_case_photo/data/sirius_data/11.jpg'
  
  draw_new_back(input_img, background_color=background_color, background_img_filename=None)
