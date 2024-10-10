import requests

urls = {
    "white_king": "https://upload.wikimedia.org/wikipedia/commons/4/42/Chess_klt45.svg",
    "white_queen": "https://upload.wikimedia.org/wikipedia/commons/1/15/Chess_qlt45.svg",
    "white_rook": "https://upload.wikimedia.org/wikipedia/commons/7/72/Chess_rlt45.svg",
    "white_bishop": "https://upload.wikimedia.org/wikipedia/commons/b/b1/Chess_blt45.svg",
    "white_knight": "https://upload.wikimedia.org/wikipedia/commons/7/70/Chess_nlt45.svg",
    "white_pawn": "https://upload.wikimedia.org/wikipedia/commons/4/45/Chess_plt45.svg",
    "black_king": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Chess_kdt45.svg",
    "black_queen": "https://upload.wikimedia.org/wikipedia/commons/4/47/Chess_qdt45.svg",
    "black_rook": "https://upload.wikimedia.org/wikipedia/commons/f/ff/Chess_rdt45.svg",
    "black_bishop": "https://upload.wikimedia.org/wikipedia/commons/9/98/Chess_bdt45.svg",
    "black_knight": "https://upload.wikimedia.org/wikipedia/commons/e/ef/Chess_ndt45.svg",
    "black_pawn": "https://upload.wikimedia.org/wikipedia/commons/c/c7/Chess_pdt45.svg",
}

# Function to download SVG files
def download_svg(name, url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(f"{name}.svg", "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"{name}.svg downloaded successfully.")
    else:
        print(f"Failed to download {name}.svg")

# Download all SVG files
for name, url in urls.items():
    download_svg(name, url)
