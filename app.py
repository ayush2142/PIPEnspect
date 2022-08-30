import streamlit as st
from PIL import Image
import torch
import cv2
import os
from delete_files import delete_image_files, delete_video_files, delete_exp_files
import uuid
import subprocess

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

IMAGES_PATH = os.path.join('dataset', 'dataset/images')

qlabels = ['CORROSION', 'CRACK', 'COATING_DAMAGE', 'GAUGE', 'DENT']

model = torch.hub.load('ultralytics/yolov5', 'custom', path=r"weights/last.pt", force_reload=True)


def main():
    page = st.sidebar.selectbox("Choose your input type", ["image", "video"])
    if page == "image":
        st.title("PIPEnspect")
        st.header("An Automation Tool for Pipeline Inspection using Cloud based AI technologies.")
        st.markdown("Select your input type and upload the file to initiate the analysis, and receive real-time results with high accuracy.")
        st.caption("Developed by Centre for Knowledge, Management, Innovation and Research at McDermott Inc.")
        input_image = st.file_uploader("Upload Image", type=['png', 'jpeg', 'jpg'])
        print(input_image)
        if input_image:
            with st.spinner(text='Resource loading...'):
                st.sidebar.image(input_image)
                picture = Image.open(input_image)
                picture = picture.save(f'temporary_data/images/{input_image.name}')
                img_source = f'temporary_data/images/{input_image.name}'

            results = model(img_source)
            print(results)
            results.save()

            result_file_path = 'runs/detect/exp/{}'.format(input_image.name.split('.')[0] + '.jpg')
            im = cv2.imread(result_file_path)
            output_path = 'image_output/{}'.format(f"final-{str(uuid.uuid4())}.jpg")
            cv2.imwrite(output_path, im)
            delete_image_files()
            with st.spinner(text='Preparing Images'):
                st.header("Analysis")
                st.image(output_path, use_column_width=True)
            

    elif page == "video":

        st.title("PIPEnspect")
        st.header("An Automation Tool for Pipeline Inspection using Cloud based AI technologies.")
        st.markdown("Select your input type and upload the file to initiate the analysis, and receive real-time results with high accuracy.")
        st.caption("Developed by Centre for Knowledge, Management, Innovation and Research at McDermott Inc.")
        input_video = st.file_uploader("Upload Video")

        if input_video:
            with st.spinner(text='Resource loading...'):
                st.sidebar.video(input_video)
                with open(os.path.join("temporary_data", "videos", input_video.name), "wb") as f:
                    f.write(input_video.getbuffer())
                video_source = f'temporary_data/videos/{input_video.name}'

            vidcap = cv2.VideoCapture(video_source)
            success, image = vidcap.read()
            count = 0

            while success:
                cv2.imwrite("temporary_data/frame_split/frame%d.jpg" % count, image)  # save frame as JPEG file
                success, image = vidcap.read()
                # print('Read a new frame: ', success)
                count += 1

            for i in range(count):
                img = "temporary_data/frame_split/frame{}.jpg".format(i)
                results = model(img)
                results.save()
                im = cv2.imread('runs/detect/exp/frame{}.jpg'.format(i))
                cv2.imwrite('temporary_data/video_output_images/frame{}.jpg'.format(i), im)
                delete_exp_files()

            img_array = []

            for i in range(count):
                filename = 'temporary_data/video_output_images/frame{}.jpg'.format(i)
                img = cv2.imread(filename)
                height, width, layers = img.shape
                size = (width, height)
                img_array.append(img)

            temp_file_result = 'temporary_data/videos/project.mp4'
            fourcc_mp4 = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(temp_file_result, fourcc_mp4, 15, size)

            for i in range(len(img_array)):
                out.write(img_array[i])
            out.release()

            converted_video = f"video_output/video-{uuid.uuid4()}.mp4"
            subprocess.call(args=f"ffmpeg -y -i {temp_file_result} -c:v libx264 {converted_video}".split(" "))

            delete_video_files()
            with st.spinner(text='Preparing Images'):
                st.header("Analysis:")
                st.video(converted_video)

           


if __name__ == "__main__":
    main()
