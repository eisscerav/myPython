import matplotlib.pyplot as plt
import cv2
import pytesseract


def show_img(img):
    plt.imshow(img)
    plt.show()


def demo():
    # refer https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/
    img = cv2.imread(r'data/sample.jpg')
    # show_img(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # show_img(gray)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    im2 = img.copy()
    # file = open("recognized.txt", "w+")
    # file.write("")
    # file.close()

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]

        # Open the file in append mode
        # file = open("recognized.txt", "a")

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)
        print(text)
        # Appending the text into file
        # file.write(text)
        # file.write("\n")

        # Close the file
        # file.close()


def main():
    demo()


if __name__ == '__main__':
    main()
