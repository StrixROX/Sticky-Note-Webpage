# 🧩 StickyPages

> _A small PyQt experiment so that I could pin my Notion pages to my desktop like post-it notes._

**StickyPages** is a minimal frameless desktop browser window built with **PyQt6** and **QtWebEngine**.  
It lets you “stick” any webpage onto your desktop in a stylish, rounded, translucent frame.

## ✨ Features

- 🌐 Displays any webpage (customizable via `config.json`)
- 🪟 Frameless and translucent window
- 🖼️ Rounded corners with adjustable border
- ⚙️ Simple JSON-based configuration
- ⌨️ Supports `Alt + F4` to close cleanly

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/StrixROX/Sticky-Note-Webpage.git
cd sticky-pages
pip install -r requirements.txt
````

## 🚀 Usage

1. (Optional) Edit `config.json` to customize the window (size, border, or webpage URL).
2. Run the app:

```bash
python main.py
```

The window will open at the specified position or center itself if `xPos`/`yPos` are `null`.

> **Update**: You can pass the argument ```[-u URL]``` to override the webpage URL from the command line, for usage with scripts etc. Run ```python main.py -h``` for help.

## ⚙️ Configuration

You can control the appearance and behavior of the window via `config.json`.
If the file is missing or incomplete, defaults will be used automatically.

Example:

```json
{
  "width": 800,
  "height": 600,
  "xPos": 50,
  "yPos": 50,
  "webpageUrl": "https://www.google.com",
  "cornerRadius": 10,
  "borderWidth": 8,
  "borderColor": "rgba(255, 255, 255, 0.7)"
}
```

| Key               | Type          | Description                                                 |
| ----------------- | ------------- | ----------------------------------------------------------- |
| `width`, `height` | number        | Window dimensions                                           |
| `xPos`, `yPos`    | number / null | Window position (top-left origin). Set to `null` to center. |
| `webpageUrl`      | string        | The webpage to load                                         |
| `cornerRadius`    | number        | Corner roundness in pixels                                  |
| `borderWidth`     | number        | Border thickness in pixels                                  |
| `borderColor`     | string        | RGBA color for border (supports transparency)               |

## 🧩 Project Structure

```
StickyPages/
├── main.py          # Main application code
├── config.json      # Configuration file
├── requirements.txt # Dependencies
└── README.md        # Documentation
```

## 🧠 Notes

* The app uses **PyQt6** and **QtWebEngine** for rendering web content.
* The window is **non-resizable** and **frameless**.
* Border and corner radius are applied using Qt’s painter masks.
* Press **Alt + F4** to close the window cleanly.

## 💡 Future Scope

* Drag-to-move functionality
* Optional always-on-top mode
* Configurable transparency
* System tray integration

### 🧑‍💻 Author

Created by **Pratyush Kumar**
