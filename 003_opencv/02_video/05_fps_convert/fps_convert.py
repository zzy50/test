import matplotlib.pyplot as plt

def simulate_fps_conversion(original_fps, target_fps, total_frames):
    frame_skip_ratio = original_fps / target_fps
    cumulative_error = 0.0
    cumulative_error_lst = []
    selected_frames_lst = []
    dropped_frames_lst = []

    for frame in range(total_frames):
        cumulative_error += 1.0
        if cumulative_error >= frame_skip_ratio:
            cumulative_error -= frame_skip_ratio
            selected_frames_lst.append(frame)
        else:
            dropped_frames_lst.append(frame)
        cumulative_error_lst.append(cumulative_error)

    return selected_frames_lst, dropped_frames_lst, cumulative_error_lst

original_fps = 16
target_fps = 15
total_frames = 100
selected_frames_lst, dropped_frames_lst, cumulative_error_lst = simulate_fps_conversion(original_fps, target_fps, total_frames)

plt.figure(figsize=(12, 6))
# for frame in selected_frames:
#     plt.axvline(x=frame, color='blue', ymin=0.49, ymax=0.54, linewidth=1, linestyle='-')
plt.plot(selected_frames_lst, [1] * len(selected_frames_lst), color='b', marker='o', label='Selected Frames', linestyle="")
plt.plot(dropped_frames_lst, [1] * len(dropped_frames_lst), color='r', marker='o', label='Dropped Frames', linestyle="")
plt.plot(cumulative_error_lst, linestyle="-", color='r', label='Cumulative Error', linewidth=0.5)
plt.xlabel('Frame Number')
plt.ylabel('Cumulative Error')
plt.title(f'Frame Selection (Original FPS: {original_fps}, Target FPS: {target_fps})')
plt.grid(True)
plt.legend()
plt.show()
