class SolutionItem:

    # CONSTRUCTOR
    def __init__(self, id: int, name: str):
        self.__id = id
        self.__name = name
    
    
    # GETTERS
    def getId(self) -> int:
        return self.__id

    def getName(self) -> str:
        return self.__name