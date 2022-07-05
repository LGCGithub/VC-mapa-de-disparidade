import win32gui
import win32ui
import win32con
import numpy as np

# find windows names

def FindWindows():
    def winEnumHandler( hwnd, ctx ):
        if win32gui.IsWindowVisible( hwnd ):
            print (hex(hwnd), win32gui.GetWindowText( hwnd ))
    win32gui.EnumWindows( winEnumHandler, None )

class Window:
    name = ''
    width = 0
    height = 0
    left = 0
    top = 0

    hwnd = None
    wDC = None
    dcObj = None

    def __init__(self, window_name, width, height):
        try:
            self.name = window_name
        
            self.hwnd = win32gui.FindWindowEx(0, 0, None, window_name)
            self.wDC = win32gui.GetWindowDC(self.hwnd)
            self.dcObj = win32ui.CreateDCFromHandle(self.wDC)

            left, top, right, bot = win32gui.GetWindowRect(self.hwnd)

            self.width = right - left
            self.height = bot - top
            self.left = left
            self.top = top

            # Remove bordas, title
            self.width = self.width - 16
            self.height = self.height - 38

        except:
            raise Exception('Erro na seleção da janela, nome da janela inválido?') from None

    def __del__(self):
        self.dcObj.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.wDC) 

    def screenshot(self):
        cDC = self.dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(self.dcObj, self.width, self.height)

        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.width, self.height), self.dcObj, (8, 30), win32con.SRCCOPY)
        signedIntArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntArray, dtype='uint8')
        img.shape = (self.height, self.width, 4)

        cDC.DeleteDC()
        win32gui.DeleteObject(dataBitMap.GetHandle())
        return img