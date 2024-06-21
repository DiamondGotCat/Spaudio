import pyroomacoustics as pra
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="spaudio")
    parser.add_argument("audio_file", type=str, help="Path to the input audio file")
    parser.add_argument("--output_file", type=str, help="Path to save the output audio file", default=None)
    parser.add_argument("--room_dim", type=float, nargs=3, default=[3.18, 3.18, 3.18], help="Dimensions of the room [x, y, z]")
    parser.add_argument("--source_position", type=float, nargs=3, default=[1.82, 0, 1.25], help="Position of the audio source [x, y, z]")
    args = parser.parse_args()

    try:
        # Load file
        audio_file_path = args.audio_file.replace("\\", "").strip()
        audio = AudioSegment.from_file(audio_file_path)

        # Load Sample rate and Audio data
        sample_rate = audio.frame_rate
        audio_data = np.array(audio.get_array_of_samples()).reshape((-1, audio.channels))

        # Normalize audio data
        audio_data = audio_data / np.max(np.abs(audio_data))

        # Room dimension
        room_dim = args.room_dim

        # Create Room
        room = pra.ShoeBox(room_dim, fs=sample_rate, max_order=10, absorption=0.2)

        # Source position
        source_position = args.source_position

        # Separate audio channels
        channels = [audio_data[:, i] for i in range(audio_data.shape[1])]

        # Add source audio
        for i, channel in enumerate(channels):
            room.add_source([source_position[0] + i * 0.1, source_position[1], source_position[2]], signal=channel)

        # Add 8 microphone array
        mic_positions = np.array([
            [1.82, 1.36, 1.25],
            [2.00, 1.36, 1.25],
            [1.64, 1.36, 1.25],
            [1.82, 1.54, 1.25],
            [1.82, 1.18, 1.25],
            [2.00, 1.54, 1.25],
            [1.64, 1.18, 1.25],
            [2.00, 1.18, 1.25]
        ]).T

        mic_array = pra.MicrophoneArray(mic_positions, room.fs)
        room.add_microphone_array(mic_array)

        # Simulate sound
        room.simulate()

        # Get Simulated result
        simulated_audio_data = room.mic_array.signals

        # Normalize Simulated Audio data
        simulated_audio_data = simulated_audio_data.astype(np.float32)
        simulated_audio_data = simulated_audio_data / np.max(np.abs(simulated_audio_data))

        # Downmix to stereo if necessary
        if simulated_audio_data.shape[0] > 2:
            simulated_audio_data = simulated_audio_data[:2]

        # Convert
        channels = simulated_audio_data.shape[0]
        simulated_audio_segment = AudioSegment(
            data=(simulated_audio_data.T * 32767).astype(np.int16).tobytes(),
            frame_rate=sample_rate,
            sample_width=2,
            channels=channels
        )

        if args.output_file:
            # Export as audio file
            output_file_path = args.output_file.replace("\\", "").strip()
            simulated_audio_segment.export(output_file_path, format=os.path.splitext(output_file_path)[-1][1:])
            print(f"Saved to '{output_file_path}'.")
        else:
            # Play audio file
            play(simulated_audio_segment)

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
