class SentenceModel:
    def __init__(self) -> None:
        pass

    @staticmethod   
    def sentence_to_words(s: str) -> list:
        return s.split(" ")
