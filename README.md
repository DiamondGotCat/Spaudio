# Spaudio: Spatial Audio Simulation Tool
Spaudio is a Python application designed to simulate spatial audio effects in a virtual 3D room environment. By leveraging the power of Pyroomacoustics and Pydub, Spaudio provides users with the ability to create realistic acoustic simulations, ideal for research, audio engineering, and immersive sound design.

## Features

- **Audio File Input**: Load your audio files in various formats.
- **3D Room Simulation**: Define a room with customizable dimensions and simulate how sound propagates within it.
- **Multiple Sources and Microphones**: Add multiple sound sources and microphones to capture the spatial audio effect.
- **Audio Output**: Save the simulated audio to a file or play it directly through your speakers.

## About default settings
Please use headphones/earphones.

### Normal mode

You can experience 3D audio to a reasonable degree while maintaining compatibility.

### Stereo mode

It gives you the experience of having a privileged seat in front of a high-quality TV, but the audio files must be stereo compatible.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.x
- Pyroomacoustics
- Pydub
- ffmpeg (for Pydub)

### Installation

Clone the repository and install the required packages:

```bash
git clone https://github.com/DiamondGotCat/Spaudio.git
cd spaudio
pip install -r requirements.txt
```

### Usage

To run Spaudio, use the following command:

```bash
python spaudio.py <audio_file> [--output_file <output_file>] [--room_dim <x> <y> <z>] [--source_position <x> <y> <z>]
```

- `<audio_file>`: Path to the input audio file.
- `--output_file <output_file>`: (Optional) Path to save the output audio file.
- `--room_dim <x> <y> <z>`: (Optional) Room dimensions.
- `--source_position <x> <y> <z>`: (Optional) Source position.
- `--source_position <x> <y> <z> <x2> <y2> <z2>`: (Optional) Source position for stereo-mode.

**(Replacing spaudio.py with spaudio-stereo.py will improve the sound quality)**

### Example

**Simulate an audio file and play it back:**

```bash
python spaudio.py input.wav
```

**Simulate an audio file and save the output:**

```bash
python spaudio.py input.wav --output_file output.wav
```

**(Replacing spaudio.py with spaudio-stereo.py will improve the sound quality)**

## Default
![スクリーンショット 2024-06-23 21 16 58](https://github.com/DiamondGotCat/Spaudio/assets/124330624/bd20b0fc-9a7e-4f2f-9b3d-733236d6ed44)


**(Square: Speaker ,Circle: Microphone)**

## Code Explanation

1. **Loading Audio**: The script loads the input audio file using Pydub and extracts the audio data and sample rate.
2. **Audio Normalization**: The audio data is normalized to ensure consistent amplitude levels.
3. **Room Configuration**: A 3D room environment is defined with specified dimensions and acoustic properties.
4. **Source and Microphone Placement**: Multiple sound sources and microphones are positioned within the room to capture the spatial audio effect.
5. **Simulation**: Pyroomacoustics simulates the sound propagation and captures the audio signals at each microphone.
6. **Output**: The simulated audio can be saved to a file or played back directly.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Pyroomacoustics: https://github.com/LCAV/pyroomacoustics
- Pydub: https://github.com/jiaaro/pydub

Enjoy creating immersive audio experiences with Spaudio!
