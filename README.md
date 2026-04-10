# image_flipper

This is a very simple ros package that produces a node to rotate an image topic 180 degrees.

## Usage
```bash
ros2 run image_flipper_pkg image_flipper --ros-args -p input_topic:=/your/camera/image_raw -p output_topic:=/your/camera/image_flipped
```