import cv2

class CheckShelf:
    def __init__(self, shelf_image_path, template_path, threshold=0.8):
        self.shelf_image_path = shelf_image_path
        self.template_path = template_path
        self.threshold = threshold

    def load_and_compare_images(self):
        shelf_image = cv2.imread(self.shelf_image_path)
        template_image = cv2.imread(self.template_path)

        if shelf_image is None or template_image is None:
            return "Не удалось загрузить одно или оба изображения."

        gray_shelf = cv2.cvtColor(shelf_image, cv2.COLOR_BGR2GRAY)
        gray_template = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(
            gray_shelf, gray_template, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= self.threshold:
            return "Товар найден на стеллаже."
        else:
            return "Товар не найден на стеллаже."
