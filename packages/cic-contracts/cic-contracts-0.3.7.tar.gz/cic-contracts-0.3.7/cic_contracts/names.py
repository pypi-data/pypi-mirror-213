# standard imports
import enum

class Name(enum.Enum):
    WRITER = "Writer"
    EXPIRE = "Expire"
    SEAL = "Seal"
    CAPPED = "Capped"
    MINTER = "Minter"
    BURNER = "Burner"
