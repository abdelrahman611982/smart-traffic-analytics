from ultralytics import YOLO
import cv2
import numpy as np
import os
import csv
import time


# ==========================================
# Settings
# ==========================================

images_path = "MVI_40191"
output_path = "traffic_tracking.mp4"

vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck


# ==========================================
# Initialize YOLO Model
# ==========================================

model = YOLO("yolo11n.pt")


# ==========================================
# Get Frames
# ==========================================

frames = sorted([
    f for f in os.listdir(images_path) 
    if f.lower().endswith((".jpg", ".png", ".jpeg"))])

print("Number of frames:", len(frames))


# ==========================================
# Read First Frame
# ==========================================

first_frame = cv2.imread(os.path.join(images_path, frames[0]))

if first_frame is None:
    raise ValueError("Could not read first frame")

height, width = first_frame.shape[:2]


# ==========================================
# Create Output Video
# ==========================================

fourcc = cv2.VideoWriter_fourcc(*"avc1")

writer = cv2.VideoWriter(output_path, 
                         fourcc, 
                         25, 
                         (width, height))


# ==========================================
# Counting Variables
# ==========================================

LINE_Y = 300

counted_ids = set()

total_count = 0

vehicle_counts = {
    "car": 0,
    "motorcycle": 0,
    "bus": 0,
    "truck": 0
}

previous_positions = {}


# ==========================================
# ROI Coordinates for Traffic Density
# ==========================================

LEFT_ROI = np.array([(514, 17), 
                     (415, 535), 
                     (7, 533), 
                     (6, 106), 
                     (443, 20)], 
                     dtype=np.int32)

RIGHT_ROI = np.array([(528, 21), 
                      (597, 539), 
                      (953, 533), 
                      (957, 77), 
                      (596, 18)], 
                      dtype=np.int32)

density_history = []


# ==========================================
# Tracking Loop
# ==========================================

start_time = time.perf_counter()

for i, frame_name in enumerate(frames):

    frame_path = os.path.join(images_path, frame_name)

    frame = cv2.imread(frame_path)

    if frame is None:
        print("Could not read frame:", frame_name)
        continue


    # ======================================
    # Traffic Density IDs
    # ======================================

    left_vehicle_ids = set()
    right_vehicle_ids = set()


    # ======================================
    # YOLO + BoT-SORT
    # ======================================

    results = model.track(frame, 
                          classes=vehicle_classes, 
                          tracker="botsort.yaml", 
                          persist=True, 
                          verbose=False)

    result = results[0]


    # ======================================
    # Process Tracks
    # ======================================

    if result.boxes is not None and result.boxes.id is not None:

        boxes = result.boxes.xyxy.cpu().numpy()
        track_ids = result.boxes.id.int().cpu().tolist()
        classes = result.boxes.cls.int().cpu().tolist()


        # ==================================
        # Process Each Vehicle
        # ==================================

        for box, track_id, class_id in zip(boxes, track_ids, classes):

            x1, y1, x2, y2 = map(int, box)


            # ==================================
            # Center of Bounding Box
            # ==================================

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            center = (center_x, center_y)


            # ==================================
            # Check Traffic ROI
            # ==================================

            inside_left = cv2.pointPolygonTest(LEFT_ROI, center, False)
            inside_right = cv2.pointPolygonTest(RIGHT_ROI, center, False)


            if inside_left >= 0:
                left_vehicle_ids.add(track_id)

            if inside_right >= 0:
                right_vehicle_ids.add(track_id)


            # ==================================
            # Line Crossing
            # ==================================

            if track_id in previous_positions:

                previous_y = previous_positions[track_id]

                crossed_down = previous_y < LINE_Y and center_y >= LINE_Y

                crossed_up = previous_y > LINE_Y and center_y <= LINE_Y

                crossed = crossed_down or crossed_up


                # Count only once

                if crossed and track_id not in counted_ids:

                    counted_ids.add(track_id)

                    total_count += 1

                    class_name = model.names[class_id]

                    if class_name in vehicle_counts:
                        vehicle_counts[class_name] += 1


            # ==================================
            # Update Previous Position
            # ==================================

            previous_positions[track_id] = center_y


            # ==================================
            # Draw Bounding Box
            # ==================================

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)


            # ==================================
            # Draw ID + Class
            # ==================================

            label = f"{model.names[class_id]} ID: {track_id}"

            cv2.putText(frame, 
                        label, 
                        (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.5,
                        (0, 255, 0), 
                        2
                        )


    # ==========================================
    # Calculate Traffic Density
    # ==========================================

    left_density = len(left_vehicle_ids)
    right_density = len(right_vehicle_ids)

    all_vehicle_ids = left_vehicle_ids | right_vehicle_ids
    total_density = len(all_vehicle_ids)

    density_history.append({"frame": i, "time": i / 25, "left_density": left_density, 
                            "right_density": right_density, "total_density": total_density})


    # ==========================================
    # Draw Traffic ROIs
    # ==========================================

    cv2.polylines(frame, [LEFT_ROI], True, (0, 255, 0), 3)
    cv2.polylines(frame, [RIGHT_ROI], True, (0, 0, 255), 3)


    # ==========================================
    # Draw Counting Line
    # ==========================================

    cv2.line(frame, 
             (0, LINE_Y), 
             (width, LINE_Y), 
             (255, 0, 0), 
             3
             )

    cv2.putText(frame, 
                "COUNTING LINE", 
                (20, LINE_Y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, 
                (255, 0, 0), 
                2
                )


    # ==========================================
    # Draw Information Panel
    # ==========================================

    cv2.rectangle(frame, 
                  (10, 10), 
                  (330, 175), 
                  (0, 0, 0), 
                  -1)


    # ==========================================
    # Line Crossing Count
    # ==========================================

    cv2.putText(frame, 
                f"Total Count: {total_count}", 
                (20, 35), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.6, 
                (255, 255, 255), 
                2
                )


    # ==========================================
    # Vehicle Type Counts
    # ==========================================

    cv2.putText(frame, f"Cars: {vehicle_counts['car']}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.putText(frame, f"Motorcycles: {vehicle_counts['motorcycle']}", (20, 82), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.putText(frame, f"Buses: {vehicle_counts['bus']}", (20, 104), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.putText(frame, f"Trucks: {vehicle_counts['truck']}", (20, 126), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


    # ==========================================
    # Traffic Density
    # ==========================================

    cv2.putText(frame, 
                f"Density L/R/T: {left_density}/{right_density}/{total_density}", 
                (20, 155), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, 
                (255, 255, 255), 
                2
                )


    # ==========================================
    # Save Frame
    # ==========================================

    writer.write(frame)


    # ==========================================
    # Progress
    # ==========================================

    if (i + 1) % 100 == 0:
        print(f"Processed {i + 1}/{len(frames)} frames")


# ==========================================
# Finish
# ==========================================

writer.release()


with open("traffic_density.csv", "w", newline="") as file:

    writer_csv = csv.DictWriter(file, 
    fieldnames=["frame", "time", "left_density", "right_density", "total_density"])

    writer_csv.writeheader()

    writer_csv.writerows(density_history)


end_time = time.perf_counter()

processing_time = end_time - start_time

processing_fps = len(frames) / processing_time


print("\n===================================")
print("DONE")
print("===================================")

print("Processed frames:", len(frames))

print(f"Processing time: {processing_time:.2f} seconds")

print(f"Processing FPS: {processing_fps:.2f}")


print("\nVehicle Counts:")

print("Cars:", vehicle_counts["car"])

print("Motorcycles:", vehicle_counts["motorcycle"])

print("Buses:", vehicle_counts["bus"])

print("Trucks:", vehicle_counts["truck"])

print("\nTotal vehicles counted:", total_count)

print("\nOutput video:", output_path)