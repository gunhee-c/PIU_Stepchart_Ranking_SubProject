def correct_anomalies_html(text):
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '"')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&nbsp;', ' ')
    return text

#URL 파싱 과정에서의 anomalie들 정리: 특정 노래들에 대해서 정리
def correct_anomalies_custom(text):
    #print("보이루")
    text = text.replace("feat.  KuTiNA", "feat. KuTiNA")
    if "팔랑크스" in text:
        #print("팔랑크스 발견")
        return "팔랑크스 RS2018 edit"
    if "Phalanx" in text:
        return "Phalanx RS2018 edit"
    return text

def hello():
    return "hello" 

def get_song_name_official(song_name, song_name_official):
    if song_name in song_name_official:
        return song_name_official[song_name]
    else:
        return song_name