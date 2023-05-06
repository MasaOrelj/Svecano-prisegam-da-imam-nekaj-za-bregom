from dataclasses import dataclass, field
#from dataclasses_json import dataclass_json

#@dataclass_json
@dataclass
class House:
    id: int = field(default=0)
    name: str = field(default="")


@dataclass
class Student:
    id: int = field(default=0)
    name: str = field(default="")
    username: str = field(default="")
    password: str = field(default="")
    patronus: str = field(default="")
    house_id: int = field(default=0)


@dataclass
class Professor:
    id: int = field(default=0)
    name: str = field(default="")
    house: str = field(default="")


@dataclass
class Subject:
    id: int = field(default=0)
    name: str = field(default="")
    professor_id: int = field(default=0)


@dataclass
class Comment:
    id: int = field(default=0)
    text: str = field(default="")
    student_id: int = field(default=0)
    post_id: int = field(default=0)


@dataclass
class Post:
    id: int = field(default=0)
    text: str = field(default="")
    likes: int =  field(default=0)
    student_id: int = field(default=0)
    forum_id: int = field(default=0)


@dataclass
class Forum:
    id: int = field(default=0)
    name: str = field(default="")