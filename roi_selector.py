import cv2
import numpy as np


# ==========================================
# Settings
# ==========================================

image_path = "MVI_40191/img00001.jpg"

MAX_POINTS = 5


# ==========================================
# Read Image
# ==========================================

image = cv2.imread(image_path)

if image is None:
    raise ValueError("Could not read image")


# ==========================================
# ROI Points
# ==========================================

left_points = []
right_points = []

current_roi = "left"


# ==========================================
# Mouse Callback
# ==========================================

def mouse_callback(event, x, y, flags, param):

    global current_roi

    if event != cv2.EVENT_LBUTTONDOWN:
        return

    # --------------------------------------
    # LEFT ROI
    # --------------------------------------

    if current_roi == "left":

        if len(left_points) < MAX_POINTS:

            left_points.append((x, y))

            print(
                f"LEFT Point {len(left_points)}: "
                f"({x}, {y})"
            )

        else:

            print("LEFT ROI already has 5 points.")

    # --------------------------------------
    # RIGHT ROI
    # --------------------------------------

    elif current_roi == "right":

        if len(right_points) < MAX_POINTS:

            right_points.append((x, y))

            print(
                f"RIGHT Point {len(right_points)}: "
                f"({x}, {y})"
            )

        else:

            print("RIGHT ROI already has 5 points.")


# ==========================================
# Create Window
# ==========================================

cv2.namedWindow(
    "ROI Selection",
    cv2.WINDOW_NORMAL
)

cv2.resizeWindow(
    "ROI Selection",
    960,
    540
)

cv2.setMouseCallback(
    "ROI Selection",
    mouse_callback
)


# ==========================================
# Display Loop
# ==========================================

while True:

    display = image.copy()

    # ======================================
    # Draw LEFT Points
    # ======================================

    for i, point in enumerate(left_points):

        cv2.circle(
            display,
            point,
            5,
            (0, 255, 0),
            -1
        )

        cv2.putText(
            display,
            str(i + 1),
            (point[0] + 10, point[1]),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    # ======================================
    # Draw RIGHT Points
    # ======================================

    for i, point in enumerate(right_points):

        cv2.circle(
            display,
            point,
            5,
            (0, 0, 255),
            -1
        )

        cv2.putText(
            display,
            str(i + 1),
            (point[0] + 10, point[1]),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

    # ======================================
    # Draw LEFT ROI
    # ======================================

    if len(left_points) >= 3:

        cv2.polylines(
            display,
            [np.array(left_points, dtype=np.int32)],
            True,
            (0, 255, 0),
            3
        )

    # ======================================
    # Draw RIGHT ROI
    # ======================================

    if len(right_points) >= 3:

        cv2.polylines(
            display,
            [np.array(right_points, dtype=np.int32)],
            True,
            (0, 0, 255),
            3
        )

    # ======================================
    # Instructions
    # ======================================

    cv2.putText(
        display,
        f"Selecting: {current_roi.upper()}",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        display,
        f"LEFT: {len(left_points)}/{MAX_POINTS}",
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    cv2.putText(
        display,
        f"RIGHT: {len(right_points)}/{MAX_POINTS}",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 0, 255),
        2
    )

    cv2.putText(
        display,
        "L = Select LEFT ROI",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        display,
        "R = Select RIGHT ROI",
        (20, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        display,
        "ESC = Finish",
        (20, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    # ======================================
    # Show Image
    # ======================================

    cv2.imshow(
        "ROI Selection",
        display
    )

    key = cv2.waitKey(1) & 0xFF

    # ======================================
    # Switch to LEFT
    # ======================================

    if key == ord("l"):

        current_roi = "left"

        print("\nNow selecting LEFT ROI")

    # ======================================
    # Switch to RIGHT
    # ======================================

    elif key == ord("r"):

        current_roi = "right"

        print("\nNow selecting RIGHT ROI")

    # ======================================
    # Finish
    # ======================================

    elif key == 27:

        break


# ==========================================
# Close Window
# ==========================================

cv2.destroyAllWindows()


# ==========================================
# Final Results
# ==========================================

print("\n======================================")
print("FINAL ROI COORDINATES")
print("======================================")

print("\nLEFT ROI:")

for i, point in enumerate(left_points):
    print(f"{i + 1}: {point}")

print("\nRIGHT ROI:")

for i, point in enumerate(right_points):
    print(f"{i + 1}: {point}")

print("\n======================================")