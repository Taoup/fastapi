from pydantic import AfterValidator, BaseModel
from typing import Annotated

def check_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id

ValidatedID = Annotated[str, AfterValidator(check_id)]

class Item(BaseModel):
    id: ValidatedID

def test(item_id: str):
    item = Item(id=item_id)
    return item.id

if __name__ == "__main__":
    print(test("isbn-1234567890"))
    print(test("imdb-1234567890"))
    print(test("invalid-1234567890"))  # 现在会抛出 ValueError


