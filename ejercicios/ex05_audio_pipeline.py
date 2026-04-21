"""
=============================================================================
Ejercicio 5: Pipeline de Audio - Polly + Transcribe (Python boto3)
Nivel: AUTONOMO
Duracion: ~20 minutos
=============================================================================

Objetivo: Construir un pipeline de audio completo que:

  1. Lea el titulo y texto de la primera noticia de data/noticias.json
  2. Use Amazon Polly (synthesize_speech) para generar un archivo MP3
     con la lectura del titulo
  3. Guarde el audio en data/output/noticia_audio.mp3
  4. (Bonus) Sube el MP3 a un bucket S3 y usa Amazon Transcribe
     (start_transcription_job) para transcribirlo de vuelta a texto

Servicios AWS:
  - Amazon Polly: Texto → Voz (TTS - Text to Speech)
  - Amazon Transcribe: Voz → Texto (STT - Speech to Text)

Parametros utiles de Polly:
  - VoiceId: 'Mia' (espanol mexicano), 'Lupe' (espanol US), 'Conchita' (espanol ES)
  - OutputFormat: 'mp3', 'ogg_vorbis', 'pcm'
  - Engine: 'neural' (mejor calidad) o 'standard'

Relacion con AIF-C01:
  - Task 1.2: Servicios de AI para procesamiento de voz
  - Polly y Transcribe son servicios complementarios (texto↔audio)
  - Concepto: pipeline de servicios AI encadenados

=============================================================================
"""

import boto3
import json
import os
from pathlib import Path

# Tu codigo aqui
polly_client = boto3.client('polly', region_name='us-east-1')
s3_client = boto3.client('s3', region_name='us-east-1')
transcribe_client = boto3.client('transcribe', region_name='us-east-1')


output_dir = Path('data/output')
output_dir.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# PASO 1: Leer la primera noticia de data/noticias.json
# ---------------------------------------------------------------------------
print("=" * 70)
print("PASO 1: Leyendo noticias...")
print("=" * 70)

with open('data/noticias.json', 'r', encoding='utf-8') as f:
    noticias = json.load(f)

primera_noticia = noticias[0]
titulo = primera_noticia['titulo']
texto = primera_noticia['texto']

print(f"📰 Título: {titulo}")
print(f"📝 Texto: {texto[:100]}...")
print()

# ---------------------------------------------------------------------------
# PASO 2: Usar Amazon Polly para generar audio del título
# ---------------------------------------------------------------------------
print("=" * 70)
print("PASO 2: Generando audio con Amazon Polly...")
print("=" * 70)

try:
    contenido_completo = f"{titulo}. {texto}"

    response = polly_client.synthesize_speech(
        Text=contenido_completo,
        OutputFormat='mp3',
        VoiceId='Mia',  # Voz en español mexicano
        Engine='neural'  # Mejor calidad
    )
    
    # Guardar el audio en archivo MP3
    audio_file = output_dir / 'noticia_audio.mp3'
    with open(audio_file, 'wb') as f:
        f.write(response['AudioStream'].read())
    
    print(f"✅ Audio generado exitosamente")
    print(f"📁 Guardado en: {audio_file}")
    print()
    
except Exception as e:
    print(f"❌ Error al generar audio con Polly: {e}")
    exit(1)

# ---------------------------------------------------------------------------
# PASO 3 (BONUS): Subir MP3 a S3 y transcribir con Amazon Transcribe
# ---------------------------------------------------------------------------
print("=" * 70)
print("PASO 3 (BONUS): Pipeline Transcribe...")
print("=" * 70)

# Nota: Requiere un bucket S3 existente
# Si tienes configurado un bucket, descomenta lo siguiente:

# BUCKET_NAME = 'tu-bucket-s3'  # Reemplaza con tu bucket
# S3_KEY = 'noticia_audio.mp3'

# try:
#     # Subir archivo a S3
#     s3_client.upload_file(
#         str(audio_file),
#         BUCKET_NAME,
#         S3_KEY
#     )
#     print(f" Archivo subido: s3://{BUCKET_NAME}/{S3_KEY}")
#     
#     # Iniciar trabajo de transcripción
#     print(f" Iniciando transcripción...")
#     transcribe_response = transcribe_client.start_transcription_job(
#         TranscriptionJobName='noticia-transcribe-job',
#         Media={'MediaFileUri': f's3://{BUCKET_NAME}/{S3_KEY}'},
#         MediaFormat='mp3',
#         LanguageCode='es-MX'  # Español mexicano
#     )
#     
#     job_name = transcribe_response['TranscriptionJob']['TranscriptionJobName']
#     print(f"✅ Trabajo de transcripción iniciado: {job_name}")
#     print(f"📊 Estado: {transcribe_response['TranscriptionJob']['TranscriptionJobStatus']}")
#     
# except Exception as e:
#     print(f"❌ Error en pipeline Transcribe: {e}")

print()
print("=" * 70)
print("✅ EJERCICIO 5 COMPLETADO")
print("=" * 70)
print()
print("Resumen:")
print(f"  - Título capturado: {titulo}")
print(f"  - Audio generado: {audio_file}")
print(f"  - Voz utilizada: Mia (español mexicano)")
print(f"  - Motor: Neural (mejor calidad)")
print()
print("Próximos pasos:")
print("  1. Reproduce el archivo: data/output/noticia_audio.mp3")
print("  2. Para activar Transcribe, configura un bucket S3 y descomenta el código BONUS")
print()