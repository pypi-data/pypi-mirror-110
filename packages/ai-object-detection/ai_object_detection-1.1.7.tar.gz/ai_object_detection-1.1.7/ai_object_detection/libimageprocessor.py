import cv2

import os
import sys
import logging
import colorlog
import re
import base64

from shutil import copyfile
from shutil import move

from PIL import Image

from pdf2image import convert_from_path

class ImageProcessor:
  logger = logging.getLogger('__main__.' + __name__);

  python_dir = os.path.dirname(cv2.__file__)
  face_cascade_xml = os.path.join(python_dir, "data\\haarcascade_frontalface_default.xml")
  eyes_cascade_xml = os.path.join(python_dir, "data\\haarcascade_eye.xml")
  eyes_cascade = cv2.CascadeClassifier(eyes_cascade_xml)
  face_cascade = cv2.CascadeClassifier(face_cascade_xml)
  current_path = os.path.abspath(os.getcwd());

  @classmethod
  def convertRGB(self, src_file, dst_file):
    try:
      if (os.path.exists(src_file)):
        im = Image.open(src_file)
        if im.mode in ("RGBA", "P"):
          im = im.convert("RGB")
        im.save(dst_file)
    except NameError as err:
      self.logger.error("Name Error: {0}".format(err))
      return False
    except OSError as err:
      self.logger.error("OS error: {0}".format(err))
      return False
    except:
      self.logger.error("Unexpected error: %s" % sys.exc_info()[0])
      return False
    return True

  @classmethod
  def convertGray(self, src_file, dst_file):
    try:
      if (os.path.exists(src_file)):
        gray = cv2.imread(src_file, cv2.IMREAD_GRAYSCALE)
        _, thresh = cv2.threshold(gray, 0 , 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        img = cv2.bitwise_not(thresh)
        cv2.imwrite(dst_file, img)
    except NameError as err:
      self.logger.error("Name Error: {0}".format(err))
      return False
    except OSError as err:
      self.logger.error("OS error: {0}".format(err))
      return False
    except:
      self.logger.error("Unexpected error: %s" % sys.exc_info()[0])
      return False
    return True

  @classmethod
  def detectFacesEyes(self, src_file):
    x1=0
    x2=0
    y1=0
    y2=0
    num_face=0
    try:
      image = cv2.imread(src_file)
      height, width, channels = image.shape
      self.logger.debug ("(0,0)(%s,%s) - '%s'" % (width,height,os.path.basename(src_file)))
      grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

      faces = self.face_cascade.detectMultiScale(
          grayImage,
          scaleFactor = 1.1,
          minNeighbors = 4,
      )
      num_face = len(faces)
      self.logger.debug ("Number of faces: %s - '%s'" % (num_face,os.path.basename(src_file)))

      eyes = self.eyes_cascade.detectMultiScale(
          grayImage,
          scaleFactor = 1.1,
          minNeighbors = 4,
      )
      num_eyes = len(eyes)
      self.logger.debug ("Number of eyes: %s - '%s'" % (num_eyes,os.path.basename(src_file)))

      if ((num_face > 0) and (num_eyes > 1)):
        num_face = 0
        w_latest = 0
        h_latest = 0
        for (xf, yf, wf, hf) in faces:
          num_eyes_found = 0
          for (xe, ye, we, he) in eyes:
            if ( xf < xe and xe+we < xf+wf and yf < ye and ye+he < yf+hf):
              num_eyes_found = num_eyes_found + 1
              if num_eyes_found >= 2:
                break
          if num_eyes_found >= 2:
            if (w_latest * h_latest < wf * hf):
              w_latest = wf
              h_latest = hf
              x1 = int(xf - wf * 0.3)
              y1 = int(yf - hf * 0.4)
              x2 = int((xf+wf) + wf * 0.3)
              y2 = int((yf+hf) + hf * 0.5)
              num_face = num_face + 1
      else:
        num_face = 0
    except NameError as e:
      self.logger.error("Unexpected error: %s" % e)
    except AttributeError as e:
      self.logger.error("Unexpected error: %s" % e)
    except:
      self.logger.error("Unexpected error: %s" % sys.exc_info()[0])

    return x1,y1,x2,y2,num_face

  @classmethod
  def cropImage(self, src_file, dst_file, x1,y1,x2,y2):
    try:
      image = cv2.imread(src_file)
      height, width, channels = image.shape
      if (x1 < 0):
        x1 = 0
      if (y1 < 0):
        y1 = 0
      if (x2 > width or x2 == 0):
        x2 = width
      if (y2 > height or y2 == 0):
        y2 = height
      self.logger.warning ("Crop: (0,0)(%s,%s) => (%s,%s)(%s,%s) - '%s'" % (width,height,x1, y1, x2,y2,os.path.basename(dst_file)))
      crop_img_mt = image[y1:y2, x1:x2]
      cv2.imwrite(dst_file, crop_img_mt)
    except OSError as err:
      self.logger.error("OS error: {0}".format(err))
    except:
      self.logger.error("Unexpected error: %s" % sys.exc_info()[0])
    return dst_file

  @classmethod
  def rotateImage(self, src_file, dst_file, degrees_to_rotate):
    try:
      self.logger.warning("Rotate '%s' => '%s'" % (os.path.basename(src_file),os.path.basename(dst_file)))
      image_obj = Image.open(src_file)
      rotated_image = image_obj.rotate(degrees_to_rotate, expand=True)
      rotated_image.save(dst_file)
    except TypeError as err:
      self.logger.error("Type Error: {0}".format(err))
      return False
    except OSError as err:
      self.logger.error("OS Error: {0}".format(err))
      return False
    except:
      self.logger.error("Unexpected error: %s" % sys.exc_info()[0])
      return False
    return True

  @classmethod
  def saveImage(filename, image_data):
    try:
      image_data = re.split(',',image_data)[1]
      imgdata = base64.b64decode(image_data)
      with open(filename, 'wb') as f:
        f.write(imgdata)
    except OSError:
      return False
    return True

  @classmethod
  def moveImage(self, src_file, dst_file):
    try:
      if (os.path.exists(src_file)):
        move(src_file, dst_file)
    except OSError as err:
      self.logger.error("Unexpected error: %s" % err)
      return False
    except:
      self.logger.error("Unexpected error: %s" % sys.exc_info()[0])
      return False
    return True

  @classmethod
  def copyImage(self, src_file, dst_file):
    try:
      if 'JPEG' in src_file:
        im = Image.open(src_file)
        if im.mode in ("RGBA", "P"):
          rgb_im = im.convert("RGB")
          rgb_im.save(dst_file)
        else:
          copyfile(src_file, dst_file)
      else:
        copyfile(src_file, dst_file)
    except OSError as err:
      self.logger.error("OS error: {0}".format(err))
      return False
    except:
      self.logger.error("Unexpected error: %s" % sys.exc_info()[0])
      return False
    return True

  @classmethod
  def updatePortrait(self, src_file, dst_file):
    try:
      self.logger.debug ("updatePortrait: '%s' to'%s'" % (src_file, dst_file))
      rotate_image_tmp=dst_file.replace('CD','CDRC')
      self.convertRGB(src_file, rotate_image_tmp)
      for i in range(0, 3):
        x1,y1,x2,y2,num_face = self.detectFacesEyes(rotate_image_tmp)
        self.logger.info ("[%i]CD: '%s' num_face: '%s'" % (i,os.path.basename(rotate_image_tmp), num_face))
        if (num_face == 0):
          self.logger.warning ("Rotate '%s'" % (os.path.basename(rotate_image_tmp)))
          if not self.rotateImage(src_file,rotate_image_tmp,(i*2+1)*90):
            break
        else:
          self.cropImage(rotate_image_tmp, dst_file, x1,y1,x2,y2)
          break
      os.remove(rotate_image_tmp)
    except NameError as err:
      self.logger.error("Name Error: {0}".format(err))
      return False
    except TypeError as err:
      self.logger.error("Type Error: {0}".format(err))
      return False
    except OSError as err:
      self.logger.error("OS Error: {0}".format(err))
      return False
    except:
      self.logger.error("Unexpected error: %s" % sys.exc_info()[0])
      return False
    return True

  @classmethod
  def copyImageFiles(self, src_dir, dst_dir, dst_archive_dir):
    if not os.path.isdir(src_dir):
      self.logger.error("Folder '%s' does not exist" % (src_dir))
      sys.exit(1)
    if not os.path.isdir(dst_dir):
      self.logger.error("Folder '%s' does not exist" % (dst_dir))
      sys.exit(1)
    if not os.path.isdir(dst_archive_dir):
      self.logger.error("Folder '%s' does not exist" % (dst_archive_dir))
      sys.exit(1)
    try:
      list_of_files = os.listdir(src_dir)
      for filename in list_of_files:
        if filename.endswith(".pdf"):
          self.logger.info("Convert %s to %s and %" % (filename,filename.replace('.pdf','MT.jpg'), filename.replace('.pdf','MS.jpg')))
          src_file = os.path.join(src_dir, filename)
          dst_file = os.path.join(dst_archive_dir, filename)
          poppler_path = os.path.join(self.current_path, 'poppler\\bin')
          pages = convert_from_path(src_file, 500, poppler_path=poppler_path)
          if len(pages) == 2:
            pages[0].save(src_file.replace('.pdf','MT.jpg'), 'JPEG')
            pages[1].save(src_file.replace('.pdf','MS.jpg'), 'JPEG')
            self.moveImage(src_file, dst_file)

      list_of_files = os.listdir(src_dir)
      for filename in list_of_files:
        filename_upper = filename.upper()
        if 'MT' in filename_upper:
          filename_out = filename_upper.replace(' ','')
          filename_out = filename_out.replace('PNG','jpg')
          filename_out = filename_out.replace('JPG','jpg')
          filename_out = filename_out.replace('JPEG','jpg')

          self.logger.info("Copy MT '%s' -> 'ANH_DA_SUA\%s'" % (filename, filename_out))
          src_file_MT = os.path.join(src_dir, filename)
          dst_file_MT = os.path.join(dst_dir, filename_out)
          dst_file_ar_MT = os.path.join(dst_archive_dir, filename)
          if not self.convertRGB(src_file_MT, dst_file_MT):
            break

          filename_MS = re.sub(re.escape('MT'), 'MS', filename, flags=re.IGNORECASE)
          filename_out_MS = filename_out.replace('MT','MS')
          self.logger.info("Copy MS '%s' -> 'ANH_DA_SUA\%s'" % (filename_MS, filename_out_MS))
          src_file_MS = os.path.join(src_dir, filename_MS)
          dst_file_MS = os.path.join(dst_dir, filename_out_MS)
          dst_file_ar_MS = os.path.join(dst_archive_dir, filename_MS)
          if not self.convertRGB(src_file_MS, dst_file_MS):
            break

          filename_CD = re.sub(re.escape('MT'), 'CD', filename, flags=re.IGNORECASE)
          filename_out_CD = filename_out.replace('MT','CD')
          self.logger.info("Copy CD '%s' -> 'ANH_DA_SUA\%s'" % (filename_CD, filename_out_CD))
          src_file_CD = os.path.join(src_dir, filename_CD)
          dst_file_CD = os.path.join(dst_dir, filename_out_CD)
          dst_file_ar_CD = os.path.join(dst_archive_dir, filename_CD)
          if (not os.path.exists(src_file_CD)):
            src_file_CD = src_file_MT
            filename_CD = filename
          if not self.convertRGB(src_file_CD, dst_file_CD):
            break

          self.logger.info("Update CD '%s' -> 'ANH_DA_SUA\%s'" % (filename_CD, filename_out_CD))
          if not self.updatePortrait(src_file_CD, dst_file_CD):
            break

          self.logger.info("Move MT,MS,CD to 'ANH_LUU_TRU'")
          self.moveImage(src_file_MT, dst_file_ar_MT)
          self.moveImage(src_file_MS, dst_file_ar_MS)
          self.moveImage(src_file_CD, dst_file_ar_CD)

    except UnboundLocalError as err:
      self.logger.error("Unbound Local Error: {0}".format(err))
      return False
    except NameError as err:
      self.logger.error("Name Error: {0}".format(err))
      return False
    except TypeError as err:
      self.logger.error("Type Error: {0}".format(err))
      return False
    except OSError as err:
      self.logger.error("OS Error: {0}".format(err))
      return False
    except KeyboardInterrupt as err:
      self.logger.error("KeyboardInterrupt: {0}".format(err))
      sys.exit(1)
    except:
      self.logger.error("Unexpected error: %s" % sys.exc_info()[0])
      return False
    return True