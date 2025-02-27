import matplotlib.pyplot as plt
from matplotlib import patches

def display_object_detection(image, detections):
    fig, ax = plt.subplots(figsize=(16, 16))
    ax.imshow(image)

    for i, detection in enumerate(detections):
        detection_box = detection['box']
        detection_origin = (detection_box['xmin'], detection_box['ymin'])
        detection_width = detection_box['xmax'] - detection_box['xmin']
        detection_height = detection_box['ymax'] - detection_box['ymin']
        detection_rect = patches.Rectangle(
            detection_origin,
            width=detection_width,
            height=detection_height,
            linewidth=2,
            edgecolor='red',
            facecolor='none',
        )
        ax.add_patch(detection_rect)

        label = f'{detection["label"]} {100 * detection["score"]:.2f}'
        ax.text(
            detection_box['xmin'],
            detection_box['ymin'] - 15,
            label,
            bbox={'facecolor': 'red', 'alpha': 0.8},
        )

    plt.show()
