import math
from multiprocessing import Process

import circle_fit as cf
import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_point_clicker import clicker

from skimage.morphology import reconstruction
from skimage.segmentation import clear_border
from subpixel_edges import subpixel_edges

class ImageProcessing:
    """
    __init__(self): Sınıfın yapıcı yöntemidir. Herhangi bir parametre almaz ve işlevsizdir.

    clearing_process(self, img, offset_val=10): Verilen bir görüntüyü temizler ve gereksiz parazitleri kaldırır. İlgili görüntüyü (img) ve opsiyonel olarak bir ofset değerini (offset_val) parametre olarak alır. 
    Temizlenmiş görüntüyü döndürür.

    subpixel_method(self, img, threshold_val, iters_val, order_val, show_status=False): Verilen bir görüntü üzerinde alt piksel kenarlarını bulmak için kullanılır. İlgili görüntüyü (img) ve alt piksel kenarlarını 
    bulmak için gereken diğer parametreleri alır: eşik değeri (threshold_val), tekrar sayısı (iters_val), interpolasyon düzeni (order_val) ve durumu gösterme (show_status). Eğer show_status True olarak belirtilirse, 
    alt piksel kenarlarını görselleştirir. Döndürdüğü değerler, bulunan kenarların dış çapı (r), merkez koordinatları (xc, yc) şeklindedir.

    edge_finder(self, img): Verilen bir görüntü üzerinde kenarları bulmak için kullanılır. İlgili görüntüyü (img) parametre olarak alır. Döndürdüğü değerler, dış çap görüntüsü (outer_edges) ve iç çap görüntüsü
    (inner_edges) şeklindedir.

    load_image(self, path): Belirtilen bir dosya yolundan bir görüntü yüklemek için kullanılır. Dosya yolunu (path) parametre olarak alır ve yüklenen görüntüyü döndürür.

    Bu sınıf, görüntü işleme işlemleri için kullanılan bir dizi yöntem içerir. Her bir yöntem, belirli bir işlevi yerine getirir ve belirli girdi parametrelerini alır. Yöntemlerin çıktıları, işlenen görüntüler,
    ölçümler veya diğer ilgili sonuçlar olabilir.
    """
    
    def __init__(self) -> None:
        pass
    
    def clearing_process(self, img, offset_val = 10):
        """
        Args:
            img ([type]): [description]
            offset_val (int, optional): [description]. Defaults to 10.

        Returns:
            [type]: [description]
        """
        # Taking the inverse of image because of Connected Components method wrongly while background is 255. For
        # this reason instensity of background setted as zero (black). cv2.bitwise_not() helps at this point.
        img = 255 - cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img, 4, cv2.CV_32S)
        img_mask = np.array(clear_border(labels)).astype(np.uint8)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img_mask, 4, cv2.CV_32S)

        max_label, _ = max([(i, stats[i, cv2.CC_STAT_AREA]) for i in range(1, num_labels)], key=lambda x: x[1])

        img_mask = np.array(clear_border(labels)).astype(np.uint8)
        img_mask[img_mask!=max_label] = 0
        img_mask = cv2.normalize(img_mask, None, alpha = 0, beta = 1, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F).astype(np.uint8)
        
        cleanedImg = 255-cv2.bitwise_and(img, img, mask=img_mask)
        
        _, th = cv2.threshold(cleanedImg, 254, 255, cv2.THRESH_BINARY_INV)

        (num_labels, labels, stats, _) = cv2.connectedComponentsWithStats(th, 8, cv2.CV_32S)
        x = stats[1, cv2.CC_STAT_LEFT]
        y = stats[1, cv2.CC_STAT_TOP]
        w = stats[1, cv2.CC_STAT_WIDTH]
        h = stats[1, cv2.CC_STAT_HEIGHT]
        
        cleanedImg = cleanedImg[y-offset_val:y+h+offset_val, x-offset_val:x+w+offset_val]
        return cleanedImg
    
    def subpixel_method(self, img, threshold_val, iters_val, order_val, show_status=False):
        img     = img.astype(float)
        edges   = subpixel_edges(img, threshold_val, iters_val, order_val)
        
        if show_status == True:
            plt.imshow(img)
            plt.quiver(edges.x, edges.y, edges.nx, -edges.ny, scale=40)
            plt.show()      
        else:
            pass
        
        coordinates = np.stack((edges.x, edges.y), axis=-1)                                                     # 5.1: Stacking the x and y coordinates.

        xc,yc,r,_ = cf.least_squares_circle((coordinates))                                                      # STEP 6: Finding the outer radius of the object with a
        return r*2, xc, yc

    def edge_finder(self, img):
        """
        Args:
            img ([type]): [description]

        Returns:
            [type]: [description]
        """
        img = cv2.bitwise_not(img)
        seed = np.ones_like(img)*255
        img[ : ,0] = 0
        img[ : ,-1] = 0
        img[ 0 ,:] = 0
        img[ -1 ,:] = 0
        seed[ : ,0] = 0
        seed[ : ,-1] = 0
        seed[ 0 ,:] = 0
        seed[ -1 ,:] = 0

        fill = reconstruction(seed, img, method='erosion')   
        inner_edges = fill-img 
        inner_edges = inner_edges + 255-np.max(inner_edges)   
        return 255-fill, inner_edges              # Outer - Inner Diameter Image

    def load_image(self, path): return cv2.imread(f"{path}")

class Measure:
    def __init__(self, im_path, se_threshold, se_iters, se_orders, cc_threshold, d_s, d_l, d_h, d_w) -> None:
        self.im_path = im_path
        self.se_threshold = se_threshold
        self.se_iters = se_iters
        self.se_orders = se_orders
        self.cc_threshold = cc_threshold
        self.d_s = d_s
        self.d_l = d_l
        self.d_h = d_h
        self.d_w = d_w
        
        # Define measurement methods
        self.SUBPIXEL_EDGES = 0
        self.CONNECTED_COMPONENTS = 1
        self.DEVERNAY = 2

        self.ip = ImageProcessing()

    def measure(self, method):
        self.img = self.ip.load_image(path=self.im_path)
        self.cleared_img = self.ip.clearing_process(img=self.img, offset_val=10)
        self.outer_edges, self.inner_edges = self.ip.edge_finder(img=self.cleared_img)

        if method == 0:                 # if measurement method is subpixel-edges    
            self.d_o, self.xc_o, self.yc_o = self.ip.subpixel_method(
                img=self.outer_edges, threshold_val=self.se_threshold, iters_val=self.se_iters, order_val=self.se_orders, show_status=False)
            self.d_i, self.xc_i, self.yc_i = self.ip.subpixel_method(
                img=self.inner_edges, threshold_val=self.se_threshold, iters_val=self.se_iters, order_val=self.se_orders, show_status=False)
            
            return self.d_o, self.xc_o, self.yc_o, self.d_i, self.xc_i, self.yc_i, self.cleared_img
        
        elif method == 1:               # if measurement method is connected-components == pixel-counting
            _, self.th_outer = cv2.threshold(self.outer_edges, 250, 255, cv2.THRESH_BINARY)
            _, self.th_inner = cv2.threshold(self.inner_edges, 250, 255, cv2.THRESH_BINARY_INV)

            self.area_outer = np.sum(self.th_outer == 0)
            self.area_inner = np.sum(self.th_inner == 0)

            self.d_outer = math.sqrt(4*self.area_outer/math.pi)
            self.d_inner = math.sqrt(4*self.area_inner/math.pi)

            return self.d_outer, self.d_inner, self.cleared_img
        
        elif method == 2:
            # save as pgm
            
            # os.system("devernay ")
            # Devernay method...
            pass

if __name__ == "__main__":
    ip = ImageProcessing()

    img = cv2.imread(r"New folder\30.bmp")
    cleared_img = ip.clearing_process(img=img, offset_val=10)
    outer_edges, inner_edges = ip.edge_finder(img=cleared_img)

    _, th_outer = cv2.threshold(outer_edges, 254, 255, cv2.THRESH_BINARY)
    _, th_inner = cv2.threshold(inner_edges, 254, 255, cv2.THRESH_BINARY_INV)
    plt.imshow(th_outer); plt.show()
    plt.imshow(th_inner); plt.show()
            