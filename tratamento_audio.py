import os
from pydub import AudioSegment

PASTA_ORIGEM = './web/audio_especies'
PASTA_DESTINO = './web/audio_final'  # Nova pasta para os áudios prontos

# Metas de tempo (em milissegundos)
TEMPO_MINIMO = 5000  # 5 segundos
TEMPO_MAXIMO = 8000  # 8 segundos (teto sugerido)
CROSSFADE = 150      # 150ms de fusão suave (evita estalos)

# Criar pasta de destino se não existir
if not os.path.exists(PASTA_DESTINO):
    os.makedirs(PASTA_DESTINO)

print(f"--- Iniciando Processamento ---")
print(f"Origem: {PASTA_ORIGEM}")
print(f"Destino: {PASTA_DESTINO}")

arquivos = [f for f in os.listdir(PASTA_ORIGEM) if f.endswith('.mp3') or f.endswith('.wav')]

for arquivo in arquivos:
    caminho_origem = os.path.join(PASTA_ORIGEM, arquivo)
    caminho_destino = os.path.join(PASTA_DESTINO, arquivo)

    try:
        audio = AudioSegment.from_file(caminho_origem)
        audio_original = audio # Guarda uma cópia para colar
        duracao_atual = len(audio)

        if duracao_atual < TEMPO_MINIMO:
            print(f"🔄 Processando: {arquivo} ({duracao_atual/1000:.1f}s)")
            
            # Enquanto for menor que o tempo mínimo, adiciona mais uma repetição
            while len(audio) < TEMPO_MINIMO:
                # O crossfade faz o final de um se misturar com o começo do outro
                audio = audio.append(audio_original, crossfade=CROSSFADE)

            print(f"   -> Novo tempo: {len(audio)/1000:.1f}s")
            audio.export(caminho_destino, format="mp3")
            
        else:
            print(f"✅ Copiando: {arquivo} (Já tem {duracao_atual/1000:.1f}s)")
            audio.export(caminho_destino, format="mp3")

    except Exception as e:
        print(f"❌ Erro ao processar {arquivo}: {e}")

print("\n--- Concluído! ---")
print("Agora atualize seu JSON para apontar para a pasta 'audio_final'.")