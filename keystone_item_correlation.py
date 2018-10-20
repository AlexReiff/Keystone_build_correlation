from lxml import html
import requests
import operator

def parse_champion_role(champion, role):
    #print(champion + " " +  role)
    resp = requests.get('http://www.op.gg/champion/' + champion + '/statistics/' + role)
    tree = html.fromstring(resp.content)
    rec_builds_table = tree.xpath('//table[@class="champion-overview__table"]')

    runes = tree.xpath('//img[@class="champion-stats-summary-rune__image champion-stats-summary-rune__image--keystone"]')
    rune = runes[0].attrib['src']
    
    rec_builds = tree.xpath('//tr[@class="champion-overview__row champion-overview__row--first"]')
    #start_builds = rec_builds[0]
    core_builds = rec_builds[1]
    #boot_choices = rec_builds[2]

    play_count = int(core_builds[2][1].text.replace(',', ''))
    first_item = core_builds[1][0][0][0].attrib['src']
    second_item = core_builds[1][0][2][0].attrib['src']
    third_item = core_builds[1][0][4][0].attrib['src']
    
    return [rune, {first_item: play_count, second_item: play_count, third_item: play_count}]

def output_to_file(rune_dict):
    txt_file = open("rune_item_correlation.txt", "w")
    for rune in rune_dict:
        txt_file.write("![](http:" + rune.split('?')[0] + ") ")
        sorted_items = []
        for key, value in sorted(runes[rune].items(), key=operator.itemgetter(1)):
            sorted_items.append(key)
        txt_file.write("![](http:" + sorted_items[-1].split('?')[0] + ") ")
        txt_file.write("![](http:" + sorted_items[-2].split('?')[0] + ") ")
        txt_file.write("![](http:" + sorted_items[-3].split('?')[0] + ")")
        txt_file.write("\n\n")
    txt_file.close() 

def main_loop(champ_names):
    runes = {}
    #print("start")
    for champ in champ_names:#['alistar', 'annie', 'sejuani']:
        for role in ['top']:#, 'jungle', 'mid', 'bot', 'support']:
            #print(champ + " " +  role)
            results = parse_champion_role(champ, "")
            rune = results[0]
            items = results[1]
            if rune in runes:
                for item in items.keys():
                    if item in runes[rune]:
                        runes[rune][item] += items[item]
                    else:
                        runes[rune][item] = items[item]
            else:
                runes[rune] = items
    return runes            

if __name__ == '__main__':
    resp = requests.get('http://www.op.gg/champion/statistics')
    tree = html.fromstring(resp.content)
    champ_names = tree.xpath('//div[@class="champion-index__champion-item__name"]/text()')
    #print(champ_names)
    runes = main_loop(champ_names)
    output_to_file(runes)

"""
PtA 8005
Lethal Tempo 8008
Fleet Footwork 8021
Conq 8010
Electrocute 8112
Predator 8124
Dark Harvest 8128
Hail of Blades ??
Aery 8214
Comet 8229
Phase Rush 8230
Grasp 8437
Aftershock 8439
Guardian 8465
Glacial 8351
Klepto 8359
Spellbook 8360
"""    