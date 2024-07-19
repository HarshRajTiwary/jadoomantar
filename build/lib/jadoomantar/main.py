import cv2
import numpy as np
import time

# Function to capture the background
def capture_background(cap, num_frames=30):
    for i in range(num_frames):
        ret, background = cap.read()
    return background

# Function to capture the cloak color
def capture_cloak_color(cap, num_frames=30):
    cloak_samples = []
    for i in range(num_frames):
        ret, frame = cap.read()
        if ret:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            cloak_samples.append(hsv.reshape(-1, 3))
    cloak_samples = np.concatenate(cloak_samples, axis=0)
    return cloak_samples

# Function to create a mask for the cloak
def create_mask(frame, lower_bound, upper_bound):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations=2)
    mask = cv2.dilate(mask, np.ones((3,3), np.uint8), iterations=1)
    return mask

# Function to apply the cloak effect
def apply_cloak_effect(frame, background, mask):
    mask_inv = cv2.bitwise_not(mask)
    res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)
    res2 = cv2.bitwise_and(background, background, mask=mask)
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
    return final_output

# Function to calculate HSV bounds from cloak samples
def calculate_hsv_bounds(cloak_samples, tolerance=40):
    hsv_means = np.mean(cloak_samples, axis=0)
    lower_bound = np.clip(hsv_means - tolerance, 0, 255).astype(int)
    upper_bound = np.clip(hsv_means + tolerance, 0, 255).astype(int)
    return lower_bound, upper_bound

# Main function to integrate everything
def invisibility_cloak():
    cap = cv2.VideoCapture(0)
    time.sleep(2)
    
    print("Capturing background...")
    background = capture_background(cap, num_frames=60)  # Capturing background for 60 frames

    print("Please show the cloak to the camera...")
    time.sleep(2)
    cloak_samples = capture_cloak_color(cap, num_frames=60)  # Capturing cloak samples for 60 frames
    
    lower_bound, upper_bound = calculate_hsv_bounds(cloak_samples)
    
    print(f"Lower bound: {lower_bound}")
    print(f"Upper bound: {upper_bound}")

    print("Starting invisibility cloak effect...")

    # Check if we can create a window
    try:
        cv2.namedWindow('Invisibility Cloak', cv2.WINDOW_NORMAL)
        show_preview = True
    except cv2.error as e:
        print("Unable to create window, running in headless mode.")
        show_preview = False

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        mask = create_mask(frame, lower_bound, upper_bound)
        final_output = apply_cloak_effect(frame, background, mask)
        
        out.write(final_output)

        if show_preview:
            cv2.imshow('Invisibility Cloak', final_output)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    out.release()
    if show_preview:
        cv2.destroyAllWindows()

# Run the program
if __name__ == "__main__":
    invisibility_cloak()
