import os
import io
import math
from PIL import Image, ImageDraw, ImageFont

def _creer_calque_filigrane_repete(width, height, text, opacity):
    """Crée une image transparente contenant le texte en filigrane répété."""
    diag = int((width**2 + height**2)**0.5)
    canvas_size = diag
    
    tiled = Image.new('RGBA', (canvas_size, canvas_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(tiled)

    # La taille de la police s'adapte à la longueur du texte
    # Plus le texte est long, plus la police est petite.
    font_size = int((width / max(len(text), 1)) * 1.5)
    
    # On met une limite max pour les textes très courts
    max_font = int(width * 0.05)
    if font_size > max_font: font_size = max_font
    if font_size < 12: font_size = 12
    
    font_path = os.path.join(os.path.dirname(__file__), "assets", "fonts", "Roboto-Regular.ttf")
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        text_width, text_height = draw.textsize(text, font=font)

    step_x = text_width + 80
    step_y = text_height * 5

    for y in range(0, canvas_size, int(step_y)):
        for x in range(0, canvas_size, int(step_x)):
            offset_x = x + ( (y // int(step_y)) % 2 ) * (step_x / 2)
            draw.text((offset_x, y), text, font=font, fill=(128, 128, 128, opacity))
    
    tiled = tiled.rotate(45, center=(canvas_size/2, canvas_size/2), resample=Image.BICUBIC)
    
    left = (canvas_size - width) / 2
    top = (canvas_size - height) / 2
    right = left + width
    bottom = top + height
    
    return tiled.crop((left, top, right, bottom))

def traiter_image(image_path, pdf_path, text, opacity=128):
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size

    txt_img = _creer_calque_filigrane_repete(width, height, text, opacity)

    watermarked_img = Image.alpha_composite(img, txt_img)
    final_img = watermarked_img.convert("RGB")
    final_img.save(pdf_path, "PDF", resolution=100.0)

def traiter_pdf(input_pdf_path, output_pdf_path, text, opacity=128):
    from pypdf import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    # On crée une seule page de filigrane par taille de page différente (souvent 1 seule suffit)
    watermarks_cache = {}
    
    alpha = opacity / 255.0
    
    for page in reader.pages:
        # Dimensions de la page
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        
        # Clé de cache pour éviter de regénérer si la taille est la même
        dim_key = (width, height)
        
        if dim_key not in watermarks_cache:
            packet = io.BytesIO()
            c = canvas.Canvas(packet, pagesize=(width, height))
            
            # Taille adaptative selon la longueur du texte
            font_size = (width / max(len(text), 1)) * 1.5
            max_font = width * 0.05
            if font_size > max_font: font_size = max_font
            if font_size < 10: font_size = 10
                
            c.setFont("Helvetica", font_size)
            # Couleur grise avec transparence gérée par reportlab
            c.setFillColorRGB(0.5, 0.5, 0.5, alpha=alpha)
            
            text_width = c.stringWidth(text, "Helvetica", font_size)
            
            step_x = text_width + 80
            step_y = font_size * 5
            
            # Rotation globale du canvas au centre
            c.translate(width/2, height/2)
            c.rotate(45)
            
            # Tiling
            max_dim = max(width, height) * 2
            for y in range(int(-max_dim), int(max_dim), int(step_y)):
                for x in range(int(-max_dim), int(max_dim), int(step_x)):
                    offset_x = x + ( (y // int(step_y)) % 2 ) * (step_x / 2)
                    c.drawString(offset_x, y, text)
                    
            c.save()
            packet.seek(0)
            
            watermark_pdf = PdfReader(packet)
            watermarks_cache[dim_key] = watermark_pdf.pages[0]
            
        # On fusionne la page originale avec notre calque filigrane (compatible Acrobat 100%)
        page.merge_page(watermarks_cache[dim_key])
        writer.add_page(page)
        
    with open(output_pdf_path, "wb") as out_file:
        writer.write(out_file)

def ajouter_filigrane_et_creer_pdf(input_path, pdf_path, text, opacity=128):
    try:
        if input_path.lower().endswith('.pdf'):
            traiter_pdf(input_path, pdf_path, text, opacity)
        else:
            traiter_image(input_path, pdf_path, text, opacity)
        print(f"Succès ! Le fichier a été généré avec le filigrane : {pdf_path}")
    except ImportError:
        print("Erreur : Des bibliothèques manquent. Veuillez lancer : pip install -r requirements.txt")
    except Exception as e:
        print(f"Une erreur est survenue lors de la création du document : {e}")
