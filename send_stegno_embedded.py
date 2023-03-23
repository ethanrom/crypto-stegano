import numpy as np
import cv2

# Read Cipher_Text File
with open('cipher.txt', 'rb') as fid_2:
    Str = fid_2.read()
Str = Str.decode('utf-8')

# Read Cover Image
filename = input("Enter the file name: ")
IMAge = cv2.imread(filename)
cv2.imshow("Input Cover Image", IMAge)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("original.jpeg", IMAge)

Rows_1, Col_1, Dim = IMAge.shape
if Dim == 3:
    IMAge = cv2.cvtColor(IMAge, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Input Gray Image", IMAge)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

histogram = cv2.calcHist([IMAge], [0], None, [256], [0, 256])
cv2.imshow("Histogram", histogram)
cv2.waitKey(0)
cv2.destroyAllWindows()

ll1, hl1, lh1, hh1 = cv2.dwt2(IMAge, 'haar')
DWT_1 = np.concatenate((np.concatenate((ll1, hl1), axis=1), np.concatenate((lh1, hh1), axis=1)), axis=0)
cv2.imshow("1-level decomposed cover image", DWT_1)
cv2.waitKey(0)
cv2.destroyAllWindows()

ll2, hl2, lh2, hh2 = cv2.dwt2(ll1, 'haar')
b = np.concatenate((np.concatenate((ll2, hl2), axis=1), np.concatenate((lh2, hh2), axis=1)), axis=0)
DWT_2 = np.concatenate((b, hl1), axis=1)
DWT_2 = np.concatenate((DWT_2, np.concatenate((lh1, hh1), axis=1)), axis=0)
cv2.imshow("2-level decomposed cover image", DWT_2)
cv2.waitKey(0)
cv2.destroyAllWindows()

ll3, hl3, lh3, hh3 = cv2.dwt2(ll2, 'haar')
c = np.concatenate((np.concatenate((ll3, hl3), axis=1), np.concatenate((lh3, hh3), axis=1)), axis=0)
cc = np.concatenate((c, hl2), axis=1)
cc = np.concatenate((cc, np.concatenate((lh2, hh2), axis=1)), axis=0)
DWT_3 = np.concatenate((cc, hl1), axis=1)
DWT_3 = np.concatenate((DWT_3, np.concatenate((lh1, hh1), axis=1)), axis=0)
cv2.imshow("3-level decomposed cover image", DWT_3)
cv2.waitKey(0)
cv2.destroyAllWindows()

Rows_2, Col_2 = hh3.shape
hh3_16 = np.zeros((Rows_2, Col_2), dtype=np.uint8)
for i in range(Rows_2):
    for j in range(Col_2):
        if len(Str) > 0:
            hh3_16[i, j] = ord(Str[0])
            Str = Str[1:]
Length_2 = len(hh3_16.ravel())

# Embedding loop
EMBED_16 = np.zeros((Rows_2, Col_2), dtype=np.uint8)
Length_3 = 0
for B in range(Rows_2):
    for C in range(Col_2):
        if Length_3 <= Length_2:
            EMBED_16[B, C] = Str[Length_3]
        else:
            EMBED_16[B, C] = hh3_16[B, C]
        Length_3 += 1

EMBED = EMBED_16

IDWT_1 = pywt.idwt2((ll3, hl3, lh3, EMBED), 'haar')
plt.imshow(IDWT_1, cmap='gray')
plt.title('3-level embedded image')
plt.show()

IDWT_2 = pywt.idwt2((IDWT_1, hl2, lh2, hh2), 'haar')
plt.imshow(IDWT_2, cmap='gray')
plt.title('2-level embedded image')
plt.show()

IDWT_3 = pywt.idwt2((IDWT_2, hl1, lh1, hh1), 'haar')
plt.imshow(IDWT_3, cmap='gray')
plt.title('3-level embedded image')
plt.show()

Embed_IMAge = IDWT_3.astype('uint8')
cv2.imwrite('Embed_IMAge.tiff', Embed_IMAge)
print('Stego-Object created')

# Calculate PSNR, SSIM, MSE, and Correlation between the original and embedded images
PSNR = measure.compare_psnr(IMAge, Embed_IMAge)
SSIM = measure.compare_ssim(IMAge, Embed_IMAge)
mse = np.mean((IMAge - Embed_IMAge) ** 2)
correlation = np.corrcoef(IMAge.flatten(), Embed_IMAge.flatten())[0, 1]

print(f'PSNR = {PSNR:.2f} dB')
print(f'SSIM = {SSIM:.4f}')
print(f'MSE = {mse:.2f}')
print(f'Correlation = {correlation:.4f}')
