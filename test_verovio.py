import verovio
from pathlib import Path

xml = Path("test_score.xml").read_text(encoding="utf-8-sig")

tk = verovio.toolkit()

print("Verovio version:", tk.getVersion())
print("XML length:", len(xml))
print("XML beginning:", xml[:150])

tk.setOptions({
    "inputFrom": "musicxml",
    "pageWidth": 1400,
    "scale": 45,
})

result = tk.loadData(xml)

print("Load result:", result)
print("Page count:", tk.getPageCount())

if tk.getPageCount() > 0:
    Path("test_preview.svg").write_text(
        tk.renderToSVG(1),
        encoding="utf-8"
    )
    print("SVG created successfully!")
else:
    print("Verovio could not render the score.")