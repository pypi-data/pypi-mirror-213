from pydantic import BaseModel
from typing import List,Optional
from . import utilities

class Color(BaseModel):
    hex: Optional[str]
    rgba: Optional[tuple]

class ElementV2(BaseModel):
    id: Optional[str]
    name: Optional[str]
    color: Optional[str]
    icon: Optional[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"
        self.color = Color(hex = self.color, rgba = utilities.hex_to_rgba(self.color))

class SkillV2(BaseModel):
    id: Optional[str]
    name: Optional[str]
    level: Optional[int]
    max_level: Optional[int]
    element: Optional[ElementV2]
    type: Optional[str]
    type_text: Optional[str]
    effect: Optional[str]
    effect_text: Optional[str]
    simple_desc: Optional[str]
    desc: Optional[str]
    icon: Optional[str]

class PathV2(BaseModel):
    id: Optional[str]
    name: Optional[str]
    icon: Optional[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"

class AttributeV2(BaseModel):
    field: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    value: Optional[float]
    display: Optional[str]
    percent: Optional[bool]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"

class PropertyV2(BaseModel):
    type: Optional[str]
    field: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    value: Optional[float]
    display: Optional[str]
    percent: Optional[bool]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"

class LightConeV2(BaseModel):
    id: Optional[str]
    name: Optional[str]
    rarity: Optional[int]
    rank: Optional[int]
    level: Optional[int]
    promotion: Optional[int]
    icon: Optional[str] = "icon/light_cone/24000.png"
    preview: Optional[str]
    portrait: Optional[str]
    path: Optional[PathV2] 
    attributes: Optional[List[AttributeV2]]
    properties: Optional[List[PropertyV2]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.portrait = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.portrait}"
        self.preview = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.preview}"
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"

class AffixV2(BaseModel):
    type: Optional[str]
    field: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    value: Optional[float]
    display: Optional[str]
    percent: Optional[bool]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"

class RelicV2(BaseModel):
    id: Optional[str]
    name: Optional[str]
    set_id: Optional[str]
    set_name: Optional[str]
    rarity: Optional[int]
    level: Optional[int]
    icon: Optional[str]
    main_affix: Optional[AffixV2]
    sub_affix: Optional[List[AffixV2]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"

class PropertyV2(BaseModel):
    type: Optional[str]
    field: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    value: Optional[float]
    display: Optional[str]
    percent: Optional[bool]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"

class RelicSetV2(BaseModel):
    id: str
    name: str
    desc: str
    properties: Optional[List[PropertyV2]]


class Addition(BaseModel):
    field: str
    name: str
    icon: str
    value: float
    display: str
    percent: bool

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"

class CharacterData(BaseModel):
    id: Optional[str]
    name: Optional[str]
    rarity: Optional[int]
    rank: Optional[int]
    level: Optional[int]
    promotion: Optional[int]
    icon: Optional[str]
    preview: Optional[str]
    portrait: Optional[str]
    path: Optional[PathV2]
    element: Optional[ElementV2]
    skills: Optional[List[SkillV2]]
    light_cone: Optional[LightConeV2]
    relics: Optional[List[RelicV2]]
    relic_sets: Optional[List[RelicSetV2]]
    additions: Optional[List[Addition]]
    attributes: Optional[List[AttributeV2]]
    properties: Optional[List[PropertyV2]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = self.name.format(NICKNAME = "Trailblazer")
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"
        self.preview = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.preview}"
        self.portrait = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.portrait}"

    



#===================================
class Avatar(BaseModel):
    id: Optional[str]
    name: Optional[str]
    icon: Optional[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"

class SpaceInfo(BaseModel):
    pass_area_progress: Optional[int]
    light_cone_count: Optional[int]
    avatar_count: Optional[int]
    achievement_count: Optional[int]


class PlayerV2(BaseModel):
    uid: Optional[str]
    nickname: Optional[str]
    level: Optional[int]
    avatar: Optional[Avatar]
    signature: Optional[str]
    friend_count: Optional[int]
    world_level: Optional[int]
    birthday: Optional[str]
    space_info: Optional[SpaceInfo]


class Player(BaseModel):
    uid: str
    name: str
    level: int
    icon: str
    signature: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"




class RankIcon(BaseModel):
    icon: str
    unlock: bool

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"

class Skill(BaseModel):
    name: str
    level: int
    type: str
    icon: str
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"

class MainProperty(BaseModel):
    name: str
    value: str
    icon: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"

class SubProperty(BaseModel):
    name: str
    value: str
    icon: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"

class Relic(BaseModel):
    name: str
    rarity: int
    level: int
    main_property: MainProperty
    sub_property: List[SubProperty]
    icon: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"

class RelicSet(BaseModel):
    name: str
    icon: str
    desc: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"

class Property(BaseModel):
    name: str
    base: str
    addition: Optional[str]
    icon: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"

class PatchInfo(BaseModel):
    name: Optional[str]
    url: Optional[str]

class LightConeInfo(BaseModel):
    atk: Optional[int]
    hp: Optional[int]
    defense: Optional[int]
    patch: Optional[PatchInfo]

class LightCone(BaseModel):
    id: Optional[int]
    name: Optional[str]
    rarity: Optional[int]
    rank: Optional[int]
    level: Optional[int]
    icon: Optional[str] = "icon/light_cone/24000.png"
    portrait: Optional[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = self.icon.split('/')[2][:-4]
        portrait = self.icon.replace("icon/light_cone/", "image/light_cone_portrait/")
        self.portrait = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{portrait}"
        self.icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.icon}"
        

class Character(BaseModel):
    id: Optional[str]
    name: Optional[str]
    rarity: Optional[int]
    level: Optional[int]
    rank: Optional[int]
    rank_text: Optional[str]
    rank_icons: List[RankIcon]
    preview: Optional[str]
    portrait: Optional[str]
    path: Optional[str]
    path_icon: Optional[str]
    element: Optional[str]
    element_icon: Optional[str]
    color: Optional[str]
    skill: List[Skill]
    light_cone: Optional[LightCone]
    relic: dict[str, Relic]
    relic_set: List[RelicSet]
    property: List[Property]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = self.name.format(NICKNAME = "Trailblazer")
        self.element_icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.element_icon}"
        self.path_icon = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.path_icon}"
        self.preview = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.preview}"
        self.portrait = f"https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{self.portrait}"


class StarRailApiDataV2(BaseModel):
    player: PlayerV2
    characters: List[CharacterData]

class StarRailApiData(BaseModel):
    player: Player
    characters: List[Character]

class PlayerSpaceInfo(BaseModel):
    PassAreaProgress: Optional[int]
    LightConeCount: Optional[int]
    AvatarCount: Optional[int]
    AchievementCount: Optional[int]


class PlayerDetailInfo(BaseModel):
    UID: int
    CurFriendCount: Optional[int]
    WorldLevel: Optional[int]
    Signature: Optional[str]
    NickName: Optional[str]
    Birthday: Optional[int]
    Level: Optional[int]
    PlayerSpaceInfo: Optional[PlayerSpaceInfo]


class PlayerInfo(BaseModel):
    PlayerDetailInfo: PlayerDetailInfo
  

