import sys
import subprocess


CONFIG = {
    5: {
        "audio": "Audio/5-matthieu-amiguet-python-for-live-music.flac",
        "video": "Video/block3.mp4",
        "video_offset": {
            "start": 29.45,
            "end": 46.0 * 60 + 53,
        },
        "output": "Video/5-matthieu-amiguet-python-for-live-music.mp4",
    }
}


def process(item):
    audio = item['audio']
    video = item['video']
    offset = (item['video_offset']['start'], item['video_offset']['end'])
    print('--> Using audio "%s"...' % audio)
    print('--> Using video "%s"...' % video)
    command = [
        'ffmpeg',
        # Input files
        '-ss', str(offset[0]),
        '-t', str(offset[1]),
        '-i', video,
        '-i', audio,
        # Codecs
        '-codec:v', 'h264',
        '-codec:a', 'aac',
        # Bitrate and framerate
        '-b:v', '8000k',
        '-b:a', '384k',
        '-r:v', '25',
        # Input channel mapping
        '-map', '0:v:0',
        '-map', '1:a:0',
        #'-filter_complex', 'amix=inputs=2:duration=first',
        # Video filters
        '-filter:v', 'hqdn3d',
        # Other options
        '-strict', '-2',
        # Duration of video
        '-t', str(offset[1] - offset[0]),
        # Output file
        item['output'],
    ]
    print('--> Running: %s' % ' '.join(command))
    subprocess.check_call(command)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: ./%s <talk-nr>' % sys.argv[0])
        print('Example for second talk: ./%s 2' % sys.argv[0])
        sys.exit(1)
    nr = int(sys.argv[1])
    if nr not in CONFIG:
        print('%s is not a valid talk number.' % nr)
        print('Choose from: %s' % list(CONFIG.keys()))
        sys.exit(1)
    print('Processing talk number %s...' % nr)
    process(CONFIG[nr])