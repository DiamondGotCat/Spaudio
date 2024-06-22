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
    parser.add_argument("--room_dim", type=float, nargs=3, default=[5.0, 4.0, 3.0], help="Dimensions of the room [x, y, z]")
    parser.add_argument("--source_positions", type=float, nargs='+', default=[2.0, 1.0, 1.5, 3.0, 3.0, 1.5], help="Positions of the audio sources [x1, y1, z1, x2, y2, z2]")
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
        room = pra.ShoeBox(room_dim, fs=sample_rate, max_order=5, absorption=0.4)

        # Source positions
        source_positions = np.array(args.source_positions).reshape(-1, 3)

        # Separate audio channels
        channels = [audio_data[:, i] for i in range(audio_data.shape[1])]

        # Add source audio
        for i, (pos, channel) in enumerate(zip(source_positions, channels)):
            room.add_source(pos, signal=channel)

        # Add 2 microphone array
        mic_positions = np.array([
            [4.5, 1.0, 1.5],
            [4.5, 3.0, 1.5]
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
