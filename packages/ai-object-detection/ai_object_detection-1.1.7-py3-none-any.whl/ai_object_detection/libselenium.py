import os
import sys
import logging
import colorlog
import win32com.client
import platform
import time
import base64
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

class WebBrowser:
  def __init__(self, downloadDir = None, captchaDir = None):
    self.logger = logging.getLogger('__main__.' + __name__);
    self.current_path = os.path.abspath(os.getcwd());

    # Create Download directory
    self.downloadDir = downloadDir
    if downloadDir == None:
      self.downloadDir = os.path.join(current_path, 'ToKkai')
    if not os.path.exists(self.downloadDir):
      os.makedirs(self.downloadDir, exist_ok = True)
      self.logger.info("Directory '%s' created" % self.downloadDir)

    self.captchaDir = captchaDir
    if self.captchaDir != None:
      if not os.path.exists(self.captchaDir):
        os.makedirs(self.captchaDir, exist_ok = True)
        self.logger.info("Directory '%s' created" % self.captchaDir)

    # File Chrome
    if (os.path.exists('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe')):
      self.chrome_exe = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
    elif (os.path.exists('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')):
      self.chrome_exe = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    else:
      self.logger.error("Error: không tìm thấy file <folder>\\Google\\Chrome\\Application\\chrome.exe")
      os._exit(1)

    # File chromedriver
    self.chrome_version = self.getChromeVersion(self.chrome_exe)
    self.os_platform = platform.architecture()

    self.chromedriver_exe = os.path.join(self.current_path, 'chromedriver.exe')
    self.chromedriver_exe_version = os.path.join(self.current_path, 'chromedriver' + self.chrome_version[:2] + '.exe')
    if (os.path.exists(self.chromedriver_exe_version)):
      self.chromedriver_exe = self.chromedriver_exe_version

    self.chrome_options = webdriver.ChromeOptions()
    self.chrome_options.binary_location = self.chrome_exe
    self.chrome_options.add_argument('--incognito')
    self.chrome_options.add_argument('--disable-gpu')
    self.chrome_options.add_argument('--log-level=3')
    self.chrome_options.add_argument('--use-gl=desktop')
    self.preferences = {
                    "profile.default_content_settings.popups": 0,
                    "download.default_directory": self.downloadDir,
                    "directory_upgrade": True
                }
    self.chrome_options.add_experimental_option('prefs', self.preferences)

  def saveImage(self, filename, image_data):
    try:
      image_data = re.split(',',image_data)[1]
      imgdata = base64.b64decode(image_data)
      with open(filename, 'wb') as f:
        f.write(imgdata)
    except OSError:
      return False
    return True

  def getConfig(self):
    self.logger.info("Current Path: %s" % self.current_path)
    self.logger.info("OS Platform: %s, %s" % (self.os_platform[0],self.os_platform[1]))

    self.logger.info("Google Chrome: %s" % self.chrome_exe)
    self.logger.info("Google Chrome Version: %s" % self.chrome_version)
    self.logger.info("Chrome Driver: %s" % self.chromedriver_exe)

  def getChromeVersion(self,filename):
    parser = win32com.client.Dispatch("Scripting.FileSystemObject")
    try:
      version = parser.GetFileVersion(filename)
    except:
      version = "90.0"
      self.logger.error("Unexpected error: %s" % sys.exc_info()[0])
    return version

  def startDriver(self):
    self.driver = webdriver.Chrome(self.chromedriver_exe, options=self.chrome_options)
    self.driver.implicitly_wait(20)
    self.driver.maximize_window()

  def waitFor(self,condition_function):
    start_time = time.time()
    while time.time() < start_time + 15:
      if condition_function():
        return True
      else:
        time.sleep(0.5)
    """
    raise Exception(
      'Timeout waiting for {}'.format(condition_function.__name__)
    )"""
  def waitForPageLoaded(self):
    time.sleep(1)
    def page_has_loaded():
      self.logger.info("Đang chờ tải trang web...")
      page_state = self.driver.execute_script('return document.readyState;')
      return page_state == 'complete'
    self.waitFor(page_has_loaded)

  def waitForGhiNhan(self):
    def page_has_loaded():
      status = 'loading'
      search = self.searchElement("Captcha empty", 'XPATH', '//input[@formcontrolname="textCaptcha"]', 1, 0, 1)
      if search:
        search_value = search.get_attribute('value')
        if not search_value or len(search_value) == 0:
          status = 'complete'
      return status == 'complete'
    self.waitFor(page_has_loaded)

  def launchUrl(self, url = 'https://dichvucong.baohiemxahoi.gov.vn/#/dang-ky?loaidoituong=0'):
    self.driver.get(url);
    time.sleep(0.5)
    self.driver.refresh()
    self.waitForPageLoaded()

  def quitDriver(self):
    self.driver.quit()

  def moveToElement(self, element_name, bytype, str_find, timeout, delay, interval):
    try:
      search = self.searchElement(element_name, bytype, str_find, timeout, delay, interval)
      if search:
        action = ActionChains(self.driver)
        action.move_to_element(search).click().perform()
        time.sleep(delay)
    except:
      self.logger.warning("Hay quay lai website")

  def waitElementOut(self, action_name, bytype, str_find, timeout, delay, interval):
    self.driver.implicitly_wait(interval)
    result = None
    times  = int(timeout / interval)
    not_found_times = 0
    for index in range(0, times):
      try:
        self.logger.debug("[%i] Cho (out) %s" %(index,action_name))
        time.sleep(interval)
        if bytype == "XPATH":
          result = WebDriverWait(self.driver, interval).until(EC.visibility_of_element_located((By.XPATH,str_find)))
        elif bytype == "CLASS_NAME":
          result = WebDriverWait(self.driver, interval).until(EC.visibility_of_element_located((By.CLASS_NAME,str_find)))
        elif bytype == "ID":
          result = WebDriverWait(self.driver, interval).until(EC.visibility_of_element_located((By.ID,str_find)))
        elif bytype == "CSS":
          result = WebDriverWait(self.driver, interval).until(EC.visibility_of_element_located((By.CSS,str_find)))
        else:
          result = None
      except:
        result = None
        break
    self.driver.implicitly_wait(20)
    return result

  def searchElement(self, element_name, bytype, str_find, timeout, delay, interval):
    self.driver.implicitly_wait(interval)
    result = None
    times  = int(timeout / interval)
    for index in range(0, times):
      try:
        self.logger.info("[%i] Tìm '%s'" %(index,element_name))
        if bytype == "XPATH":
          result = WebDriverWait(self.driver, interval).until(EC.visibility_of_element_located((By.XPATH,str_find)))
        elif bytype == "CLASS_NAME":
          result = WebDriverWait(self.driver, interval).until(EC.visibility_of_element_located((By.CLASS_NAME,str_find)))
        elif bytype == "ID":
          result = self.driver.find_element_by_id(str_find)
          if result:
            break
        elif bytype == "CSS":
          result = WebDriverWait(self.driver, interval).until(EC.visibility_of_element_located((By.CSS,str_find)))

        if result and result.is_displayed() and result.is_enabled():
          break
        else:
          time.sleep(interval)
      except:
        result = None
        time.sleep(interval)
    self.driver.implicitly_wait(20)
    return result

  def searchSendkeys(self, element_name, bytype, str_find, enter_keys, timeout, delay, interval):
    for x in range(3):
      search = self.searchElement(element_name, bytype, str_find, timeout, delay, interval)
      if search:
        if (not search.get_attribute('value')):
          search.send_keys(enter_keys)
          if delay > 0:
            time.sleep(delay)
        else:
          break

  def searchClick(self,element_name, bytype, str_find, timeout, delay, interval):
    try:
      search = self.searchElement(element_name, bytype, str_find, timeout, delay, interval)
      if search:
        search.click()
        if delay > 0:
          time.sleep(delay)
    except:
      search = None
    return search

  def waitElementIn(self, action_name, bytype, str_find, timeout, delay, interval):
    self.driver.implicitly_wait(interval)
    result = None
    times  = int(timeout / interval)
    for index in range(0, times):
      try:
        self.logger.info("[%i] Wait '%s'" %(index,action_name))
        if bytype == "XPATH":
          result = WebDriverWait(self.driver, interval).until(EC.presence_of_element_located((By.XPATH,str_find)))
        elif bytype == "CLASS_NAME":
          result = WebDriverWait(self.driver, interval).until(EC.presence_of_element_located((By.CLASS_NAME,str_find)))
        elif bytype == "ID":
          result = self.driver.find_element_by_id(str_find)
        elif bytype == "CSS":
          result = WebDriverWait(self.driver, interval).until(EC.presence_of_element_located((By.CSS,str_find)))
        else:
          result = None
        if result and result.is_displayed() and result.is_enabled():
          break
      except:
        result = None
        time.sleep(interval)
    self.driver.implicitly_wait(20)
    return result

  def fillForm(self, file_cd, file_mt, file_ms, ho_ten, ma_so_str, cmnd_str, tinh_tp_str, huyen_str, xa_str, dia_chi, so_dt_str, chon_bhxh_hm=True):
    #Ho Ten
    if ho_ten:
      self.searchSendkeys('Ho Ten', 'CLASS_NAME', 'mat-input-element', ho_ten, 20, 0, 2)

    #click Ma so
    if ma_so_str:
      self.searchSendkeys('Ma so', 'XPATH', '//input[@formcontrolname="MaSoBhxh"]', ma_so_str, 10, 0, 2)

    #fileAnhCaNhan
    if file_cd:
      if os.path.exists(file_cd):
        search = self.searchElement("fileAnhCaNhan", 'ID', 'fileAnhCaNhan', 10, 0,2)
        search.send_keys(file_cd)
        search = self.searchClick('fileAnhCaNhan', 'XPATH', '//*[@id="body-dialog"]/mat-toolbar/section/div/button[6]', 20,0,2)
        search = self.searchClick('fileAnhCaNhan', 'XPATH', '//*[@id="body-dialog"]/mat-toolbar/section/div/button[6]', 4,0,2)
        search = self.waitElementOut('fileAnhCaNhan','XPATH', '//*[@id="footer-dialog"]/button/span', 30,0, 1)
        if search:
          self.searchClick('fileAnhCaNhan', 'XPATH', '//*[@id="footer-dialog"]/button/span', 4,0,2)
      else:
        file_cd = os.path.join(self.current_path, "fileAnhCaNhan.jpg")
        search = self.searchElement("fileAnhCaNhan", 'ID', 'fileAnhCaNhan', 10, 0,2)
        search.send_keys(file_cd)
        self.searchClick('fileAnhCaNhan', 'XPATH', '//*[@id="body-dialog"]/mat-toolbar/section/div/button[6]', 10,0,2)
        self.searchClick('fileAnhCaNhan','XPATH', '//*[@id="footer-dialog"]/button/span', 10,0, 2)

    if cmnd_str == None or len(cmnd_str) != 13:
      #cmnd mat truoc
      if file_mt:
        if os.path.exists(file_mt):
          search = self.searchElement("fileAnhCmndMatTruoc", 'ID', 'fileAnhCmndMatTruoc', 10, 0,2)
          search.send_keys(file_mt)
          search = self.waitElementOut('fileAnhCmndMatTruoc', 'XPATH', '//*[@id="footer-dialog"]/button/span', 60,0, 1)
          if search:
            self.searchClick('fileAnhCmndMatTruoc', 'XPATH', '//*[@id="footer-dialog"]/button/span', 4,0,2)
        else:
          file_mt = os.path.join(self.current_path, "fileAnhCmndMatTruoc.PNG")
          if os.path.exists(file_mt):
            search = self.searchElement("fileAnhCmndMatTruoc", 'ID', 'fileAnhCmndMatTruoc', 10, 0,2)
            search.send_keys(file_mt)
            self.searchClick('fileAnhCmndMatTruoc', 'XPATH', '//*[@id="body-dialog"]/mat-toolbar/section/div/button[6]', 10,0,2)
            self.searchClick('fileAnhCmndMatTruoc','XPATH', '//*[@id="footer-dialog"]/button/span', 10,0, 2)

      #cmnd mat sau
      if file_ms:
        if os.path.exists(file_ms):
          search = self.searchElement("fileAnhCmndMatSau", 'ID', 'fileAnhCmndMatSau', 10, 0,2)
          search.send_keys(file_ms)
          search = self.waitElementOut('fileAnhCmndMatSau','XPATH', '//*[@id="footer-dialog"]/button/span', 60,0, 1)
          if search:
            self.searchClick('fileAnhCmndMatSau', 'XPATH', '//*[@id="footer-dialog"]/button/span', 4,0,2)
        else:
          file_ms = os.path.join(self.current_path, "fileAnhCmndMatSau.PNG")
          if os.path.exists(file_ms):
            search = self.searchElement("fileAnhCmndMatSau", 'ID', 'fileAnhCmndMatSau', 10, 0,2)
            search.send_keys(file_ms)
            self.searchClick('fileAnhCmndMatSau', 'XPATH', '//*[@id="body-dialog"]/mat-toolbar/section/div/button[6]', 10,0,2)
            self.searchClick('fileAnhCmndMatSau','XPATH', '//*[@id="footer-dialog"]/button/span', 10,0, 2)

    #cmnd_str
    if cmnd_str:
      self.searchSendkeys('So CMND', 'XPATH', '//input[@formcontrolname="Cmnd"]', cmnd_str, 10, 0, 2)

    #Tinh
    if tinh_tp_str:
      self.searchSendkeys('Tinh', 'XPATH', '//*[@id="mat-input-8"]', tinh_tp_str, 10, 3,2)
    #huyen_str
    if huyen_str:
      self.searchSendkeys('Huyen', 'XPATH', '//*[@id="mat-input-9"]', huyen_str, 10, 3,2)
    #xa_str
    if xa_str:
      self.searchSendkeys('Xa', 'XPATH', '//*[@id="mat-input-10"]', xa_str, 10, 2,2)
    #so nha
    if dia_chi:
      self.searchSendkeys('So Nha', 'XPATH', '//*[@id="mat-input-11"]', dia_chi, 10, 0,2)
    #Email
    #if so_dt_str:
    #  self.searchSendkeys('So Di Dong', 'XPATH', '//input[@formcontrolname="Email"]', "%s@gmail.com" % (so_dt_str), 10, 0,2)
    #So di dong
    if so_dt_str:
      self.searchSendkeys('So Di Dong', 'XPATH', '//*[@id="mat-input-3"]', so_dt_str, 10, 0,2)
    #Click Chon
    if chon_bhxh_hm:
      self.searchClick('Cick Chon', 'XPATH', '//*[@id="form-cnt"]/div[9]/div/div/button/span', 30,2,1)
      #Chon 079
      self.searchClick('Chon 079', 'XPATH', '//*[@id="body-dialog"]/tree-root/tree-viewport/div/div/tree-node-collection/div/tree-node[50]/div/tree-node-wrapper/div/div/tree-node-content/span', 30,2,1)
      #Chon 07921
      self.searchClick('Chon 07921', 'XPATH', '//*[@id="body-dialog"]/tree-root/tree-viewport/div/div/tree-node-collection/div/tree-node[50]/div/tree-node-children/div/tree-node-collection/div/tree-node[19]/div/tree-node-wrapper/div/div/tree-node-content/span', 30,2,1)
      #Click Chon
      self.searchClick('Click Chon', 'XPATH', '//*[@id="footer-dialog"]/button[1]', 30,1,1)

    # Go to Captcha
    self.logger.info("Nhap Captcha")
    self.moveToElement("Captcha Textbox", 'XPATH', '//input[@formcontrolname="textCaptcha"]', 10, 2,2)

  def waitCaptcha(self, file_cd, file_mt, file_ms, ho_ten, ma_so_str, cmnd_str, tinh_tp_str, huyen_str, xa_str, dia_chi, so_dt_str, chon_bhxh_hm=False):
    status = ""
    msg = ""
    is_top = True
    ghi_nhan = False
    last_Captcha = "new"
    search_value = "new"
    for i in range(60):
      search = self.searchElement("[%i] Nhap Captcha" % (i), 'XPATH', '//input[@formcontrolname="textCaptcha"]', 4, 0, 2)
      if search:
        search_value = search.get_attribute('value')
        search_value = search_value.upper()

      # Cho nhap
      if len(search_value) == 0 and not ghi_nhan:
        time.sleep(3)
        continue

      if is_top:
        is_top = False

      # Da nhap
      if not '@' in search_value and len(search_value) == 4:
        if last_Captcha != search_value:
          search = self.searchElement("[%i] Cap nhat Captcha" % (i), 'XPATH', '//input[@formcontrolname="textCaptcha"]', 2, 0, 2)
          if search:
            search_value = search.get_attribute('value')
            for c in search_value:
              if c.islower():
                search_value = search_value.upper()
                search.clear()
                time.sleep(0.5)
                search.send_keys(search_value)
                time.sleep(1)
                break
          if self.captchaDir != None:
            search = self.searchElement("[%i] Captcha image" % (i), 'XPATH', '//img[@alt="captcha"]', 2, 0, 2)
            if search:
              self.logger.info("Save Captcha\%s.png" % (search_value))
              captchaFilepath = os.path.join(self.captchaDir, "%s.png" % (search_value))
              self.saveImage(captchaFilepath,search.get_attribute('src'))
          # Click 'Ghi Nhan'
          self.searchClick('Ghi Nhan', 'XPATH', '//*[@id="cdk-step-content-0-1"]/app-dang-ky-ca-nhan/form/div/div/div/div[3]/div/button/span', 10, 1, 2)
          last_Captcha = search_value
          ghi_nhan = True
          self.searchClick("[%i] Reset Captcha" % (i), 'XPATH', '//button[@aria-label="refresh captcha"]', 2, 0, 2)
          self.waitForGhiNhan()

        # Kiểm tra 'Thông Báo lỗi'
        error_msg = ""
        search = self.searchElement('Thong Bao', 'XPATH', '//*[@id="toast-container"]/div/div[1]', 2,0,1)
        if search:
          error_msg = search.text

        if error_msg:
          msg = error_msg
          ghi_nhan = False
          self.logger.error("Thong bao loi: %s" % (error_msg).encode('cp1250','replace'))
          print("Thong bao loi: %s" % error_msg)
          #Mã số XXXXX đã đăng ký giao dịch điện tử với cơ quan BHXH, số điện thoại đăng ký XXXX. Liên hệ 1900.9068 để được hỗ trợ.
          if 'đã đăng ký' in error_msg:
            self.logger.info("Da hoan thanh")
            status = "xong"
            break
          #Số điện thoại XXXXX đã được kê khai giao dịch điện tử với mã số XXXX.
          elif 'đã được kê khai' in error_msg:
            self.logger.error("Da co loi")
            status = "error"
            break
          #Thông tin của bạn chưa có trong CSDL QG về DC, yêu cầu bổ sung ảnh CCCD
          elif 'chưa có trong CSDL QG' in error_msg:
            self.logger.error("Da co loi")
            status = "error"
            break
          #Vui lòng cung cấp ảnh CCCD để hoàn tất việc đăng ký GDĐT với cơ quan BHXH Việt Nam
          elif 'Vui lòng cung cấp ảnh CCCD' in error_msg:
            if os.path.exists(file_mt) and os.path.exists(file_ms):
              self.fillForm(None, file_mt, file_ms, None, None, None, None, None, None, None, None, False)
            else:
              self.logger.error("Da co loi. Khong tim thay file hinh")
              status = "error"
              break
          #Vui lòng điền đầy đủ thông tin
          elif 'Vui lòng điền đầy đủ' in error_msg:
            self.logger.error("Da co loi")
            status = "error"
            # xóa Captcha đã nhập
            search = self.searchElement('Captcha box-xoa', 'XPATH', '//input[@formcontrolname="textCaptcha"]', 4, 0, 2)
            search.clear()
            # làm mới Captcha
            #self.searchClick('Lam moi Captcha', 'XPATH', '//*[@id="form-cnt"]/div[11]/div[3]/div/div/div/div[2]/a/img', 4, 0, 2)
          #Có lỗi xảy ra
          else:
            status = "error"
            # xóa Captcha đã nhập
            search = self.searchElement('Captcha box-xoa', 'XPATH', '//input[@formcontrolname="textCaptcha"]', 4, 0, 2)
            search.clear()
            # làm mới Captcha
            # self.searchClick('Lam moi Captcha', 'XPATH', '//*[@id="form-cnt"]/div[11]/div[3]/div/div/div/div[2]/a/img', 4, 0, 2)
      else:
        if '@' in search_value and last_Captcha != search_value:
          ghi_nhan = False
          last_Captcha = search_value
          self.logger.info("Captcha: %s" % search_value.encode('cp1250','replace'))
          if ('XO' in search_value):
            self.logger.warning("Nguoi dung da hoan thanh")
            status = "xong"
            msg = "Nguoi dung da hoan thanh"
            break
          elif ("BO" in search_value):
            self.logger.warning("Bo qua")
            status = "skip"
            msg = "Bo qua"
            break
          elif ("LO" in search_value):
            self.logger.warning("Du lieu bi loi")
            status = "error"
            msg = "Du lieu bi loi"
            break
          elif ("MT" in search_value):
            self.fillForm(None, file_mt, None, None, None, None, None, None, None, None, None, False)
          elif ("MS" in search_value):
            self.fillForm(None, None, file_ms, None, None, None, None, None, None, None, None, False)
          elif ("CD" in search_value):
            self.fillForm(file_cd, None, None, None, None, None, None, None, None, None, None, False)
          elif ("TI" in search_value):
            self.fillForm(None, None, None, None, None, None, tinh_tp_str, huyen_str, xa_str, dia_chi, None, False)
          elif ("HU" in search_value):
            self.fillForm(None, None, None, None, None, None, None, huyen_str, xa_str, dia_chi, None, False)
          elif ("XA" in search_value):
            self.fillForm(None, None, None, None, None, None, None, None, xa_str, dia_chi, None, False)
          elif ("DI" in search_value):
            self.fillForm(None, None, None, None, None, None, None, None, None, dia_chi, None, False)

      if not '@' in search_value and ghi_nhan:
        # Click 'Dong'
        search = self.searchClick('Nut Dong', 'XPATH', '//button[@aria-label="Close dialog"]', 6, 5, 2)
        if search:
          self.logger.info("Da hoan thanh")
          status = "xong"
          msg = "Da hoan thanh"
          break

      time.sleep(3)
    return status,msg,is_top