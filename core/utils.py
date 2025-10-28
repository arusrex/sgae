from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def redimensionar_imagem(imagem, qualidade=None, largura=None, altura=None):
    novaLargura = largura if largura else 500
    novaAltura = altura if altura else 500
    novaQualidade = qualidade if qualidade else 100

    if imagem:
        img = Image.open(imagem)

        # img = img.resize((novaLargura, novaAltura))
        img.thumbnail((novaLargura, novaAltura))

        buffer = BytesIO()
        img.save(buffer, format='PNG', quality=novaQualidade, optimize=True)
        buffer.seek(0)

        imagem_pronta = ContentFile(buffer.read(), name=imagem.name)

        return imagem_pronta
    
def tratar_imagens(imagem, qualidade=None, largura=None, altura=None):
    novaLargura = largura if largura else 500
    novaAltura = altura if altura else 500
    novaQualidade = qualidade if qualidade else 100

    fundo_branco = (255, 255, 255)

    if imagem:
        img = Image.open(imagem).convert("RGBA")
        img.thumbnail((novaLargura, novaAltura))

        imagem_com_fundo = Image.new('RGB', img.size, fundo_branco)

        if img.mode == "RGBA"
            imagem_com_fundo.paste(img, mask=img.split()[3])
        else:
            imagem_com_fundo.paste(img)

        # img = img.resize((novaLargura, novaAltura))

        buffer = BytesIO()
        imagem_com_fundo.save(buffer, format='JPEG', quality=novaQualidade, optimize=True)
        buffer.seek(0)

        imagem_pronta = ContentFile(buffer.read(), name=imagem.name)

        return imagem_pronta
