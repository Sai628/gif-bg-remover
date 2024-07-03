import os
from PIL import Image, ImageSequence


def process_gif(input_gif_path, temp_path):
    gif = Image.open(input_gif_path)
    frames = ImageSequence.Iterator(gif)

    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    for count, frame in enumerate(frames):
        print(f"process frame {count}")
        frame = frame.convert("RGBA")
        frame_output_path = os.path.join(temp_path, f"frame_{count:03d}.png")
        frame.save(frame_output_path, 'PNG')
        change_bg_to_transparent(frame_output_path, frame_output_path)


def change_bg_to_transparent(input_image_path, output_image_path):
    img = Image.open(input_image_path)
    img = img.convert('RGBA')
    width, height = img.size
    color_0 = img.getpixel((0, 0))
    for h in range(height):
        for w in range(width):
            dot = (w, h)
            color_1 = img.getpixel(dot)
            if color_1 == color_0:
                color_1 = color_1[:-1] + (0,)
                img.putpixel(dot, color_1)
    img.save(output_image_path)


def get_average_gif_frame_duration(gif_path):
    with Image.open(gif_path) as gif:
        durations = [frame.info['duration'] for frame in ImageSequence.Iterator(gif)]
    return sum(durations) // len(durations) if durations else 100


def make_gif_from_folder(input_gif_path, folder_path, output_gif_path):
    images = sorted(
        (os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path) if file_name.lower().endswith('.png')),
        key=lambda x: os.path.getmtime(x)
    )

    frames = [Image.open(image) for image in images]
    average_duration = get_average_gif_frame_duration(input_gif_path)

    frames[0].save(
        output_gif_path,
        format='GIF',
        append_images=frames[1:],
        save_all=True,
        duration=average_duration,
        loop=0,
        disposal=2 
    )
    print(f"gif saved to {output_gif_path}")


def test():
    # change to actual file path
    input_gif_path = r"D:\github\gif-bg-remover\data\loading1.gif"
    output_gif_path = r"D:\github\gif-bg-remover\data\loading1_output.gif"
    temp_path = r'D:\github\gif-bg-remover\temp'

    process_gif(input_gif_path, temp_path)
    make_gif_from_folder(input_gif_path, temp_path, output_gif_path)


if __name__ == '__main__':
    test()
