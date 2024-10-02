from flask import Flask, render_template, request, send_file
from supabase import create_client, Client
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

# Configurações do Supabase
SUPABASE_URL = "https://bnbeyejgjwhneesdnxbw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJuYmV5ZWpnandobmVlc2RueGJ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjczMDc2MDAsImV4cCI6MjA0Mjg4MzYwMH0.i7Y-TJlMMRAeGp7FHLQlRJ8Vvk5-YmGMzcL8TZIMYWk"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
def buscar_aniversariantes_casamento(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    response = supabase.table('aniversarios_casamento').select('*').gte('data_aniversario', start_date).lte('data_aniversario', end_date).execute()
    return response.data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        aniversariantes = buscar_aniversariantes(start_date, end_date)
        aniversariantes_casamentos = buscar_aniversariantes_casamento(start_date, end_date)
        if aniversariantes:
            image_path = gerar_imagem(aniversariantes, aniversariantes_casamentos)
            return send_file(image_path, mimetype='image/png')

    return render_template('index.html', aniversariantes=[])

def buscar_aniversariantes(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    response = supabase.table('membros').select('*').gte('data_aniversario', start_date).lte('data_aniversario', end_date).execute()
    return response.data
def buscar_aniversariantes_casamento(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    response = supabase.table('aniversarios_casamento').select('*').gte('data_aniversario', start_date).lte('data_aniversario', end_date).execute()
    return response.data
def gerar_imagem(aniversariantes, aniversariantes_casamentos):
    # Carregar a imagem padrão
    image = Image.open('static/padrao.png')
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()  # Você pode usar uma fonte específica se preferir

    # Adicionar texto dos aniversariantes
    y_position = 275  # Posição inicial do texto
    for membro in aniversariantes:
        font_geral = ImageFont.truetype('GlacialIndifference-Bold.otf', 40)
        nome = membro['nome']
        data_aniversario = membro['data_aniversario']
        data_aniversario = datetime.strptime(data_aniversario, "%Y-%m-%d")
        data_aniversario = data_aniversario.strftime('%d/%m')
        draw.text((157, y_position), f"{nome}", fill='black', font=font_geral)
        draw.text((800, y_position), f"{data_aniversario}", fill='black', font=font_geral)
        y_position += 55  # Espaço entre as linhas
    y_position = 900
    for membro in aniversariantes_casamentos:
        font_geral = ImageFont.truetype('GlacialIndifference-Bold.otf', 40)
        nome = membro['nome']
        data_aniversario = membro['data_aniversario']
        data_aniversario = datetime.strptime(data_aniversario, "%Y-%m-%d")
        data_aniversario = data_aniversario.strftime('%d/%m')
        draw.text((157, y_position), f"{nome}", fill='black', font=font_geral)
        draw.text((800, y_position), f"{data_aniversario}", fill='black', font=font_geral)
        y_position += 60  # Espaço entre as linhas

    # Salvar a nova imagem
    output_path = 'static/aniversariantes.png'
    image.save(output_path)

    return output_path

if __name__ == '__main__':
    app.run(debug=True)
