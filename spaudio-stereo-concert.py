import pyroomacoustics as pra
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import argparse
import os
from pydub.utils import which

AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

def load_audio_file(audio_file_path):
    audio = AudioSegment.from_file(audio_file_path)
    sample_rate = audio.frame_rate
    audio_data = np.array(audio.get_array_of_samples()).reshape((-1, audio.channels))
    audio_data = audio_data / np.max(np.abs(audio_data))
    return audio_data, sample_rate, audio.channels

def create_room(room_dim, sample_rate):
    # コンサートホールのような設定に変更
    room = pra.ShoeBox(room_dim, fs=sample_rate, max_order=10, absorption=0.2)
    return room

def add_sources_to_room(room, audio_data, source_positions):
    channels = [audio_data[:, i] for i in range(audio_data.shape[1])]
    for i, (pos, channel) in enumerate(zip(source_positions, channels)):
        room.add_source(pos, signal=channel)

def add_microphones_to_room(room):
    mic_positions = np.array([
        [4.5, 1.75, 1.5],
        [4.5, 2.25, 1.5]
    ]).T
    mic_array = pra.MicrophoneArray(mic_positions, room.fs)
    room.add_microphone_array(mic_array)

def simulate_room(room):
    room.simulate()
    return room.mic_array.signals

def export_audio(simulated_audio_data, sample_rate, output_file_path):
    channels = simulated_audio_data.shape[0]
    simulated_audio_segment = AudioSegment(
        data=(simulated_audio_data.T * 32767).astype(np.int16).tobytes(),
        frame_rate=sample_rate,
        sample_width=2,
        channels=channels
    )
    simulated_audio_segment.export(output_file_path, format=os.path.splitext(output_file_path)[-1][1:])

def main():
    parser = argparse.ArgumentParser(description="spaudio")
    parser.add_argument("audio_file", type=str, help="Path to the input audio file")
    parser.add_argument("--output_file", type=str, help="Path to save the output audio file", default=None)
    parser.add_argument("--room_dim", type=float, nargs=3, default=[20.0, 15.0, 10.0], help="Dimensions of the room [x, y, z]")
    parser.add_argument("--source_positions", type=float, nargs='+', default=[5, 2.75, 1.5, 5, 1.25, 1.5], help="Positions of the audio sources [x1, y1, z1, x2, y2, z2]")
    args = parser.parse_args()

    try:
        audio_data, sample_rate, channels = load_audio_file(args.audio_file)
        room = create_room(args.room_dim, sample_rate)
        source_positions = np.array(args.source_positions).reshape(-1, 3)
        if len(source_positions) != channels:
            raise ValueError("The number of source positions must match the number of audio channels.")
        add_sources_to_room(room, audio_data, source_positions)
        add_microphones_to_room(room)
        simulated_audio_data = simulate_room(room)
        simulated_audio_data = simulated_audio_data.astype(np.float32) / np.max(np.abs(simulated_audio_data))
        if simulated_audio_data.shape[0] > 2:
            simulated_audio_data = simulated_audio_data[:2]

        if args.output_file:
            export_audio(simulated_audio_data, sample_rate, args.output_file)
            print(f"Saved to '{args.output_file}'.")
        else:
            simulated_audio_segment = AudioSegment(
                data=(simulated_audio_data.T * 32767).astype(np.int16).tobytes(),
                frame_rate=sample_rate,
                sample_width=2,
                channels=simulated_audio_data.shape[0]
            )
            play(simulated_audio_segment)

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
