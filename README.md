# Space Data Analysis with Parallel Computing

## Description
This project aims to analyze space data obtained from a space telescope using parallel computing techniques. The program processes sets of images of celestial objects captured by the telescope, conducts analysis on each image to identify interesting astrophysical objects, and collects statistics about them.

## Features
- **Image Processing**: Utilizes OpenCV for image processing tasks such as filtering, edge detection, and contour finding.
- **Parallel Computing**: Employs multiprocessing to distribute the image analysis tasks across multiple CPU cores, enhancing efficiency and speed.
- **Object Classification**: Classifies identified objects based on area and brightness criteria, distinguishing between stars, comets, planets, galaxies, and quasars.
- **Visualization**: Provides visual feedback by drawing bounding boxes around detected objects and annotating them with their types.

## Installation
1. Clone the repository: `git clone https://github.com/username/repository.git`
2. Navigate to the project directory: `cd repository`
3. Install the required dependencies: `pip install -r requirements.txt`

## Usage
1. Ensure you have a space image containing the desired objects.
2. Launch the application.
3. Click on the "Load Image" button to select and load the image file.
4. Once the image is loaded, click on the "Start Analysis" button to initiate the parallel processing of the image.
5. After all processes are completed, the result will be available in the "image_result" folder.

## Dependencies
- OpenCV (`opencv-python`)
- NumPy (`numpy`)
- Pillow (`Pillow`)
- Multiprocessing (`multiprocessing`)
- Tkinter (`tkinter`)
