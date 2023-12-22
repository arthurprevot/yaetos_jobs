from yaetos.etl_utils import ETL_Base, Commandliner
import cv2

class Job(ETL_Base):
    def transform(self, listing):
        listing.foreach(transform_one_image)
        return listing

def transform_one_image(row):
    file_path = row.file_dir + row.file_name
    print(f"->Loading: {file_path}")

    # Load the image from file
    image = cv2.imread(file_path, 0)

    # Apply GaussianBlur to reduce image noise if it is required
    image_blur = cv2.GaussianBlur(image, (5, 5), 0)

    # Convert to binary image through thresholding
    _, image_thresh = cv2.threshold(image_blur, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours from the binary image
    contours, hierarchy = cv2.findContours(image_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw all contours on the original image
    image_contours = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # Convert to BGR for coloring the contours
    cv2.drawContours(image_contours, contours, -1, (0, 255, 0), 1)  # Draw contours in green

    # Save the image with contours to a file and output the path
    output_path = row.file_dir_out + row.file_name
    cv2.imwrite(output_path, image_contours)
    return True


if __name__ == "__main__":
    args = {'job_param_file': 'conf/jobs_metadata.yml'}
    Commandliner(Job, **args)
