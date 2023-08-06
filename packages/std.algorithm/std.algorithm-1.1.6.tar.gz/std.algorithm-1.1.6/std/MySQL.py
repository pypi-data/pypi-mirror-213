import mysql.connector, std, re, random, time, os

class Database:

    def create_database(self):
        cursor = self.cursor()
        try:
            cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.DB_NAME))
        except Exception as err:
            print("Failed creating database: {}".format(err))

    def __init__(self):
        user = os.environ.get('MYSQL_USER', 'prod')
        password = os.environ.get('MYSQL_PASSWORD', 'prod')
        host = os.environ.get('MYSQL_HOST', '127.0.0.1')
        database = os.environ.get('MYSQL_DATABASE', 'axiom')
        charset = os.environ.get('MYSQL_CHARSET', 'utf8')
        try:
            self.conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
        except mysql.connector.errors.ProgrammingError as err:
            print(err.msg)
            m = re.compile("Unknown database '(\w+)'").search(err.msg)
            assert m
            assert m[1] == database
            self.conn = mysql.connector.connect(user=user, password=password, host=host, database='mysql')
            self.execute("create database " + database)
            self.conn = mysql.connector.connect(user=user, password=password, host=host, database=database)

    def cursor(self, **kwargs):
        return self.conn.cursor(**kwargs)

    @property
    def wait_timeout(self):
        cursor = self.cursor()
        cursor.execute("show global variables like 'wait_timeout'")
        for Variable_name, Value in cursor:
            assert Variable_name == 'wait_timeout'
            return Value

    @property
    def max_allowed_packet(self):
        cursor = self.cursor()
        cursor.execute("show global variables like 'max_allowed_packet'")
        for Variable_name, Value in cursor:
            assert Variable_name == 'max_allowed_packet'
            return Value

    def commit(self):
        self.conn.commit()

    def query(self, sql, order=None, limit=None, offset=0, dictionary=False):
        if order:
            sql += f" order by {order}"
            
        if limit:
            sql += ' limit %s' % limit
            
        if offset:
            sql += ' offset %s' % offset

        cursor = self.cursor(dictionary=dictionary)
        cursor.execute(sql)
        yield from cursor

    def execute(self, sql, *args):
        cursor = self.cursor()
        cursor.execute(sql, *args)
        self.commit()
        return cursor.rowcount

    def executemany(self, sql, seq_params, batch_size=1024, verbose=True):
        # seq_params must be a list of tuple
        cursor = self.cursor()
        
        if batch_size:
            batches = std.batches(seq_params, batch_size)
            if verbose and len(batches) == 1:
                verbose = False
                         
            rowcount = 0
            for i, seq_params in enumerate(batches):
                if verbose:
                    print("executing instances from", i * batch_size, 'to', (i + 1) * batch_size, "(excluded)")
                cursor.executemany(sql, seq_params)
                rowcount += cursor.rowcount
        else:
            cursor.executemany(sql, seq_params)
            rowcount = cursor.rowcount
            
        self.commit()
        return rowcount

    def show_create_table(self, table):
        for _, sql in self.query("show create table %s" % table):
            return sql

    def show_tables(self):
        tables = [table for table, *_ in self.query("show tables")]
#         tables.sort()
        return tables

    def show_create_table_oracle(self, table):
        for _, sql in self.query("select table_name, dbms_metadata.get_ddl('TABLE','%s') from dual,user_tables where table_name='%s'" % (table, table)):
            return sql

    def desc_oracle(self, table):
        return [args for args in self.query("select column_name,data_type,nullable from all_tab_columns where owner='%s' and table_name='%s'" % (self.conn._con._kwargs['user'], table))]

    def desc_table(self, table):
        return [*self.query("desc %s" % table)]


class MySQLConnector(Database):

    def __init__(self):
        Database.__init__(self)
        
    def load_data_from_list(self, table, array, step=10000, replace=False, ignore=False, truncate=False):
        desc = self.desc_table(table)
        
        has_training_field = False
        
        char_length = [256] * len(desc)
        dtype = [None] * len(desc)
        for i, (Field, Type, *_) in enumerate(desc):
            dtype[i] = Type
            
            Type = str(Type, encoding="utf-8")  
            if Field == 'training':
                has_training_field = True
                
            if Type in ('text', 'json'):
                char_length[i] = 65535
                continue
            
            elif Type == 'mediumblob':
                char_length[i] = 16 * 1024 * 1024 - 1
                continue
            
            m = re.compile("varchar\((\d+)\)").match(Type)
            if m:
                char_length[i] = int(m[1])           
                
        def create_csv(lines, step):
            import tempfile
            folder = tempfile.gettempdir()
                
            for i in range(0, len(lines), step):
                csv = folder + '/%s-%d.csv' % (table, i)
                with open(csv, 'w', encoding='utf8') as file:
                    for args in lines[i:i + step]: 
                        if isinstance(args, tuple):
                            args = [*args]
                            
                        for i, arg in enumerate(args):
                            if isinstance(arg, set):
                                arg = [*arg]
                                                            
                            if isinstance(arg, (list, tuple)):
                                arg = std.json_encode(arg)
                                arg = std.json_encode(arg)[1:-1]
                            elif isinstance(arg, str): 
                                arg = std.json_encode(arg)[1:-1]
                            elif isinstance(arg, bytes):
                                if len(arg) > char_length[i]:
                                    print(args)
                                    print('args[%d] exceeds the allowable length %d' % (i, char_length[i]))
                                    arg = arg[:char_length[i]]
                                    
                                arg = arg.decode()                                
                            else:
                                arg = str(arg)
                            
                            if not ignore and (len(arg.encode(encoding='utf8')) if dtype[i] == 'text' else len(arg)) > char_length[i]:
                                if truncate:
                                    print('truncating the data to maximum length:', char_length[i], ", since its length is", len(arg.encode(encoding='utf8')))
                                    arg = arg[:char_length[i]]
                                else:
                                    print(args)
                                    print('args[%d] exceeds the allowable length %d' % (i, char_length[i]))
                                    args = None
                                    break
                            args[i] = arg
                        
                        if args:
                            if has_training_field and len(args) < len(desc):
                                args.append(str(random.randint(0, 1)))               
                            print('\t'.join(args), file=file)
                            
                std.eol_convert(csv)
                yield csv
                
        for csv in create_csv(array, step):
            self.load_data_from_csv(table, csv, delete=True, replace=replace, ignore=ignore)

    def load_data(self, table, data, **kwargs):
        if isinstance(data, str):
            self.load_data_from_csv(table, data, **kwargs)
        else:
            self.load_data_from_list(table, data, **kwargs)
            
    def load_data_from_csv(self, table, csv, delete=False, replace=False, ignore=False):
        start = time.time()
        csv = csv.replace('\\', '/')        
        if replace:
            sql = 'load data local infile "%s" replace into table %s character set utf8' % (csv, table)
        elif ignore:
            sql = 'load data local infile "%s" ignore into table %s character set utf8' % (csv, table)
        else: 
            sql = 'load data local infile "%s" into table %s character set utf8' % (csv, table)
        print('executing: ', sql)
        
        local_infile = True
        for Variable_name, Value in self.query("show global variables like 'local_infile'"):
            assert Variable_name == 'local_infile'
            if Value == 'OFF':
                local_infile = False
                
        if not local_infile:
            self.execute('set global local_infile = 1')
            
# in my.ini:            
# [mysql]
# local-infile=1
# 
# [mysqld]
# local-infile=1
            
        try:
            self.execute(sql)
        except Exception as e:
            print(e)
            return
            
        print('time cost =', (time.time() - start))
        if delete:
            print("os.remove(csv)", csv)
            try:
                os.remove(csv)
            except:
                exit()

    def read_from_excel(self):
        from xlrd import open_workbook
        for table in ['ecchatfaqcorpus', 'ecchatrecords', 'ecchatreportunknownquestion', 'eccommonstored', 'eccompany', 'ecoperatorbasicsettings', 'ecchatreportupdate']:
            desc = self.show_create_table_not_connected('ucc.%s' % table)
            print(desc)
            fields = []
            for field in desc.split('\n')[1:]:
                field = field.strip()
                if field.startswith('`'):
                    fields.append(field)
            print(fields)
    
            workbook = open_workbook(utility.workingDirectory + 'mysql/ucc_tables/%s.xlsx' % table)
    
            sheet = workbook.sheet_by_index(0)
    
    #         assert len(fields) == sheet.ncols
    
            datetime_index = []
            for j in range(sheet.ncols):
                if re.compile('DEFAULT NULL').search(fields[j]):
                    datetime_index.append(j)
            sql = 'insert into ucc.%s values (%s)' % (table, ','.join(['%s'] * len(fields)))
            print(sql)
    
            for i in range(sheet.nrows):
                array = sheet.row_values(i)
                for j in range(sheet.ncols):
                    if isinstance(array[j], str):
                        m = re.compile(r'(\d+)/(\d+)/(\d+) (\d+:\d+:\d+)').fullmatch(array[j])
                        if m:
                            groups = m.groups()
                            array[j] = '%s-%s-%s %s' % (groups[2], groups[0], groups[1], groups[3])
                print(array)
                for j in datetime_index:
                    if not array[j]:
                        array[j] = None
    
                if sheet.ncols < len(fields):
                    array += [None] * (len(fields) - sheet.ncols)
                self.execute(sql, array)

    def select(self, *args, **kwargs):
        if isinstance(args[0], (list, tuple)):
            fields, *args = args
            assert fields
            star = ', '.join(fields)
        else:
            star = '*'
            
        if args:
            table, *args = args
        else:
            table = kwargs.pop('table')

        sql = f"select {star} from {table} "
        
        fetch_size = kwargs.pop('fetch_size', None)
        limit = kwargs.pop('limit', None)
        if fetch_size:
            assert limit, "limit must be set if fetch_size is set"
        
        where = kwargs.pop('where', None)
        offset = kwargs.pop('offset', None)
        order = kwargs.pop('order', None)
        dictionary = kwargs.pop('dictionary', None)
        conditions = []
        for field, value in kwargs.items():
            if isinstance(value, (tuple, list, set)):
                conditions.append(f"{field} in (%)" % ', '.join(str(t) for t in value))
            else:
                if isinstance(value, str):
                    value = std.json_encode(value)
                conditions.append(f"{field} = %s" % value)
          
        if where:
            conditions.append(where)
            
        if conditions:
            sql += 'where ' + ' and '.join(conditions)
            
        print('sql =', sql)
        
        if fetch_size and limit > fetch_size:
            if offset is None:
                offset = 0

            for off in range(0, limit, fetch_size):
                print('offset =', off + offset)
                [*data] = self.query(sql, order=order, limit=fetch_size, offset=off + offset, dictionary=dictionary)
                yield from data
                
        else:
            yield from self.query(sql, order=order, limit=limit, offset=offset, dictionary=dictionary)

    def __call__(self):
#         import mysql.connector.pooling
#          
#         config = {
#           "user": "yourusername",
#           "password": "yourpassword",
#           "host": "yourhost",
#           "database": "yourdatabase"
#         }
#          
#         cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=20, **config)
#          
#         cnx = cnxpool.get_connection()
#          
#         cursor = cnx.cursor()
#         cursor.execute("SELECT * FROM mytable")
#          
#         cursor.close()
#         cnx.close()        
        return MySQLConnector()

instance = MySQLConnector()


def is_number(Type):
    return re.match('tinyint\(\d+\)|double', Type)


def is_int(Type):
    return re.search('int\(\d+\)', Type)


def is_float(Type):
    return re.match('double', Type)


def is_string(Type):
    return re.match('varchar\(\d+\)', Type)


def is_enum(Type):
    return re.match('enum\((\S+)\)', Type)
    
def quote(s):
    return s.replace("'", "''").replace("\\", r"\\")


def mysqlRepresentation(Type, value):
    if is_number(Type.decode()):
        ... 
    else:
        value = std.json_encode(value)
        
    return value

if __name__ == '__main__':
    ...

#ln -s /usr/local/mysql/mysql.sock /tmp/mysql.sock
#mysql -uuser -puser -Daxiom