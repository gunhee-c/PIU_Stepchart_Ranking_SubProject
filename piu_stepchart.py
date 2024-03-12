
class PiuSeries:
    def __init__(self):
        self.name = ""
        self.versions = []

    def add_song_data(self, song_data):
        self.song_data_list.append(song_data)


class PiuSongDataList:
    def __init__(self):
        self.song_data_list = []
        self.version_list = []
        self.stepchart_list = []

    def build_from_CSV(self, csv):
        for i in range(len(csv)):
            #만약에 해당 노래가 없다면 
            song_data = PiuSongData()
            song_data.title = csv[i][0]
            song_data.composer = csv[i][1]
            song_data.title_en = csv[i][2]
            song_data.composer_en = csv[i][3]

            self.add_song_data(song_data)
        pass


    def add_song_data(self, song_data):
        self.song_data_list.append(song_data)

    def add_versions(self, version):
        self.version_list.append(version)


class PiuSongData:
    def __init__(self):
        self.title = ""
        self.composer = ""
        self.title_en = ""
        self.composer_en = ""
        self.bpm = ""
        self.category = ""
        self.gametype = ""

        self.stepchartinfo_list = []

        pass



class StepChartData:
    def __init__(self):
        self.level = ""
        self.level_history = []
        pass