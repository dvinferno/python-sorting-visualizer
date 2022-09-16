import math
import pygame
import random

pygame.init()


class drawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    BLUE = 0, 0, 255
    GRAY = 128, 128, 128
    BACKGROUND_COLOR = WHITE

    Shades = [
        GRAY,
        (160, 160, 160),
        (192, 192, 192),
    ]

    FONT = pygame.font.SysFont('arialblack', 20)
    LARGE_FONT = pygame.font.SysFont('arialblack', 30)

    SIDE_PADDING = 100
    TOP_PADDING = 150

    def __init__(self, width, height, list):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Visualizer")
        self.set_list(list)

    def set_list(self, list):
        self.list = list
        self.min_value = min(list)
        self.max_value = max(list)

        self.bar_width = round((self.width - self.SIDE_PADDING) / len(list))
        self.bar_height = math.floor(
            (self.height - self.TOP_PADDING) / (self.max_value - self.min_value))
        self.start_x = self.SIDE_PADDING // 2


def draw(drawInformation, algo_name, Ascending):
    drawInformation.window.fill(drawInformation.BACKGROUND_COLOR)

    title = drawInformation.LARGE_FONT.render(
        f"{algo_name} - {'Ascending' if Ascending else 'Descending'}", 1, drawInformation.GREEN)
    drawInformation.window.blit(
        title, (drawInformation.width/2 - title.get_width()/2, 5))

    controls = drawInformation.FONT.render(
        "R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, drawInformation.BLACK)
    drawInformation.window.blit(
        controls, (drawInformation.width/2 - controls.get_width()/2, 45))

    sorting = drawInformation.FONT.render(
        "I - Insertion Sort | B - Bubble Sort", 1, drawInformation.BLACK)
    drawInformation.window.blit(
        sorting, (drawInformation.width/2 - sorting.get_width()/2, 75))

    draw_list(drawInformation)
    pygame.display.update()


def draw_list(drawInformation, color_positions={}, clear_bg=False):
    list = drawInformation.list

    if clear_bg:
        clear_rect = (drawInformation.SIDE_PADDING // 2, drawInformation.TOP_PADDING, drawInformation.width -
                      drawInformation.SIDE_PADDING, drawInformation.height - drawInformation.TOP_PADDING)
        pygame.draw.rect(drawInformation.window,
                         drawInformation.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(list):
        x = drawInformation.start_x + i * drawInformation.bar_width
        y = drawInformation.height - \
            (val - drawInformation.min_value) * drawInformation.bar_height

        color = drawInformation.Shades[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(drawInformation.window, color, (x, y, drawInformation.bar_width,
                         (drawInformation.height - (val - drawInformation.min_value))))

        if clear_bg:
            pygame.display.update()


def generate_list(n, min_value, max_value):
    list = []

    for _ in range(n):
        val = random.randint(min_value, max_value)
        list.append(val)

    return list


def bubble_sort(drawInformation, Ascending=True):
    list = drawInformation.list

    for i in range(len(list) - 1):
        for j in range(len(list) - 1 - i):
            num1 = list[j]
            num2 = list[j + 1]
            if (num1 > num2 and Ascending) or (num1 < num2 and not Ascending):
                list[j], list[j + 1] = list[j + 1], list[j]
                draw_list(drawInformation, {
                          j: drawInformation.GREEN, j + 1: drawInformation.RED}, True)
                yield True

    return list


def insertion_sort(draw_info, ascending=True):
    list = draw_info.list

    for i in range(1, len(list)):
        current = list[i]

        while True:
            ascending_sort = i > 0 and list[i - 1] > current and ascending
            descending_sort = i > 0 and list[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            list[i] = list[i - 1]
            i = i - 1
            list[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN,
                      i: draw_info.RED}, True)
            yield True

    return list


def main():
    Sorting = False
    Ascending = True
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_value = 0
    max_value = 100

    list = generate_list(n, min_value, max_value)
    draw_info = drawInformation(800, 600, list)

    sorting_algo = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None

    while run:
        clock.tick(124)

        if Sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                Sorting = False
        else:
            draw(draw_info, sorting_algo_name, Ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                list = generate_list(n, min_value, max_value)
                draw_info.set_list(list)
                Sorting = False
            elif event.key == pygame.K_SPACE and Sorting == False:
                Sorting = True
                sorting_algo_generator = sorting_algo(draw_info, Ascending)
            elif event.key == pygame.K_a and not Sorting:
                Ascending = True
            elif event.key == pygame.K_d and not Sorting:
                Ascending = False
            elif event.key == pygame.K_i and not Sorting:
                sorting_algo = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not Sorting:
                sorting_algo = bubble_sort
                sorting_algo_name = "Bubble Sort"

    pygame.quit()


if __name__ == "__main__":
    main()
