from s3fs import S3FileSystem
from pandas import read_csv
from pickle import dump as pickle_dump
from pickle import load as pickle_load
from psycopg2 import connect as psycopg2_connect
from csv import QUOTE_NONNUMERIC
from pyspark.sql.session import SparkSession
from pyspark.sql.dataframe import DataFrame as SparkDF
from .S3File import S3Files


class S3:
	def __init__(self, key=None, secret=None, iam_role=None, root='s3://', spark=None):
		"""
		starts an S3 connection
		:type key: str or NoneType
		:type secret: str or NoneType
		:type iam_role: str or NoneType
		:type root: str or NoneType
		:type spark: SparkSession or NoneType
		"""
		self._key = key
		self._secret = secret
		self._iam_role = iam_role
		if root is None:
			root = ''
		self._root = root
		self._spark = spark

		self.list = self.ls
		self.move = self.mv
		self.dir = self.ls
		self.copy = self.cp
		self.delete = self.rm

	@property
	def file_system(self):
		return S3FileSystem(key=self._key, secret=self._secret, use_ssl=False)

	def _get_absolute_path(self, path):
		if not path.startswith(self._root):
			path = self._root + path
		return path

	def ls(self, path, exclude_empty=False, detail=False, sort_by='path', sort_reverse=True, **kwargs):
		path = self._get_absolute_path(path)
		files = self.file_system.ls(path=path, detail=detail, **kwargs)

		# if the path is only a file ls will return itself.
		if len(files) == 1:
			if self._root + files[0] == path or files[0] == path:
				return []

		if exclude_empty:
			files = [file for file in files if self.get_size(file) > 0]
		if detail:
			files = S3Files(files)
			files.sort(by=sort_by, reverse=sort_reverse)
		else:
			if sort_by is not None:
				files.sort()
		return files

	def mv(self, path1, path2, recursive=True, max_depth=None, **kwargs):
		return self.file_system.mv(path1=path1, path2=path2, recursive=recursive, maxdepth=max_depth, **kwargs)

	def cp(self, path1, path2, recursive=True, on_error=None, **kwargs):
		return self.file_system.copy(path1=path1, path2=path2, recursive=recursive, on_error=on_error, **kwargs)

	def rm(self, path, recursive=True, **kwargs):
		path = self._get_absolute_path(path)
		return self.file_system.delete(path=path, recursive=recursive, **kwargs)

	def mkdir(self, path, **kwargs):
		path = self._get_absolute_path(path)
		return self.file_system.mkdir(path=path, **kwargs)

	def tree(self, path, depth_limit=None, indentation='\t'):
		def _get_tree(_path, _depth):
			subs = self.ls(_path)
			if _depth == 0:
				name = _path
			else:
				name = self.get_file_name_and_extension(_path)

			if len(subs) == 0:
				return f'{indentation * _depth}{name}'
			else:
				if depth_limit is None:
					return f'{indentation * _depth}{name}/\n' + '\n'.join(
						[_get_tree(_path=sub, _depth=_depth + 1) for sub in subs]
					)
				elif depth_limit > _depth:
					return f'{indentation * _depth}{name}/\n' + '\n'.join(
						[_get_tree(_path=sub, _depth=_depth + 1) for sub in subs]
					)
				else:
					return f'{indentation * _depth}{name}/\n{indentation * (_depth + 1)}...'
		print(_get_tree(_path=path, _depth=0))

	def exists(self, path):
		path = self._get_absolute_path(path)
		return self.file_system.exists(path=path)

	def write_bytes(self, path, bytes):
		path = self._get_absolute_path(path)
		with self.file_system.open(path=path, mode='wb') as f:
			f.write(bytes)

	def get_size(self, path):
		path = self._get_absolute_path(path)
		return self.file_system.size(path=path)

	def write_csv(self, data, path, index=False, encoding='utf-8', **kwargs):
		"""

		:type data: SparkDF
		:param path:
		:param index:
		:param kwargs:
		:return:
		"""
		path = self._get_absolute_path(path)
		bytes = data.to_csv(path_or_buf=None, quoting=QUOTE_NONNUMERIC, index=index, **kwargs).encode(encoding)
		self.write(path=path, bytes=bytes)

	def read_bytes(self, path):
		with self.file_system.open(path=self._root+path, mode='rb') as f:
			result = f.read()
		return result

	def read_csv(self, path, encoding='utf-8', **kwargs):
		path = self._get_absolute_path(path)
		with self.file_system.open(self._root+path, 'rb', ) as f:
			df = read_csv(f, encoding=encoding, **kwargs)
		return df

	def write_pickle(self, obj, path, mode='overwite'):
		"""

		:type obj: SparkDF
		:type path: str
		:type mode: str
		:rtype: bool
		"""
		path = self._get_absolute_path(path)
		if self.exists(path=path):
			if mode == 'overwrite':
				self.delete(path=path)
			else:
				raise FileExistsError(f'File "{path}" exists on S3!')

		with self.file_system.open(path=path, mode='wb') as f:
			try:
				return obj.to_pickle(f)
			except:
				if self.exists(path=path):
					self.delete(path=path)
				try:
					return pickle_dump(obj=obj, file=f)
				except Exception as e:
					if self.exists(path=path):
						self.delete(path=path)
					raise e

	def read_pickle(self, path):
		path = self._get_absolute_path(path)
		with self.file_system.open(path=path, mode='rb') as f:
			obj = pickle_load(file=f)
		return obj

	def copy_to_redshift(self, path, redshift, schema, table, truncate=False, create_table=False):
		path = self._get_absolute_path(path)
		if create_table:
			data = self.read_csv(path=path)
			redshift.create_table(data=data, name=table, schema=schema)

		connection = psycopg2_connect(f"""
			dbname='{redshift._database}' port='{redshift._port}' 
			user='{redshift._user_id}' password='{redshift._password}' 
			host='{redshift._server}'
		""")

		cursor = connection.cursor()

		if truncate:
			cursor.execute(f"TRUNCATE TABLE {schema}.{table}")

		if self._iam_role:
			credentials = f"IAM_ROLE '{self._iam_role}'"
		else:
			credentials = f"CREDENTIALS 'aws_access_key_id={self._key};aws_secret_access_key={self._secret}'"

		cursor.execute(f"""
			COPY {schema}.{table} FROM '{self._root+path}' 
			{credentials}
			FORMAT AS CSV ACCEPTINVCHARS EMPTYASNULL IGNOREHEADER 1;commit;
		""")

		connection.close()

	def write_parquet(self, data, path, mode='overwrite'):
		"""
		saves a Spark DataFrame to a path on S3 and returns the list of parquet files
		:type data: SparkDF
		:type path: str
		:type mode: str
		:rtype: list[str]
		"""
		path = self._get_absolute_path(path)

		if mode == 'overwrite' and self.exists(path=path):
			self.rm(path=path, recursive=True)

		data.write.mode(mode).save(path=path)
		return self.ls(path=path)

	@property
	def spark(self):
		"""
		:rtype: SparkSession
		"""
		if self._spark is None:
			return RuntimeError('S3 does not have access to a SparkSession')
		return self._spark

	@staticmethod
	def get_file_name_and_extension(path):
		"""
		returns a file name from a path
		:type path: str
		:rtype: str
		"""
		return path.strip('/').split('/')[-1]

	@classmethod
	def get_file_name(cls, path):
		"""
		returns a file name from a path
		:type path: str
		:rtype: str
		"""
		return cls.get_file_name_and_extension(path=path).split('.')[0]

	@classmethod
	def get_file_extension(cls, path):
		"""
		returns a file extension from a path
		:type path: str
		:rtype: str
		"""
		name_and_extension = cls.get_file_name_and_extension(path=path).split('.')
		if len(name_and_extension) > 1:
			return '.'.join(name_and_extension[1:])
		else:
			return None

	def is_file(self, path):
		return self.file_system.isfile(path=path)

	def is_dir(self, path):
		return self.file_system.isdir(path)

	@property
	def json(self):
		return self.file_system.to_json()

	def is_parquet_file(self, path):
		"""
		returns True if a path is a parquet file
		:type path: str
		:rtype: bool
		"""
		if self.get_size(path=path) == 0:
			return False
		else:
			n_and_e = self.get_file_name_and_extension(path=path).lower()
			return n_and_e.startswith('part-') and n_and_e.endswith('.parquet')

	def read_parquet(self, path, spark=None, parallel=True):
		"""
		reads parquet files inside a path and returns the data
		:type path: str
		:type spark: SparkSession or NoneType
		:type parallel: bool
		:rtype: SparkDF
		"""
		if spark is None:
			spark = self.spark

		files = self.ls(path=path, exclude_empty=True)
		if len(files) == 1:
			file = files[0]
			if self.get_size(file) > 0:
				if not self.is_parquet_file(path=file):
					print(f'"{file}" does not appear to be a parquet file!')
				return spark.read.load(file)
			else:
				raise FileNotFoundError(f'"{file}" is empty!')

		elif parallel:
			return spark.read.load(path=f'{path}/part-*.parquet')

		else:
			parquet_files = [file for file in files if self.is_parquet_file(path=file)]
			result = None
			for parquet in parquet_files:
				data = spark.read.load(self._get_absolute_path(parquet))
				if result is None:
					result = data
				else:
					result = result.union(data)

			return result

	load_parquet = read_parquet
	save_parquet = write_parquet
	load_pickle = read_pickle
	save_pickle = write_pickle

	def save(self, obj, path, mode='overwrite'):
		"""
		writes an object to path as a parquet if the object is a Spark DataFrame or a pickle otherwise
		:type obj: object
		:type path: str
		:type mode: str
		:rtype: bool
		"""
		if isinstance(obj, SparkDF):
			if path.endswith('.pickle'):
				raise ValueError(f'Spark DataFrame cannot be saved into a pickle file: "{path}"')

			if not path.endswith('.parquet'):
				path += '.parquet'

			return self.write_parquet(data=obj, path=path, mode=mode)

		else:
			if path.endswith('.parquet'):
				raise ValueError(f'{type(path)} cannot be saved into a parquet file: "{path}"')

			if not path.endswith('.pickle'):
				path += '.pickle'

			return self.write_pickle(obj=obj, path=path, mode=mode)

	def load(self, path, spark=None):
		"""
		reads an object from a path. If the extension is .parquet then the object is assumed to be a Spark DataFrame
		and the read_parquet method is used, otherwise a pickle will be read.
		:type path: str
		:type spark: SparkSession
		:rtype: bool
		"""
		if path.endswith('.parquet'):
			return self.read_parquet(path=path, spark=spark or self.spark)

		elif path.endswith('.pickle'):
			return self.read_pickle(path=path)

		else:
			raise NotImplementedError(f'load is not implemented for {path}!')
