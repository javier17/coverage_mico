import hashlib
from enum import Enum
from http import HTTPStatus
from sqlalchemy import and_
import bcrypt
from sqlalchemy import or_
from sqlalchemy.orm import (ColumnProperty, InstrumentedAttribute,
                            RelationshipProperty)
from sqlalchemy.orm.attributes import InstrumentedAttribute
from micro_companies.src.models.models import db


class DbService:

    def db_generic_create(data, model_class):
        new_instance = model_class()
        DbTools.assign_related_fields(data, model_class, new_instance)
        db.session.add(new_instance)
        db.session.commit()

        selected_fields = DbTools.get_selected_fields(model_class, {})
        selected_relationships = selected_fields["relationships_fields"]["fields"]
        selected_columns_name = selected_fields["column_fields"]["names"]

        cleaned_instance = DbTools.remove_relationship_overload(
            new_instance, selected_columns_name, selected_relationships)

        return ResponseTools.build_response(message=f'{model_class.__name__} created successfully', code=201, response=cleaned_instance)

    def db_generic_update(model_id, data, model_class):

        model_instance = model_class.query.get_or_404(model_id)
        DbTools.assign_related_fields(data, model_class, model_instance)
        db.session.commit()

        selected_fields = DbTools.get_selected_fields(model_class, {})
        selected_relationships = selected_fields["relationships_fields"]["fields"]
        selected_columns_name = selected_fields["column_fields"]["names"]

        cleaned_instance = DbTools.remove_relationship_overload(
            model_instance, selected_columns_name, selected_relationships)

        return ResponseTools.build_response(message=f'{model_class.__name__} updated successfully', response=cleaned_instance)

    def db_generic_delete(model_id, model_class):
        model_instance = model_class.query.get_or_404(model_id)

        db.session.delete(model_instance)
        db.session.commit()

        return ResponseTools.build_response(message=f'{model_class.__name__} deleted successfully', code=204)

    def db_generic_get_by_id(model_id, model_class, json_data=None):
        query = model_class.query

        selected_fields = DbTools.get_selected_fields(model_class, json_data)
        selected_columns = selected_fields["column_fields"]["fields"]
        selected_relationships = selected_fields["relationships_fields"]["fields"]
        selected_columns_name = selected_fields["column_fields"]["names"]

        query.with_entities(*selected_columns)
        entity = query.get_or_404(model_id)

        if not entity:
            return ResponseTools.build_response(message=f"{model_class.__name__} dosn't exist", code=400)

        cleaned_instance = DbTools.remove_relationship_overload(
            entity, selected_columns_name, selected_relationships)

        return ResponseTools.build_response(message=f'{model_class.__name__} deleted successfully', response=cleaned_instance)

    def db_generic_get(model_class, json_data=None):
        query = model_class.query

        # Filtering
        if json_data and '_filters' in json_data:
            query = DbTools.apply_filters(
                query, model_class, json_data['_filters'])
        # Ordering
        if json_data and '_order_by' in json_data:

            order_by = []
            for ob in json_data['_order_by']:
                field = ob['field']
                direction = ob['direction']

                if '.' in field:
                    # Handle ordering by a related entity's property
                    related_entity, related_property = field.split('.')
                    join_alias = getattr(
                        model_class, related_entity).property.mapper.class_
                    join_clause = getattr(join_alias, related_property)
                    if direction == 'asc':
                        order_by.append(join_clause.asc())
                    else:
                        order_by.append(join_clause.desc())
                    query = query.join(join_alias)

                else:
                    # Order by a property of the main entity
                    attr = getattr(model_class, field)
                    if direction == 'asc':
                        order_by.append(attr.asc())
                    else:
                        order_by.append(attr.desc())
            query = query.order_by(*order_by)

        total_count = query.count()

        selected_fields = DbTools.get_selected_fields(model_class, json_data)
        selected_columns = selected_fields["column_fields"]["fields"]
        selected_relationships = selected_fields["relationships_fields"]["fields"]
        selected_columns_name = selected_fields["column_fields"]["names"]
        # Cargar las entidades seleccionadas
        query.with_entities(*selected_columns)

        # Pagination
        page = json_data['_page'] if json_data and '_page' in json_data else 1
        per_page = json_data['_per_page'] if json_data and '_per_page' in json_data else 10
        query = query.paginate(page=page, per_page=per_page)
        # Build response
        pagination_data = {
            "total_count": total_count,
            "per_page": per_page,
            "page": page
        }
        # Eliminar sobrecarga de entidades relacionadas
        filtered_results = []
        for item in query.items:
            filtered_results.append(DbTools.remove_relationship_overload(
                item, selected_columns_name, selected_relationships))

        response = ResponseTools.build_response(
            code=200, message="Data retrieved successfully", response=filtered_results)
        response['pagination'] = pagination_data

        return response


class DbTools:
    def apply_filters(query, model_class, filters):
        filter_clauses = []

        for field, filter_value in filters.items():
            # Separate the field name and operator (if provided)
            parts = field.split("__")
            field_name = parts[0]
            operator = parts[1] if len(parts) > 1 else "eq"  # Default to "eq"

            if "." in field_name:
                # Handle filters on related entities (entity.attribute)
                entity_name, attr_name = field_name.split(".")
                entity_class = getattr(
                    model_class, entity_name).property.mapper.class_

                if operator == "eq":
                    if isinstance(filter_value, list):
                        filter_clause = getattr(
                            entity_class, attr_name).in_(filter_value)
                    else:
                        filter_clause = getattr(
                            entity_class, attr_name) == filter_value
                elif operator == "lt":
                    filter_clause = getattr(
                        entity_class, attr_name) < filter_value
                elif operator == "gt":
                    filter_clause = getattr(
                        entity_class, attr_name) > filter_value
                elif operator == "lte":
                    filter_clause = getattr(
                        entity_class, attr_name) <= filter_value
                elif operator == "gte":
                    filter_clause = getattr(
                        entity_class, attr_name) >= filter_value
                elif operator == "ilike":
                    filter_clause = getattr(
                        entity_class, attr_name).ilike(f"%{filter_value}%")

                else:
                    raise ValueError(f"Invalid operator: {operator}")

                filter_clauses.append(filter_clause)
            else:
                parts = field.split("__")
                field_name = parts[0]
                operator = parts[1] if len(parts) > 1 else "eq"  # Default to "eq"
                if hasattr(model_class, field_name):
                    if operator == "eq":
                        if isinstance(filter_value, list):
                            filter_clause = getattr(
                                model_class, field_name).in_(filter_value)
                        else:
                            filter_clause = getattr(
                                model_class, field_name) == filter_value
                    elif operator == "lt":
                        filter_clause = getattr(
                            model_class, field_name) < filter_value
                    elif operator == "gt":
                        filter_clause = getattr(
                            model_class, field_name) > filter_value
                    elif operator == "lte":
                        filter_clause = getattr(
                            model_class, field_name) <= filter_value
                    elif operator == "gte":
                        filter_clause = getattr(
                            model_class, field_name) >= filter_value
                    elif operator == "ilike":
                        filter_clause = getattr(
                            model_class, field_name).ilike(f"%{filter_value}%")

                    else:
                        raise ValueError(f"Invalid operator: {operator}")

                    filter_clauses.append(filter_clause)

        if filter_clauses:
            query = query.filter(and_(*filter_clauses))

        return query

    def get_selected_fields(model_class, json_data):
        # Obtiene los campos  relacionales
        relationship_fields = DbTools.get_relationship_fields(model_class)[0]
        # Obtiene columnas del model_class
        columns_fields = DbTools.get_relationship_fields(model_class)[1]

        if json_data:
            select_fields_names = json_data.get(
                "_select_fields", [attr.key for attr in columns_fields])
        else:
            select_fields_names = [attr.key for attr in columns_fields]

        selected_relationships_names = [
            attr.key for attr in relationship_fields]
        selected_entities = []
        selected_relationships = []

        for field in select_fields_names:

            if field in selected_relationships_names:
                selected_relationships.append(getattr(model_class, field))
            else:
                selected_entities.append(getattr(model_class, field))

        return {
            "column_fields": {
                "fields": selected_entities,
                "names": select_fields_names
            },
            "relationships_fields": {
                "fields": selected_relationships,
                "names": selected_relationships_names
            }
        }

    def remove_relationship_overload(result, select_fields, selected_relationships):

        filtered_result = {column: getattr(
            result, column) for column in select_fields}
        for relationship_field in selected_relationships:
            relationship_data = getattr(result, relationship_field.key)
            if isinstance(relationship_data, list):
                filtered_result[relationship_field.key] = [
                    {column: getattr(
                        item, column) for column in relationship_field.property.mapper.class_.__table__.columns.keys()}
                    for item in relationship_data
                ]
            else:
                filtered_result[relationship_field.key] = {
                    column: getattr(relationship_data, column) for column in relationship_field.property.mapper.class_.__table__.columns.keys()
                }
        return filtered_result

    def validate_fields_in_model(fields, model_class):
        for field in fields:
            if field not in model_class.__table__.columns:
                raise ValueError(
                    f"Field '{field}' does not exist in '{model_class.__name__}'")

    def get_relationship_fields(model_class):
        relationship_fields = []
        column_fields = []
        for field in model_class.__dict__.values():
            if isinstance(field, InstrumentedAttribute) and isinstance(field.property, RelationshipProperty):
                relationship_fields.append(field)
            elif isinstance(field, InstrumentedAttribute) and isinstance(field.property, ColumnProperty):
                column_fields.append(field)
        return relationship_fields, column_fields

    def assign_related_fields(data, model_class, model_instance):
        for field, value in data.items():
            if not hasattr(model_class, field) or getattr(getattr(model_class, field), 'primary_key', False):
                continue

            new_value = value
            attr = getattr(model_class, field)
            if isinstance(attr.property, RelationshipProperty):
                related_instances = attr.property.mapper.class_.query.filter(
                    attr.property.mapper.class_.id.in_(value)).all()

                if len(related_instances) != len(value):
                    valid_ids = [instance.id for instance in related_instances]
                    invalid_ids = [id for id in value if id not in valid_ids]
                    message = f'The following related IDs are invalid in {field} field : ' + ','.join(
                        map(str, invalid_ids))
                    raise ValueError(ResponseTools.build_response(
                        message=message, code=400))

                new_value = related_instances

            setattr(model_instance, field, new_value)

    def model_instance_to_dict(instance, mapped_instances=None):
        if mapped_instances is None:
            mapped_instances = set()

        if instance in mapped_instances:
            return None

        mapped_instances.add(instance)

        result = {}

        # Mapear las columnas directas
        for attr in instance.__class__.__table__.columns.keys():
            result[attr] = getattr(instance, attr)

        # Mapear las relaciones
        for attr, prop in instance.__mapper__.relationships.items():
            if prop.uselist:
                result[attr] = [DbTools.model_instance_to_dict(
                    obj, mapped_instances) for obj in getattr(instance, attr)]
            else:
                result[attr] = DbTools.model_instance_to_dict(
                    getattr(instance, attr), mapped_instances)

        return result

    def hash_password(password):
        sal = bcrypt.gensalt().decode()
        salted_password = password + sal
        passw = hashlib.sha256(salted_password.encode()).hexdigest()
        return {'password': passw, 'salt': sal}
    
    def verify_password(input_password, stored_password_hash, salt):
        salted_password = input_password + salt
        input_password_hash = hashlib.sha256(salted_password.encode()).hexdigest()
        return input_password_hash == stored_password_hash
    
    def apply_joins(query, joins, model_class):
        for join_info in joins:
            join_type = join_info['type']
            table_name = join_info['table']
            onclause = join_info['onclause']

            # Validate onclause field
            DbTools.validate_fields_in_model([onclause], model_class)

            if 'joins' in join_info:
                secondary_joins = join_info['joins']
                DbTools.validate_fields_in_model(
                    [table_name], model_class)  # Validate join table
                query = DbTools.apply_joins(
                    query, secondary_joins, model_class)

            if join_type == 'inner':
                query = query.join(table_name, onclause=onclause)
            elif join_type == 'left':
                query = query.outerjoin(table_name, onclause=onclause)
            elif join_type == 'right':
                query = query.outerjoin(
                    table_name, onclause=onclause, isouter=True)
            elif join_type == 'full':
                query = query.outerjoin(
                    table_name, onclause=onclause, full=True)

        return query

    def get_model_class(table_name):
        for cls in db.Model._sa_registry._class_registry.values():
            if hasattr(cls, '__tablename__') and cls.__tablename__ == table_name:
                return cls
        return None


class ResponseTools:
    def map_response_code_to_type(response_code):
        response_ranges = {
            range(100, 400): ResponseType.SUCCESS,
            range(400, 600): ResponseType.ERROR,
        }

        for code_range, response_type in response_ranges.items():
            if response_code in code_range:
                return response_type

        return None

    def build_response(code=200, message=None, response=None, error_message=None):
        response_type = ResponseTools.map_response_code_to_type(code)

        if response_type is None:
            raise ValueError("Invalid response code")

        result = {
            "status": {
                "type": response_type.value,
                "code": code,
                "message": message or HTTPStatus(code).description,
                "errorMessage": error_message
            },
            "response": response
        }

        return result


class ResponseType(Enum):
    SUCCESS = "success"
    ERROR = "error"





""" 
json_data = {
    "_filters": [
        {"field": "username", "operator": "eq",
            "value": "john_doe", "logic": "AND"},
        {"field": "email", "operator": "contains",
            "value": "example.com", "logic": "OR"}
    ],
    "_joins": [
        {"type": "inner", "table": "rol", "onclause": "user.rol_id = rol.id"}
    ],
    "_order_by": [
        {"field": "createdAt", "direction": "desc"},
        {"field": "username", "direction": "asc"}
    ],
    "_page": 1,
    "_per_page": 10,
    "_select_fields": ["id", "username", "email"]
}
 """
