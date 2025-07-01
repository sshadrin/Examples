from    typing      import Dict
from    pydantic    import BaseModel, Field

class GetPass(BaseModel):
    generate_pass: Dict[str, str] = Field(...)

class GetPassParam(BaseModel):
    length   : int = Field(...)
    low_str  : bool = Field(False)
    hight_str: bool = Field(False)
    symbol   : bool = Field(False)
    number   : bool = Field(False)
