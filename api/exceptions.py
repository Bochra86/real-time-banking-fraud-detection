class DatabaseError(Exception):

    def __init__(self, message: str = "Database error"):
        self.message = message
        super().__init__(self.message)

        


