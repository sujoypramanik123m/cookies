import subprocess

async def compress_video(input_path, output_path, codec="libx265", crf=28):
    try:
        command = [
            "ffmpeg",
            "-i", input_path,
            "-vcodec", codec,
            "-crf", str(crf),
            "-preset", "fast",
            output_path
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise Exception(stderr.decode())
        return output_path
    except Exception as e:
        print(f"Error compressing video: {e}")
        return None
