import abc
import datetime
import inspect
import json
import pickle
import uuid
import warnings
from dataclasses import dataclass, field, fields, is_dataclass
from decimal import Decimal
from enum import Enum
from typing import Any, Generic, Iterable, TypeVar, Union

import boto3


class TableInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def delete(self):
        pass

    @abc.abstractmethod
    def scan(self):
        pass

    @abc.abstractmethod
    def delete_item(self, Key: dict):
        pass

    @abc.abstractmethod
    def get_item(self, Key: dict):
        pass

    @abc.abstractmethod
    def query(self, **kwargs):
        pass

    @abc.abstractmethod
    def put_item(self, Item: dict):
        pass


class BatchWriterInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def delete_item(self, Key: dict):
        pass


@dataclass
class SimulatedTable(TableInterface):
    items: dict = field(default_factory=lambda: {})
    table_status: str = "ACTIVE"
    # for items with no specified sk
    std_sk: str = field(default_factory=lambda: str(uuid.uuid1()))
    pk_name: str = "pk"
    sk_name: str = "sk"
    writer: BatchWriterInterface = None

    @dataclass
    class SimulateBatchWriter(BatchWriterInterface):
        table: TableInterface

        def __init__(self, table: TableInterface = None):
            self.table = table

        def delete_item(self, Key: dict):
            self.table.delete_item(Key)

        def put_item(self, Item: dict):
            self.table.put_item(Item)

        def close(self):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.close()

    def _inject_sk(self, Key: dict):
        if self.sk_name not in Key:
            Key[self.sk_name] = self.std_sk

    def _keys_from_item(self, item):
        Key = {}
        if self.pk_name not in item:
            raise KeyError(
                "The provide item must have a value for the partition key: ",
                self.pk_name,
            )
        Key[self.pk_name] = item[self.pk_name]
        if self.sk_name in item:
            Key[self.sk_name] = item[self.sk_name]
        else:
            self._inject_sk(Key)

        return Key

    def _expression_att_val2Key(self, ExpressionAttributeValues: dict):
        Key = {}
        for dirty_key in ExpressionAttributeValues:
            clean_key = dirty_key[1:-3]
            Key[clean_key] = ExpressionAttributeValues[dirty_key]
        return Key

    def batch_writer(self):
        if self.writer is None:
            self.writer = self.SimulateBatchWriter(table=self)
        return self.writer

    def delete(self):
        self.items = {}
        self.table_status = "DELETING"

    def _items_as_list(self):
        item_list = []
        for (
            _,
            partition,
        ) in self.items.items():  # The first ignored key is the partition key
            for _, item in partition.items():  # The second ignored key is the sort key
                item_list.append(item)
        return item_list

    def scan(self):
        scan_response = {
            "Count": len(self._items_as_list()),
            "Items": self._items_as_list(),
        }
        return scan_response

    def delete_item(self, Key: dict):
        aux = Key
        Key = aux.copy()
        self._inject_sk(Key)
        self.items[str(Key[self.pk_name])].pop(str(Key[self.sk_name]))

    def get_item(self, Key: dict):
        aux = Key
        Key = aux.copy()
        self._inject_sk(Key)
        try:
            return {"Item": self.items[str(Key[self.pk_name])][str(Key[self.sk_name])]}
        except Exception as ex:
            print(ex)
            return None

    def query(self, **kwargs):
        Key = self._expression_att_val2Key(kwargs["ExpressionAttributeValues"])
        response = {"Items": []}
        if self.sk_name in Key:  # One item
            item = self.get_item(Key)
            if item is not None:
                response["Items"].append(item)
        else:  # Multiple items
            for sk in self.items[str(Key[self.pk_name])]:
                response["Items"].append(self.items[str(Key[self.pk_name])][sk])
        return response

    def put_item(self, Item: dict):
        Key = self._keys_from_item(Item)
        if str(Key[self.pk_name]) not in self.items:
            self.items[str(Key[self.pk_name])] = {}
        self.items[str(Key[self.pk_name])][str(Key[self.sk_name])] = Item


class SimulatedDynamoDBResource:
    tables: dict = {}

    def create_table(self, **kwargs):
        table_name = kwargs["TableName"]
        key_schema = kwargs["KeySchema"]
        pk = None
        sk = None
        if table_name in self.tables:
            if self.tables[table_name].table_status != "DELETING":
                raise RuntimeError(
                    "A table with the name ", table_name, " already exists"
                )
            else:
                self.tables.pop(table_name)
        for key_schema_dict in key_schema:
            if key_schema_dict["KeyType"] == "HASH":
                pk = key_schema_dict["AttributeName"]

            elif key_schema_dict["KeyType"] == "RANGE":
                sk = key_schema_dict["AttributeName"]

        if pk is not None:
            if sk is not None:
                self.tables[table_name] = SimulatedTable(pk_name=pk, sk_name=sk)
            else:
                self.tables[table_name] = SimulatedTable(pk_name=pk)
            return self.tables[table_name]

        else:
            raise RuntimeError("Provided KeySchema missing the partition key")

    def Table(self, table_name: str):
        if (table_name is None) or (table_name not in self.tables):
            raise RuntimeError(
                "Provided table name does not correspond to a valid table"
            )
        return self.tables[table_name]


###### ---------- Global parameters ---------- ######


@dataclass
class DynamoDBGlobalParameters:
    """
    A singleton to define global parameters related to DynamoDB
    """

    _instance = None

    use_aws_cli_credentials: bool
    single_table: str
    endpoint_url: str
    region_name: str
    aws_access_key_id: str
    aws_secret_access_key: str
    read_capacity_units: int
    write_capacity_units: int

    @classmethod
    def get_instance(
        cls,
        use_aws_cli_credentials: bool = True,
        single_table: str = None,
        endpoint_url="http://localhost:8000",
        region_name: str = "dummy",
        aws_access_key_id: str = "dummy",
        aws_secret_access_key: str = "dummy",
        read_capacity_units: int = 5,
        write_capacity_units: int = 5,
    ):
        """
        Get an instance of the singleton
        """
        if cls._instance is None:
            cls._instance = cls(
                use_aws_cli_credentials,
                single_table,
                endpoint_url,
                region_name,
                aws_access_key_id,
                aws_secret_access_key,
                read_capacity_units,
                write_capacity_units,
            )
        return cls._instance

    @classmethod
    def is_instantiated(cls):
        return cls._instance is not None


###### ---------- Global parameters ---------- ######


###### ---------- Repository Interfaces and Implementation ---------- ######

T = TypeVar("T")  # A generic type var to hold Entity classes


class Repository(Generic[T], metaclass=abc.ABCMeta):
    """
    Just a simple "interface" inspired by the Java Spring Repository Interface
    """

    entity_type: T
    pass

    def check_provided_type(self):
        """Returns True if obj is a dynamo_entity class or an instance of a dynamo_entity class."""
        cls = T if isinstance(T, type) else type(T)
        return hasattr(cls, "_FIELDS")


class CrudRepository(Repository, metaclass=abc.ABCMeta):
    """
    Just a simple "interface" inspired by the Java Spring CrudRepository Interface
    """

    @abc.abstractmethod
    def count(self):
        """
        Counts the number of items in the table
        :return:
        """
        pass

    @abc.abstractmethod
    def remove(self, entity: T):
        pass

    @abc.abstractmethod
    def remove_all(self):
        pass

    @abc.abstractmethod
    def remove_by_keys(self, keys: dict):
        pass

    @abc.abstractmethod
    def remove_all_by_keys(self, keys: Iterable[dict]):
        pass

    @abc.abstractmethod
    def exists_by_keys(self, keys: dict):
        pass

    @abc.abstractmethod
    def find_all(self):
        pass

    @abc.abstractmethod
    def find_by_keys(self, keys_list: dict):
        pass

    @abc.abstractmethod
    def save(self, entity: T):
        pass

    @abc.abstractmethod
    def save_all(self, entities: Iterable[T]):
        pass


class DynamoCrudRepository(CrudRepository):

    ddb = None
    table = None
    table_name: str = None
    map_dict: map = None
    map_filled: bool = False
    print_debug: bool = False

    @staticmethod
    def ITEM2INSTANCE():
        return 1

    @staticmethod
    def INSTANCE2ITEM():
        return 0

    def if_debug_print(self, *args):
        if self.print_debug:
            print(args)

    def __init__(
        self,
        entity_type: T,
        print_debug: bool = False,
        use_mock_db: bool = False,
    ):
        self.entity_type = entity_type
        self.print_debug = print_debug

        self.map_dict = self.entity_type.dynamo_map()
        self._fill_map_dict(self.entity_type)

        global_values = DynamoDBGlobalParameters.get_instance()
        # For a single table design, define the table name as a global parameter,
        # if the table name is not set in the global parameters, will use the entity class table name
        if global_values.single_table is not None:
            self.table_name = global_values.single_table
        else:
            self.table_name = self.entity_type.dynamo_table_name()
        if use_mock_db:
            self.ddb = SimulatedDynamoDBResource()
            if (self.ddb.Table(self.table_name)) is None:
                self.create_table()  # The table does not exists in the mock dynamodb
        else:
            try:
                if not global_values.use_aws_cli_credentials:
                    # Set the db connection
                    self.ddb = boto3.resource(
                        "dynamodb",
                        endpoint_url=global_values.endpoint_url,
                        region_name=global_values.region_name,  # does not matter locally
                        aws_access_key_id=global_values.aws_access_key_id,  # does not matter locally
                        aws_secret_access_key=global_values.aws_secret_access_key,
                    )
                else:
                    self.ddb = boto3.resource("dynamodb")
            except Exception as ex:
                print(ex)
                raise ConnectionRefusedError("Not able to connect to DynamoDB")

        try:
            self.table = self.ddb.Table(self.table_name)
        except Exception as ex:
            print(ex)
            warning_str = (
                "Could not access table "
                + str(self.table_name)
                + " check if the table exists"
            )
            raise ResourceWarning(warning_str)

    def create_table(self):
        global_values = DynamoDBGlobalParameters.get_instance()
        attribute_definitions, key_schema = self._get_attribute_def_and_key_schema(
            self.entity_type
        )
        try:
            self.table = self.ddb.create_table(
                TableName=self.table_name,
                AttributeDefinitions=attribute_definitions,
                KeySchema=key_schema,
                ProvisionedThroughput={
                    "ReadCapacityUnits": global_values.read_capacity_units,
                    "WriteCapacityUnits": global_values.write_capacity_units,
                },
            )
        except Exception as ex:
            print(ex)
            raise ResourceWarning("Not able to create table", self.table_name)
        return self.table

    def count(self):
        try:
            scan_response = self.table.scan()
        except Exception as ex:
            print(ex)
            raise ResourceWarning("Not able to scan table", self.table_name)
        i = scan_response["Count"]
        while "LastEvaluatedKey" in scan_response:
            try:
                scan_response = self.table.scan(  # TableName='SingleTable',
                    ExclusiveStartKey=scan_response["LastEvaluatedKey"]
                )
            except Exception as ex:
                print(ex)
                warnings.warn("Not able to scan table" + str(self.table_name))
                return i
            i += scan_response["Count"]
        return i

    def remove_by_keys(self, keys: dict):
        try:
            self.table.delete_item(Key=keys)
        except Exception as ex:
            print(ex)
            warnings.warn(
                "Not able to delete item with keys"
                + str(keys)
                + "from table"
                + str(self.table_name)
            )

    def remove(self, to_delete: T):
        pk_name = self.entity_type.dynamo_pk()
        pk_value = getattr(to_delete, pk_name)
        keys = {pk_name: pk_value}

        if hasattr(self.entity_type, "dynamo_sk"):
            sk_name = self.entity_type.dynamo_sk()
            sk_value = getattr(to_delete, sk_name)
            keys[sk_name] = sk_value

        return self.remove_by_keys(keys)

    def item2instance(self, item):
        entity_instance = self.entity_type()
        for fl in fields(self.entity_type):
            if fl.name in item:
                if (
                    getattr(self.entity_type, "dynamo_custom_converter", False)
                    and fl.name in self.entity_type.dynamo_custom_converter()
                ):
                    setattr(
                        entity_instance,
                        fl.name,
                        self.entity_type.dynamo_custom_converter()[
                            self.ITEM2INSTANCE()
                        ](item[fl.name]),
                    )
                if issubclass(fl.type, (int, float, Decimal)):
                    setattr(entity_instance, fl.name, fl.type(str(item[fl.name])))
                elif issubclass(fl.type, (bytes, bool)):  # Perform a direct conversion
                    setattr(entity_instance, fl.name, fl.type(item[fl.name]))

                elif issubclass(fl.type, (dict, list)):  # json
                    setattr(entity_instance, fl.name, json.loads(item[fl.name]))

                elif issubclass(fl.type, Enum):  # Enum
                    setattr(entity_instance, fl.name, fl.type[item[fl.name]])

                elif issubclass(fl.type, str):
                    setattr(entity_instance, fl.name, str(item[fl.name]))

                # Use the iso format for storing datetime as strings
                elif issubclass(
                    fl.type, (datetime.date, datetime.time, datetime.datetime)
                ):
                    setattr(
                        entity_instance, fl.name, fl.type.fromisoformat(item[fl.name])
                    )

                elif issubclass(fl.type, object):  # objects in general are pickled
                    setattr(
                        entity_instance, fl.name, pickle.loads(bytes(item[fl.name]))
                    )

                else:  # No special case, use a simple str cast, probably will never be reached
                    setattr(entity_instance, fl.name, fl.type(item[fl.name]))

        return entity_instance

    def find_by_keys(self, keys: Union[dict, list]):
        """
        Finds objects stored in the database using the given keys
        :param keys: dict, list a set of keys to search for the object.
         If a list if provided, assumes the pattern [pk, sk]
        :return: an o object of the mapped class or a list of objects of the mapped class
        """
        if isinstance(keys, list):  # Produce dict from list
            key_list = keys
            keys = {}
            keys[self.entity_type.dynamo_pk()] = key_list[0]
            keys[self.entity_type.dynamo_sk()] = key_list[1]
        try:
            response = self.table.get_item(Key=keys)

            if "Item" in response:
                item = response[
                    "Item"
                ]  # item is a dict {table_att_name: table_att_value}
                return self.item2instance(item)
            else:
                return None
        except Exception:  # Check if the keys do not compose a unique key
            key_cond_exp, exp_att_val = self.keys2KeyConditionExpression(keys)
            response = {}
            try:
                response = self.table.query(
                    KeyConditionExpression=key_cond_exp,
                    ExpressionAttributeValues=exp_att_val,
                )
            except Exception:
                warnings.warn(
                    "Not able to query" + str(self.table) + "with keys" + str(keys)
                )
                return None
            if "Items" in response:
                entity_list = []
                items = response["Items"]
                for item in items:
                    entity_list.append(self.item2instance(item))

                while "LastEvaluatedKey" in response:
                    try:
                        response = self.table.query(
                            KeyConditionExpression=self.keys2KeyConditionExpression(
                                keys
                            ),
                            ExpressionAttributeValues=exp_att_val,
                            ExclusiveStartKey=response["LastEvaluatedKey"],
                        )
                    except Exception:
                        warnings.warn(
                            "Not able to query"
                            + str(self.table)
                            + "with keys"
                            + str(keys)
                        )
                        return entity_list if len(entity_list) > 0 else None
                        return None

                    if "Items" in response:
                        entity_list = []
                        items = response["Items"]
                        for item in items:
                            entity_list.append(self.item2instance(item))

                # If there is only one object, return the object, otherwise, return the list
                return entity_list if len(entity_list) != 1 else entity_list[0]
            return None

    def keys2KeyConditionExpression(self, keys: dict):
        buffer = ""
        exp_att_val = {}
        sortd = sorted(keys.keys())
        for key in sortd:
            buffer += str(key) + " = :" + str(key) + "val"
            if key != sortd[-1]:
                buffer += " AND "
            exp_att_val[":" + str(key) + "val"] = keys[key]
        return buffer, exp_att_val

    def find_all(self):
        entity_list = []

        try:
            scan_response = self.table.scan()
        except Exception as ex:
            print(ex)
            warnings.warn("Not able to scan table" + str(self.table_name))
            return None

        if "Items" in scan_response:
            items = scan_response["Items"]
            for item in items:
                entity_list.append(self.item2instance(item))
        else:
            return None

        while "LastEvaluatedKey" in scan_response:
            try:
                scan_response = self.table.scan(  # TableName='SingleTable',
                    ExclusiveStartKey=scan_response["LastEvaluatedKey"]
                )
            except Exception as ex:
                print(ex)
                warnings.warn("Not able to scan table" + str(self.table_name))
                return entity_list
            if "Items" in scan_response:
                items = scan_response["Items"]
                for item in items:
                    entity_list.append(self.item2instance(item))

        return entity_list

    def instance2item_params(self, obj: T):
        item_params = {}

        # Get every attribute of obj, ignoring private members and methods
        for attribute in inspect.getmembers(obj):
            if (
                (not attribute[0].startswith("_"))
                and (not inspect.ismethod(attribute[1]))
                and (not attribute[0] in obj.dynamo_ignore())
            ):
                if (
                    getattr(obj, "dynamo_custom_converter", False)
                    and attribute[0] in obj.dynamo_custom_converter()
                ):
                    item_params[attribute[0]] = obj.dynamo_custom_converter()[
                        self.INSTANCE2ITEM()
                    ](attribute[1])
                # switch self.map_dict[<attribute_name>]
                if self.map_dict[attribute[0]] == "N":  # case 'N' (number)
                    item_params[attribute[0]] = Decimal(
                        str(attribute[1])
                    )  # str cast to support numpy, pandas, etc

                elif self.map_dict[attribute[0]] == "B":  # case 'B' (bytes)
                    if isinstance(attribute[1], bytes):
                        item_params[attribute[0]] = bytes(attribute[1])
                    elif isinstance(
                        attribute[1], object
                    ):  # objects in general are pickled
                        item_params[attribute[0]] = pickle.dumps(attribute[1])
                    else:
                        raise TypeError(
                            "Only bytes and objects should be stored as bytes"
                        )
                elif self.map_dict[attribute[0]] == "BOOL":  # case 'BOOL' (boolean)
                    item_params[attribute[0]] = 1 if attribute[1] else 0
                else:  # default (string)
                    # Consider special cases and use specific string formats
                    # datetime
                    if isinstance(
                        attribute[1], (datetime.date, datetime.time, datetime.datetime)
                    ):
                        item_params[attribute[0]] = attribute[1].isoformat()

                    # enum
                    elif isinstance(attribute[1], Enum):
                        item_params[attribute[0]] = attribute[1].name

                    # maps and lists (converted to json)
                    elif isinstance(attribute[1], (dict, list)):
                        item_params[attribute[0]] = json.dumps(attribute[1])

                    # strings
                    elif isinstance(attribute[1], str):
                        item_params[attribute[0]] = str(attribute[1])
                    # No special case, use a simple str cast
                    else:
                        item_params[attribute[0]] = str(attribute[1])
        return item_params

    def save(self, obj: T):
        item_params = self.instance2item_params(obj)
        try:
            self.table.put_item(Item=item_params)
        except Exception as ex:
            print(ex)
            warnings.warn(
                "Not able to put item"
                + str(item_params)
                + "in table"
                + str(self.table_name)
            )

    def remove_all(self):
        pk = self.entity_type.dynamo_pk()
        sk = self.entity_type.dynamo_sk()
        entity_list = self.find_all()
        try:
            with self.table.batch_writer() as batch:
                for entity in entity_list:
                    batch.delete_item(
                        Key={
                            pk: entity.__getattribute__(pk),
                            sk: entity.__getattribute__(sk),
                        }
                    )
        except Exception as ex:
            print(ex)
            raise ResourceWarning(
                "Not able to remove all items from table", self.table_name
            )
        return True

    def remove_all_by_keys(self, keys_list: Iterable[dict]):
        try:
            with self.table.batch_writer() as batch:
                for keys in keys_list:
                    batch.delete_item(Key=keys)
        except Exception as ex:
            print(ex)
            raise ResourceWarning(
                "Not able to remove items with keys",
                keys_list,
                "from table",
                self.table_name,
            )

    def exists_by_keys(self, keys: Union[dict, list]):
        if isinstance(keys, list):  # Produce dict from list
            key_list = keys
            keys = {
                self.entity_type.dynamo_pk(): key_list[0],
                self.entity_type.dynamo_sk(): key_list[1],
            }
        try:
            response = self.table.get_item(Key=keys)
            if "Item" in response:
                return True
        except Exception as ex:  # Check if the keys do not compose a unique key
            print(ex)
            key_cond_exp, exp_att_val = self.keys2KeyConditionExpression(keys)
            try:
                response = self.table.query(
                    KeyConditionExpression=key_cond_exp,
                    ExpressionAttributeValues=exp_att_val,
                )
            except Exception:
                warnings.warn("Not able to query table" + str(self.table_name))
                return False
            if "Items" in response and len(response["Items"]) > 0:
                return True
        return False

    def save_all(self, entities: Iterable[T]):
        try:
            with self.table.batch_writer() as batch:
                for obj in entities:
                    item_params = self.instance2item_params(obj)
                    batch.put_item(Item=item_params)
        except Exception as err:
            print(err)
            raise ResourceWarning(
                "Not able to save item list", entities, "into table", self.table_name
            )

    def _fill_map_dict(self, cls):
        if not self.map_filled:
            fls = fields(cls)
            for fl in fls:
                attrib_type = str
                if (
                    fl.name not in self.map_dict
                ):  # Try to infer the type from the class  attribute type
                    # if using a specific library like numpy or pandas, the user should specify the "N" type himself
                    if issubclass(fl.type, (int, float, Decimal)):
                        attrib_type = "N"
                    elif issubclass(
                        fl.type,
                        (
                            str,
                            dict,
                            list,
                            datetime.date,
                            datetime.time,
                            datetime.datetime,
                            Enum,
                        ),
                    ):
                        attrib_type = "S"
                    elif issubclass(
                        fl.type, (bytes, object)
                    ):  # general objects will be pickled
                        attrib_type = "B"
                    elif issubclass(fl.type, bool):
                        attrib_type = "BOOL"
                    else:  # this will probably never be reached since general objects are converted to bytes
                        attrib_type = "S"

                    self.map_dict[fl.name] = attrib_type
            self.map_filled = True

    def _get_attribute_def_and_key_schema(self, cls):
        self._fill_map_dict(cls)

        attribute_definitions = []
        key_schema = []
        self.map_dict = cls.dynamo_map()

        cls_key_attribs = {cls.dynamo_pk(): "HASH"}
        if hasattr(cls, "dynamo_sk"):
            cls_key_attribs[cls.dynamo_sk()] = "RANGE"

        for fl in fields(cls):
            if fl.name in cls_key_attribs:
                # PK and GSI should come before SK and LSI
                if cls_key_attribs[fl.name] == "HASH":
                    attribute_definitions.insert(
                        0,
                        {
                            "AttributeName": "" + fl.name,
                            "AttributeType": "" + self.map_dict[fl.name],
                        },
                    )
                    key_schema.insert(
                        0,
                        {
                            "AttributeName": "" + fl.name,
                            "KeyType": cls_key_attribs[fl.name],
                        },
                    )
                else:
                    attribute_definitions.append(
                        {
                            "AttributeName": "" + fl.name,
                            "AttributeType": "" + self.map_dict[fl.name],
                        }
                    )
                    key_schema.append(
                        {
                            "AttributeName": "" + fl.name,
                            "KeyType": cls_key_attribs[fl.name],
                        }
                    )
        return attribute_definitions, key_schema


###### ---------- Repository Interfaces and Implementation ---------- ######


###### ---------- Wrapper fo mappable classes ---------- ######
def _wrap_class(
    pk: Any,
    cls=None,
    table_name: str = None,
    sk=None,
    mapping_schema: dict = None,
    ignore_attributes: list = None,
    custom_converter: dict = None,
):
    """
    Adds methods to the class
    """
    mapping_schema = mapping_schema if mapping_schema is not None else {}
    ignore_attributes = ignore_attributes if ignore_attributes is not None else []
    custom_converter = custom_converter if custom_converter is not None else {}
    table_name = table_name if table_name is not None else cls.__name__

    # The methods to be added to the class
    @classmethod
    def dynamo_table_name(cls):
        return table_name

    @classmethod
    def dynamo_pk(cls):
        return pk

    @classmethod
    def dynamo_sk(cls):
        return sk

    @classmethod
    def dynamo_map(cls):
        return mapping_schema

    @classmethod
    def dynamo_ignore(cls):
        return ignore_attributes

    @classmethod
    def dynamo_custom_converter(cls):
        return custom_converter

    # set the table name
    cls.dynamo_table_name = dynamo_table_name

    # set the partition key
    cls.dynamo_pk = dynamo_pk

    # set the sort key
    if sk is not None:
        cls.dynamo_sk = dynamo_sk

    # set the mapping of class attributes to table attributes
    cls.dynamo_map = dynamo_map

    # set the class attributes that will be ignored (not saved on the database)
    if ignore_attributes is not None:
        cls.dynamo_ignore = dynamo_ignore

    if custom_converter is not None:
        cls.custom_converter = dynamo_custom_converter

    # To add non lambda functions, define the function first them assign it to cls.<function_name>

    return cls


def dynamo_entity(
    pk: Any,
    cls=None,
    table_name: str = None,
    sk=None,
    mapping_schema: dict = None,
    ignore_attributes: list = None,
    custom_converter: dict = None,
):
    """
    Wraps a class so it is mappable to DynamoDB. Use it as a decorator.
    The entity class has to allow an empty constructor call.

    Parameters
    ----------
    pk : Any
        The name of the attribute that will be used as the partition key on DynamoDB
    table_name : str, optional
        The DynamoDB table name, if no name is provided, the class name will be used
    sk : Any, optional
        The sort key used with the partition key. Can be None if there is no sort key (default is None)
    mapping_schema: dict, optional
        A dict mapping the class attributes names to the attributes on DynamoDB.
        If no mapping is provided for a particular (or all) class attribute, the class attribute name will be used
        (default is None)
    ignore_attributes: list[str], optional
        A list with the name of the class attributes that should not be saved to/loaded from the database.
        (default is None)
    custom_converter: dict[str, list[function]]
        A dict with a custom conversion functions to encode and decode an attribute before saving
        the keys are the attribute name in the class, the value are lists where list[CrudeRepositoryImp.INSTANCE2ITEM]
        contains the converter from object to dynamodb item and the list[CrudeRepositoryImp.ITEM2INSTANCE]
        contains the converter from dynamodb item to object
    """

    def wrap(cls):
        return _wrap_class(
            pk, cls, table_name, sk, mapping_schema, ignore_attributes, custom_converter
        )

    if cls is None:
        return wrap

    return wrap(cls)


###### ---------- Example ---------- ######


class Counter:
    n_items: int = 0

    def get_current(self):
        return self.n_items

    def get_next(self):
        self.n_items += 1
        return self.n_items


@dataclass
@dynamo_entity(table_name="dTableName", pk="pk", sk="sk")
class SampleEntityClass:
    pk: str = None
    sk: int = None
    attrib1: str = "This is the attribute 1"
    attrib2: int = 2
    field1: float = field(default=0.0)

    def say_my_name(self):
        print(self.dynamo_table_name())

    def am_i_dataclass(self):
        return is_dataclass(self)


if __name__ == "__main__":
    counter = Counter()
    # To use local dynamo call DynamoDBGlobalParameters.get_instance(use_aws_cli_credentials=False)
    sample_crud = DynamoCrudRepository(
        SampleEntityClass, print_debug=True, use_mock_db=True
    )

    aMap = SampleEntityClass.dynamo_map()

    aObj = SampleEntityClass(pk="aPartitionKey", sk=counter.get_next())

    print("Saving object:", aObj, "\n")
    sample_crud.save(aObj)

    anotherObj = sample_crud.find_by_keys(
        {"pk": "aPartitionKey", "sk": counter.get_current()}
    )
    print("Loaded object:", anotherObj, "\n")

    print("Updated attribute")
    aObj.attrib2 = 20
    sample_crud.save(aObj)
    anotherObj = sample_crud.find_by_keys({"pk": "aPartitionKey"})
    print("Loaded object:", anotherObj, "\n")

    sample_crud.remove(aObj)
    print("Object deleted")

    anotherObj = sample_crud.find_by_keys({"pk": "aPartitionKey"})
    print("Loaded object:", anotherObj, "\n")

    n_items = sample_crud.count()
    aList = []
    for _ in range(100):
        aList.append(SampleEntityClass(pk="aPartitionKey", sk=counter.get_next()))
    sample_crud.save_all(aList)
    n_items = sample_crud.count()
    bList = sample_crud.find_all()
    aTruth = sample_crud.exists_by_keys(
        {"pk": "aPartitionKey", "sk": counter.get_current()}
    )
    sample_crud.remove_all_by_keys(
        [{"pk": "aPartitionKey", "sk": counter.get_current()}]
    )
    aLie = sample_crud.exists_by_keys({"pk": "aPartitionKey", "sk": counter.get_next()})
    sample_crud.remove_all()
    print(sample_crud.count())

    # Na classe de teste tipos variados do python , tipos como decimal, float, int, string, bool, map, datetime(string),
    # enum,
    # Implementar as classes de exemplo
    # Auto geração de ID - UUID e de data no meu exemplo incluir usando fields
    # Versionamento (field versionável - status e o timestamp da mudança)
    # Relacionamento entre objetos
    # Exemplo com mais de uma classe
    # Usar um parâmetro para informar o indíce, se não informar, usar a tabela
    # Alguns atributos vão ser mapeados para json outros para lista

    # Primeiro exemplo com company e account

    # One to many relationship - livro

    """
    Retornar todas as contas trazendo tambem algumas informações da empresa
    Filtro: 1) Corporate Name (razão social - empresa)
            2) Business Name (nome fantasia - empresa)
            3) Billing number (conta)

    Output: Corporate name, cnpj(taxpayer), início do contrato e fim do contrato (json), 
            status do contrato (versão atual),


    DynamoStreams

    """
