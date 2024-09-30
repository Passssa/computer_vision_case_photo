# from PIL import Image
# import numpy as np

# import cv2
# from rembg import remove

СOLOR_RGB = {'red': (255, 0, 0),
             'pink': (255, 105, 180),
             'orange': (255, 165, 0),
             'yellow': (255, 255, 0),
             'green': (0, 128, 0),
             'cyan': (0, 255, 255),
             'blue': (0, 0, 255),
             'purple': (128, 0, 128),
             'brown': (165, 42, 42),
             'gray': (128, 128, 128),
             'black': (0, 0, 0),
             'white': (255, 255, 255),
             'tan': (210, 180, 140),
             'beige': (245, 245, 220),
             'ivory': (255, 255, 240),
             'thistle': (216, 191, 222)}



def draw_new_back(image_filename: str, background_color:tuple = None, background_img_filename:str = None):
  """Меняет фон на карточке товара. Новая картинка сохраняется в эту же директорию.

  Args:
    image_filename (str): путь до файла с изначальным изображением.
    background_color (tuple, optional): цвет для нового фона.
    background_img_filename (str): путь до файла с изображением для нового фона.
  """
  image = cv2.imread(image_filename) # считываем файл
  image = remove(image) # удаляем фон
  image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR) if image.shape[2] == 4 else image

  mask = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY) # делаем маску для изображения
  _, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)

  image_mask = cv2.bitwise_and(np.array(image), np.array(image), mask=mask) # применяем маску 
  inverse_mask = cv2.bitwise_not(mask)

  # подготавливаем новый фон (если фона не подали - возвращаем изображение без фона (или с прозрачным фоном))
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
  background = cv2.bitwise_and(new_back, new_back, mask=inverse_mask) # наш фон

  result = cv2.add(image_mask, background)  # скрещиваем фон и изображение
  
   # сохранем новое изображение
  pred_img_res = Image.fromarray(result.astype(np.uint8))
  output_filename = f"{input_img.rstrip(input_img.split('/')[-1])}output_{input_img.split('/')[-1].split('.')[0]}.png"
  pred_img_res.save(output_filename, 'PNG')
  print(output_filename)

  

  

if __name__ == "__main__":
  background_color = input().replace(' ','').replace('(','').replace(')','').split(',')
  background_color = tuple(int(x) for x in background_color)
  background_img = str(input())
  input_img = str(input())

  if len(background_color) == 0 and len(background_img) == 0:
    background_img = 'backgrounds_images/белое_полотно_фотостудии.png' # путь до файла с новым фоном
    background_color = СOLOR_RGB['thistle'] # цвет для фона
  
  input_img = 'data/sirius_data/11.jpg' # путь до файла с входной картинкой

  print(background_color, background_img, input_img)
  
#   draw_new_back(input_img, background_color=background_color, background_img_filename=None)
