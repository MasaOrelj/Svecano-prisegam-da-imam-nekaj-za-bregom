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
class StudentDTO:
    id: int = field(default=0)
    name: str = field(default="")
    username: str = field(default="")
    password: str = field(default="")
    patronus: str = field(default="")
    house_name: str = field(default="")


@dataclass
class Professor:
    id: int = field(default=0)
    name: str = field(default="")
    house_id: str = field(default="")


@dataclass
class Subject:
    id: int = field(default=0)
    name: str = field(default="")
    professor_id: int = field(default=0)



@dataclass
class SubjectDTO:
    id: int = field(default=0)
    name: str = field(default="")
    professor_id: int = field(default=0)
    professor_name: str = field(default="")


@dataclass
class Comment:
    id: int = field(default=0)
    text: str = field(default="")
    student_id: int = field(default=0)
    post_id: int = field(default=0)



@dataclass
class CommentDTO:
    id: int = field(default=0)
    text: str = field(default="")
    student_name: str = field(default="")
    post_id: int = field(default=0)
    post_text: str = field(default="")


@dataclass
class Post:
    id: int = field(default=0)
    text: str = field(default="")
    likes: int =  field(default=0)
    student_id: int = field(default=0)
    forum_id: int = field(default=0)




@dataclass
class PostDTO:
    id: int = field(default=0)
    text: str = field(default="")
    likes: int =  field(default=0)
    student_id: int = field(default=0)
    student_name: str = field(default="")
    forum_id: int = field(default=0)
    forum_name: str = field(default="")


@dataclass
class Forum:
    id: int = field(default=0)
    name: str = field(default="")