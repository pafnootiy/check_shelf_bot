from check_shelf import CheckShelf


def main():
    shelf_image_path = "images/part2.jpg"
    template_path = "templates/sample.jpg"
    bot = CheckShelf(shelf_image_path, template_path)
    result = bot.load_and_compare_images()
    print(result)


if __name__ == '__main__':
    main()
