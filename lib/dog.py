import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    all=[]
    
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
     
    @classmethod
    def drop_table(cls):
        sql="""
            DROP TABLE IF EXISTS dogs
           
        """     
        CURSOR.execute(sql)

  
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.breed))

        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    # getting data from the db and converting it to objects in python
    
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id =row[0]
        return dog
    
    @classmethod
    def get_all(cls):
        sql ="SELECT * FROM dogs"
        
        all=CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(row) for row in all]
    
        # cls.all = [cls.new_from_db(row) for row in all]

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM dogs WHERE name = ?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None 

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM dogs
            WHERE id = ?
            LIMIT 1
        """
        result = CURSOR.execute(sql, (id,)).fetchone()
        if result:
            return cls.new_from_db(result)
        return None
    
    # @classmethod
    # def find_or_create_by(cls, name, breed):
    #     sql = """
    #     SELECT * FROM dogs
    #     WHERE name = ? AND breed = ?
    #     LIMIT 1
    # """
    # result = CURSOR.execute(sql, (name, breed)).fetchone()
    # if result:
    #     return cls.new_from_db(result)
    # else:
    #     sql = """
    #         INSERT INTO dogs (name, breed)
    #         VALUES (?, ?)
    #     """
    #     CURSOR.execute(sql, (name, breed))
    #     dog_id = CURSOR.lastrowid
    #     CONN.commit()
    #     return cls.find_by_id(dog_id)

    # def update(self, new_name):
    #     old_name = self.name
    #     sql = """
    #     UPDATE dogs
    #     SET name = ?
    #     WHERE name = ?
    # """
    #     CURSOR.execute(sql, (new_name, old_name))
    #     CONN.commit()
    #     self.name = new_name
