import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# Load Density Data
# ==========================================

df = pd.read_csv("traffic_density.csv")


# ==========================================
# Basic Statistics
# ==========================================

average_density = df["total_density"].mean()
maximum_density = df["total_density"].max()
minimum_density = df["total_density"].min()


# ==========================================
# Peak Time
# ==========================================

peak_index = df["total_density"].idxmax()
peak_time = df.loc[peak_index, "time"]


# ==========================================
# Average Density by Direction
# ==========================================

average_left = df["left_density"].mean()
average_right = df["right_density"].mean()


# ==========================================
# Print Statistics
# ==========================================

print("\n===================================")
print("TRAFFIC ANALYTICS")
print("===================================")

print(f"Average Density: {average_density:.2f}")
print(f"Maximum Density: {maximum_density}")
print(f"Minimum Density: {minimum_density}")
print(f"Peak Time: {peak_time:.2f} seconds")
print(f"Average Left Density: {average_left:.2f}")
print(f"Average Right Density: {average_right:.2f}")


# ==========================================
# Density Graph
# ==========================================

plt.figure(figsize=(10, 5))

plt.plot(df["time"], df["total_density"])

plt.xlabel("Time (seconds)")
plt.ylabel("Number of Vehicles")
plt.title("Traffic Density Over Time")
plt.grid()

plt.show()