from PIL import Image
import imageio
import scipy.cluster
import scipy.misc
import scipy
import numpy as np
import struct
import binascii


def rgb_to_hex(rgb_code):
    hex = ''
    for i in rgb_code:
        hex += '%02x' % i
    return hex


def get_border_color(filename):
    I = np.asarray(Image.open(filename).resize((100, 100)))
    if(I.shape[2]==4):
        # removing an extra A element from RGBA
        I = I[:, :, 0:3]
    topborder = I[0:1, :].reshape((1, 100, 3))
    rightborder = I[:, -1].reshape((1, 100, 3))
    bottomborder = I[-1, :].reshape((1, 100, 3))
    leftborder = I[:, 0:1].reshape((1, 100, 3))

    final_arr = np.squeeze(np.concatenate(
        (topborder, leftborder, rightborder, bottomborder), axis=1))

    color = []
    for col in final_arr.T:
        ele, counts = np.unique(col, return_counts=True)
        color.append(ele[np.argmax(counts)])

    return rgb_to_hex(color)


def get_dominant_color(filename):
    NUM_CLUSTERS = 5

    im = Image.open(filename)
    im = im.resize((150, 150))      # optional, to reduce time
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)

    # print('finding clusters')
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    # print('cluster centres:\n', codes)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = np.histogram(vecs, len(codes))    # count occurrences

    index_max = np.argmax(counts)                    # find most frequent
    peak = codes[index_max]
    colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    print('most frequent is %s (#%s)' % (peak, colour[:6]))
    return colour[:6]


# get_dominant_color('image.png')
# c = ar.copy()
# for i, code in enumerate(codes):
#     c[scipy.r_[np.where(vecs == i)], :] = code
# imageio.imwrite('clusters.png', c.reshape(*shape).astype(np.uint8))
# print('saved clustered image')
