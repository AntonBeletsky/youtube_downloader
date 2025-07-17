from pytubefix import YouTube
import os

def main():
    # Get input from user
    url = input("Enter the YouTube video URL: ").strip()
    download_path = input("Enter folder to save the file (e.g., C:/Videos): ").strip()

    # Create folder if it doesn't exist
    if not os.path.exists(download_path):
        print(f"📁 Folder '{download_path}' not found. Creating...")
        os.makedirs(download_path)

    try:
        yt = YouTube(url)
    except Exception as e:
        print(f"❌ Failed to fetch video: {e}")
        return

    title = yt.title or "video"
    filename = f"{title}.mp4"
    filepath = os.path.join(download_path, filename)

    # Check if file already exists
    if os.path.isfile(filepath):
        print(f"⚠️ File already exists: '{filepath}'")
        choice = input("Do you want to download it again? (y/n): ").strip().lower()
        if choice != 'y':
            print("🚫 Download canceled.")
            return

    # Get the best progressive stream (contains both video + audio)
    stream = yt.streams.filter(progressive=True, file_extension='mp4')\
                       .order_by('resolution').desc().first()

    if stream is None:
        print("❌ No compatible stream found with both video and audio.")
        return

    print("⏳ Downloading...")
    stream.download(output_path=download_path, filename=filename)
    print(f"✅ Download complete: '{filepath}'")

if __name__ == "__main__":
    main()
