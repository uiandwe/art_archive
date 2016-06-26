__author__ = 'hyeonsj'
from controllers import DbController, artistController
dc = DbController.DbController()


class ArtistModel():

    class Artist():
        def __init__(self):
            self.id = 0
            self.name = ""
            self.birth_year = 0
            self.death_year = 0
            self.country = ""
            self.genre = ""

        def set(self, instance, column, value):
            setattr(instance, column, value)

        def to_dict(self, instance, filed_list):
            return_dict = dict()
            for filed in filed_list:
                return_dict[filed] = getattr(instance, filed)
            return return_dict

    def get(self, filed=None, artist_id=None):

        filed_list = []

        #특정 필드가 아니면 artist테이블의 모든 칼럼 이름을 가져와서 filed_list에 넣음
        if filed is None:
            filed = "*"
            sql = " SHOW COLUMNS FROM artists; "
            cur = dc.find(sql)

            for item in cur:
                filed_list.append(item[0])
        else:
            for item in filed.split(","):
                filed_list.append(item)

        sql = "SELECT "+filed+"  FROM artists "

        if artist_id is not None:
            sql += " where id = "+str(artist_id)

        cur = dc.find(sql)
        #에러일 경우 tuple 리턴
        if type(cur) is tuple:
            return cur

        return_instance_list = []
        for item in cur:
            #객체 생성 후 변수 삽입
            instance_artist = self.Artist()

            for idx, column in enumerate(filed_list):
                instance_artist.set(instance_artist, column, item[idx])

            return_instance_list.append(instance_artist)

        return return_instance_list, filed_list

    def delete(self, artist_id=None):

        delete_where = ""

        if artist_id:
            delete_where = "where id = "+str(artist_id)+" "

        sql = "delete from artists " + delete_where
        cur = dc.delete(sql)

        if type(cur) is tuple:
            return cur

        else:
            return True

    def insert(self, instance_artist):

        artist_dict = instance_artist.__dict__

        insert_columns = []
        insert_values = []
        columns = artist_dict.keys()
        for artist_columns in columns:
            if artist_columns is not "id":
                if artist_dict[artist_columns] is not None and artist_dict[artist_columns] != "":
                    insert_columns.append(artist_columns)
                    if type(artist_dict[artist_columns]) is str:
                        insert_values.append("'"+artist_dict[artist_columns]+"'")
                    else:
                        insert_values.append(str(artist_dict[artist_columns]))

        insert_columns = ",".join(insert_columns)
        insert_values = ",".join(insert_values)

        sql = "insert into artists("+insert_columns+") value("+insert_values+")"
        dc.insert(sql)

        sql = "SELECT LAST_INSERT_ID();"
        cur = dc.find(sql)

        return cur