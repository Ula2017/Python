from miditime.miditime import MIDITime
from ArgumentParser import ArgumentParser
import json
import urllib.request
from datetime import datetime
import random


def mag_to_pitch_tuned(mymidi, magnitude, option):
    if option == 0:
        scale_pct = mymidi.linear_scale_pct(49, 55, magnitude)
    elif option == 1:
        scale_pct = mymidi.linear_scale_pct(38000, 90000, magnitude)
    elif option == 2:
        scale_pct = mymidi.linear_scale_pct(320, 3300, magnitude)
    elif option == 3:
        scale_pct = mymidi.linear_scale_pct(38000, 90000, magnitude)
    elif option == 4:
        scale_pct = mymidi.linear_scale_pct(1, 9000, magnitude)
    else:
        scale_pct = mymidi.linear_scale_pct(1,1000, magnitude)

    c_major = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    note = mymidi.scale_to_note(scale_pct, c_major)
    midi_pitch = mymidi.note_to_midi_pitch(note)

    return midi_pitch


def main():

    parser = ArgumentParser()
    args = parser.get_parser()

    name = args.loc + '/' + args.file_name + '.mid'
    tempo = args.tempo
    octave = args.octave_range
    option = args.opt

    if option == 1 or option == 3:
        time = 0.2
    elif option == 2:
        time = 5
    elif option == 4:
        time = 1
    elif option == 5:
        time = 20
    else:
        if option != 0:
            print("Wrong option. Change to default.")
            option = 0
        time = 1

    if option == 0 or option == 4 or option == 5:
        r = urllib.request.urlopen('http://api.gios.gov.pl/pjp-api/rest/station/findAll').read()
        j = json.loads(r.decode('utf-8'))
    if option == 1 or option == 2 or option == 3:
        r = urllib.request.urlopen('https://www.reddit.com/r/all/top/.json')
        r = r.read()
        j = json.loads(r.decode('utf-8'))

    mymidi = MIDITime(tempo, name, time, octave, 1)
    beat_tmp =[]
    magniture =[]

    if option == 0:

        for i in range(0, 155):
            d = j[i]['dateStart'].split(' ')
            d[0] = d[0].split('-')
            d[1] = d[1].split(':')
            dt = datetime(int(d[0][0]), int(d[0][1]), int(d[0][2]), int(d[1][0]), int(d[1][1]), int(d[1][2]))
            beat_tmp.append(dt)
            magniture.append(float(j[i]['gegrLat']))

        beat_tmp_ = [mymidi.days_since_epoch(x) for x in beat_tmp]

    elif option == 4 or option == 5:

        id_tmp = []
        for i in range(0, 156):
            id_tmp.append(j[i]['id'])
        station = random.randint(0, 159)
        url_station = 'http://api.gios.gov.pl/pjp-api/rest/station/sensors/' + str(id_tmp[station])
        r3 = urllib.request.urlopen(url_station).read()
        j3 = json.loads(r3.decode('utf-8'))
        if option == 4:
            for i in j3:
                x = i['id']
                magniture.append(x)
                d = i['sensorDateStart'].split(' ')
                d[0] = d[0].split('-')
                d[1] = d[1].split(':')
                dt = datetime(int(d[0][0]), int(d[0][1]), int(d[0][2]), int(d[1][0]), int(d[1][1]), int(d[1][2]))
                beat_tmp.append(dt)

            beat_tmp = [mymidi.days_since_epoch(x) for x in beat_tmp]

        else:
            num = random.randint(0, len(j3) - 1)
            x = j3[num]['id']
            print(num)
            print(x)
            url_sensor = 'http://api.gios.gov.pl/pjp-api/rest/data/getData/' + str(x)
            r4 = urllib.request.urlopen(url_sensor).read()
            j4 = json.loads(r4.decode('utf-8'))
            print(j4)
            if not j4['values']:
                print("There is no data.")
                return
            for j in range(1, 58):
                da = j4['values'][j]['date'].split(' ')
                da[0] = da[0].split('-')
                da[1] = da[1].split(':')
                da5 = datetime(int(da[0][0]), int(da[0][1]), int(da[0][2]), int(da[1][0]), int(da[1][1]), int(da[1][2]))
                val = j4['values'][j]['value']
                print(type(val))
                if isinstance(val, float):
                    magniture.append(int(val))
                else:
                    magniture.append(33)

                beat_tmp.append(da5)
            beat_tmp = [mymidi.days_since_epoch(g) for g in beat_tmp]
    else:
        for i in range(0, 20):
            if option == 1:
                e = j['data']['children'][i]['data']['created']
                x = j['data']['children'][i]['data']['score']

            if option == 2:
                try:
                    e = j['data']['children'][i]['data']['preview']['images'][0]['source']['width']
                    x = j['data']['children'][i]['data']['preview']['images'][0]['source']['height']
                except KeyError:
                    print()
            if option == 3:
                e = j['data']['children'][i]['data']['created']
                x = j['data']['children'][i]['data']['ups']

            beat_tmp.append(e)
            magniture.append(x)

    beat = [mymidi.beat(x) for x in beat_tmp]
    start_time = beat[0]

    note_list = []
    i = 0
    for d in beat:
        note_list.append([d - start_time, mag_to_pitch_tuned(mymidi, magniture[i], option), 100, 1])
        i = i + 1

    mymidi.add_track(note_list)
    mymidi.save_midi()

if __name__ == '__main__':
    main()