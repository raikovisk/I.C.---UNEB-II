import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
import matplotlib.pyplot as plt
from wordcloud import WordCloud

#arquivos  
print("Abrindo arquivos..\n")                                                                       
audio_mp3 = 'Vicios_e_Virtudes.mp3'
audio_wav = 'Vicios_e_Virtudes.wav'

# conversão de mp3 para wav
print("Convertendo Audio..\n")                                                           
sound = AudioSegment.from_mp3(audio_mp3)
sound.export(audio_wav, format='wav')

# selecionando audio
audio = AudioSegment.from_file(audio_wav, 'wav')
# Tamanho em milisegundos
tamanho = 30000
# divisão do audio em partes
partes = make_chunks (audio, tamanho) 
partes_audio =[]
for i, parte in enumerate(partes):
    # Enumerando arquivo particionado
    parte_name = 'Vicios{0}.wav'.format(i)
    # Guardando os nomes das partições em uma lista
    partes_audio.append(parte_name)
    # Exportando arquivos
    parte.export(parte_name, format='wav')
partes_audio

def transcreve_audio(nome_audio):
  # Selecione o audio para reconhecimento
  r = sr.Recognizer()
  with sr.AudioFile(nome_audio) as source:
    audio = r.record(source)  # leitura do arquivo de audio

  # Reconhecimento usando o Google Speech Recognition
  try:
    print('Google Speech Recognition: ' + r.recognize_google(audio,language='pt-BR'))
    texto = r.recognize_google(audio,language='pt-BR')
  except sr.UnknownValueError:
    print('Google Speech Recognition NÃO ENTENDEU o audio')
    texto = ''
  except sr.RequestError as e:
    print('Não foi possível solicitar resultados do serviço Google Speech Recognition; {0}'.format(e))
    texto = ''
  return texto

  # Aplicando a função de reconhecimento de voz em cada parte
texto = ''
for parte in partes_audio:
  texto = texto + ' ' + transcreve_audio(parte)

# criar uma lista de stop_words
stop_words = ['a','e','o','de','da','do','que']

# criar uma wordcloud
wc = WordCloud(stopwords=stop_words, background_color="black", width=1600, height=800)
wordcloud = wc.generate(texto)

# plotar wordcloud
fig, ax = plt.subplots(figsize=(12,8))
ax.imshow(wordcloud, interpolation='bilinear')
ax.set_axis_off()