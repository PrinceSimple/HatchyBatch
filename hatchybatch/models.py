import numpy as np
import lic
import random
from svgpathtools import Path, Line, parse_path, disvg, wsvg
from structure_tensor import eig_special_2d, structure_tensor_2d
from skimage.filters import gaussian
from skimage.util import invert
from skimage.feature import canny
from skimage.io import imread
from skimage.transform import rescale
from skimage.morphology import dilation


class ImageData():
    ''' the image data model'''
    MAX_SIZE = 1024

    def __init__(self):
        self.source = None

    def constant_scale(self, img):
        '''scales the longest side of the image to a fixed value (MAX_SIZE)'''
        scale_factor = self.MAX_SIZE / np.max(img.shape)
        return rescale(img, scale_factor, anti_aliasing=True)

    def load_image(self, filename):
        '''loads, scales and converts an image to grayscale for use as the source for the imageData class'''
        self.source = self.constant_scale(imread(filename, as_gray=True))

    @staticmethod
    def ramp_threshold(img, phi, epsilon):
        return np.tanh(np.multiply(phi, np.subtract(img, epsilon)))

    @staticmethod
    def binarize(ndarr):
        ndarr[ndarr > 0] = 1
        ndarr[ndarr < 0] = 0
        return ndarr

    def generate_DoG(self, sigma_high, sigma_low, threshold):
        '''Difference of Gaussians simple implementation in numpy and scikit-image'''
        outer = gaussian(self.source, sigma=sigma_high)
        inner = gaussian(self.source, sigma=sigma_low)
        diff = np.subtract(inner, outer)
        diff_positive = np.subtract(diff, np.min(diff))
        relative_diff = np.divide(diff_positive, np.max(diff_positive))
        self.dog = self.binarize(np.subtract(relative_diff, threshold))

    def generate_XDoG(self, sigma_high, sigma_low, p, phi, epsilon):
        ''' XDoG - implementation of Winnemöller et al. eXtended Difference of Gaussians'''
        outer = gaussian(self.source, sigma=sigma_high)
        inner = gaussian(self.source, sigma=sigma_low)
        # Equation 2.7.4 in thesis
        scaled_dog = np.subtract(np.multiply(
            p + 1, inner), np.multiply(p, outer))
        unsharp_mask = np.multiply(np.multiply(outer, scaled_dog), 255)
        # Equation 2.7.2 in thesis
        ramp_tresh = np.add(1, self.ramp_threshold(
            img=unsharp_mask, phi=phi, epsilon=epsilon))
        result = np.multiply(ramp_tresh, 255)
        self.xdog = np.round(np.multiply(
            np.divide(result, np.max(result)), 255)).astype('uint8')

    def generate_edge_map(self, sigma, thresh_high, thresh_low):
        ''' simple canny edge detection with the GUI supplied parameters'''
        self.edgemap = canny(self.source, sigma, thresh_high, thresh_low)
        #self.edge_idx = np.transpose(np.nonzero(self.edgemap))

    def generate_flow_field(self, sigma, rho, hatchsigma):
        '''edge tangent flow field derived by the eigenvectors of the structure tensor'''
        S = structure_tensor_2d(self.source, sigma, rho)
        val, vec = eig_special_2d(S)
        hatchfield = gaussian(vec, sigma=hatchsigma)
        self.flowfield_u = vec[0]
        self.flowfield_v = vec[1]
        self.flowfield_hatch_u = hatchfield[0]
        self.flowfield_hatch_v = hatchfield[1]

    def generate_lic(self, stroke_length=20):
        ''' line integral convolution used to visualize the vector field in the GUI'''
        self.lic = lic.lic(
            self.flowfield_u, self.flowfield_v, length=stroke_length)

    def generate_thresholds(self, thresh_min_values, thresh_max_values):
        ''' threshold masks from the image '''
        self.thresh_xdog = self.xdog < 252
        self.thresholds = []
        self.xdog_thresholds = []
        for min, max in zip(thresh_min_values, thresh_max_values):
            thresh_min = self.source > min
            thresh_min = invert(thresh_min)
            thresh_max = self.source > max
            thresh_max = invert(thresh_max)
            thresh = dilation(np.bitwise_xor(thresh_min, thresh_max))
            self.thresholds.append(thresh)
            self.xdog_thresholds.append(
                np.bitwise_and(self.thresholds[-1], self.thresh_xdog))


class Tracer():
    '''model class for the path generation'''

    def __init__(self, imageshape, edgemap, thresholds, u, v, hatch_u, hatch_v):
        self._paths = []
        self.imageshape = imageshape
        self.edgemap = np.transpose(np.nonzero(edgemap > 0))
        self.hatchmaps = thresholds
        self.u = u
        self.v = v
        self.hatch_u = hatch_u
        self.hatch_v = hatch_v
        self.rads = np.arctan2(u, v)
        self.degrees = np.divide(np.multiply(self.rads, 180), np.pi)

    @ staticmethod
    def check_bounce(pentip):
        '''check for inconsistencies in vector field, which causes the pentip to bounce on one axis'''
        return np.round(pentip.dir[0], decimals=1) == np.round(-pentip.pdir[0], decimals=1) or np.round(pentip.dir[1], decimals=1) == np.round(-pentip.pdir[1], decimals=1)

    @ staticmethod
    def check_imagebounds(pentip, shape):
        '''check if the pentip is still in the boundaries of the image'''
        return pentip.pos[0] > 0 and pentip.pos[0] < shape[0] and pentip.pos[1] > 0 and pentip.pos[1] < shape[1]

    @ staticmethod
    def check_edgebounds(pentip, hatchmap):
        '''check if the pentip is inside a "True" area of the hatchmap'''
        pos_x = np.floor(pentip.pos[0]).astype(int)
        pos_y = np.floor(pentip.pos[1]).astype(int)
        return hatchmap[pos_x-1][pos_y-1]

    def get_next_direction(self, pentip):
        '''get the next edge orientation of the pentip in the vector field'''
        pos_x = np.floor(pentip.pos[0]).astype(int)
        pos_y = np.floor(pentip.pos[1]).astype(int)
        return [self.hatch_u[pos_x][pos_y], self.hatch_v[pos_x][pos_y]]

    def generate_seed_points(self, threshmask, distance):
        '''generate starting points for the pentips'''
        seedpoints = np.zeros(self.imageshape, dtype=bool)
        seedpoints[0::distance, 0::distance] = True
        seedpoints = np.bitwise_and(seedpoints, threshmask)
        return np.transpose(np.nonzero(seedpoints > 0))

    def generate_hatchpaths(self, path_lengths, distances, crosshatch):
        ''' the algorithm for hatching paths generation'''
        for idx, hatchmap in enumerate(self.hatchmaps):
            seed_points = self.generate_seed_points(hatchmap, distances[idx])
            for startpoint in seed_points:
                path = Path()
                pentip = Pentip(startpoint[0], startpoint[1])
                for i in range(0, random.randint(path_lengths[idx]-3, path_lengths[idx]+3)):
                    if self.check_imagebounds(pentip, self.imageshape):
                        pentip.dir = self.get_next_direction(pentip)
                        if self.check_bounce(pentip):
                            break
                        pentip.pdir = pentip.dir.copy()
                        pentip.ppos = pentip.pos.copy()
                        pentip.pos = np.add(pentip.pos, pentip.dir)
                        path.append(
                            Line(complex(pentip.ppos[1], pentip.ppos[0]), complex(pentip.pos[1], pentip.pos[0])))
                    if not self.check_edgebounds(pentip, hatchmap):
                        break
                if len(path._segments) > 1:
                    self._paths.append(path)
                    if crosshatch[idx]:
                        self._paths.append(
                            path.rotated(random.randint(70, 110), path.point(random.choice([0.3, 0.4, 0.5, 0.6, 0.7]))))
        # disvg(self._paths)

    def generate_contours(self, path_length, probability):
        ''' the algorithm for the edge paths generation'''
        for idx, pixel in enumerate(self.edgemap):
            if random.random() < probability:
                pt_x = pixel[1]
                pt_y = pixel[0]
                path = parse_path(
                    f'M {pt_x-random.randint(1,path_length)} {pt_y} L {pt_x+random.randint(1,path_length)} {pt_y}')
                path = path.rotated(self.degrees[pt_y][pt_x])
                self._paths.append(path)
        # disvg(self._paths)

    def show_preview(self):
        ''' display the generated SVG in the browser'''
        #self.svg_str = disvg(self._paths, paths2Drawing=True).tostring()
        disvg(self._paths)  # stroke_widths=[1 for paths in self._paths])

    def save_output(self, filename):
        wsvg(self._paths, filename=filename, mindim=1024)


class Pentip():
    '''pentip used to follow the vector field'''

    def __init__(self, x, y):
        self.pos = np.array([x, y], dtype=np.float32)
        self.ppos = self.pos.copy()
        self.dir = np.array([0, 0], dtype=np.float32)
        self.pdir = self.dir.copy()

    def distance(self, other):
        return np.sqrt(np.sum((self.pos - other.pos) ** 2))


class ConfigData():
    def __init__(self):
        pass
