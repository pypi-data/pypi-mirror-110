{% materialization table, adapter='rockset' -%}
  {%- set identifier = model['alias'] -%}
  {%- set old_relation = adapter.get_relation(database=database, schema=schema, identifier=identifier) -%}
  {%- set already_exists = (old_relation is not none) -%}
  {%- set target_relation = api.Relation.create(database=database, schema=schema, identifier=identifier, type='table') -%}
  
  {{ run_hooks(pre_hooks) }}

  {%- if already_exists -%}
      {{ adapter.drop_relation(old_relation) }}
  {%- endif -%}

  {{ log('Calling create table for materialization type table') }}
  {{ adapter.create_table(target_relation, sql) }}

  {#-- Rockset does not support CREATE TABLE sql. All logic to create collections happens in create_table_as --#}
  {% call statement('main') -%}
    {{ "SELECT 1" }}
  {%- endcall %}

  {{ run_hooks(post_hooks) }}

  {% do persist_docs(target_relation, model) %}

  {{ return({'relations': [target_relation]}) }}

{% endmaterialization %}