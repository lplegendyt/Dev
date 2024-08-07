from PIL import Image
import pytesseract

# Pfad zur Tesseract-Executable auf Windows angeben
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Erstellen Sie ein einfaches Testbild oder verwenden Sie ein vorhandenes Bild mit Text
test_image_path = 'test_image.png'  # Ersetzen Sie dies durch den Pfad zu Ihrem Testbild
image = Image.open(test_image_path)

# Text aus dem Bild extrahieren
text = pytesseract.image_to_string(image)

print(f"Extracted text: {text}")
