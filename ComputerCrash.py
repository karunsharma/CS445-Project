import subprocess, sys
osopener = "open" if sys.platform == "darwin" else "xdg-open"
while True:
	subprocess.call([osopener,"content.txt"])