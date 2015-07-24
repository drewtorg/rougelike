import libtcodpy as libtcod
import components as Components
import object
import json

class Decoder:
    def __init__(self, path):
        self.path = path

    def decode(self, file):
        decodeFile = open(self.path + file)
        decodeString = decodeFile.read()
        return json.loads(decodeString, object_hook=self._decode_dict)

    def decode_monster_from_file(self, file, x, y):
        monsterDict = self.decode(file)

        fighter_component = Components.Fighter(hp=monsterDict['fighter']['hp'], dexterity=monsterDict['fighter']['dexterity'],
            accuracy=monsterDict['fighter']['accuracy'], power=monsterDict['fighter']['power'], xp=monsterDict['fighter']['xp'],
            death_function=Components.monster_death)

        ai_component = Components.WanderingMonster()

        monster = object.Object(x, y, monsterDict['char'], monsterDict['name'], libtcod.Color(monsterDict['r'],monsterDict['g'],monsterDict['b']),
            blocks=bool(monsterDict['blocks']), fighter=fighter_component, ai=ai_component)
        return monster

    def decode_spawn_chance(self, file):
        monsterDict = self.decode(file)
        return monsterDict['spawn_chance']

    def decode_item_from_file(self, file):
        return True

    def _decode_list(self, data):
        rv = []
        for item in data:
            if isinstance(item, unicode):
                item = item.encode('utf-8')
            elif isinstance(item, list):
                item = self._decode_list(item)
            elif isinstance(item, dict):
                item = self._decode_dict(item)
            rv.append(item)
        return rv

    def _decode_dict(self, data):
        rv = {}
        for key, value in data.iteritems():
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif isinstance(value, list):
                value = self._decode_list(value)
            elif isinstance(value, dict):
                value = self._decode_dict(value)
            rv[key] = value
        return rv