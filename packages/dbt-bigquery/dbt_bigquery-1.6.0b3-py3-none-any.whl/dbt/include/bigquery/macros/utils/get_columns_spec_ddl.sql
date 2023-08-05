{% macro bigquery__format_column(column) -%}
  {% set data_type = column.data_type %}
  {% set formatted = column.column.lower() ~ " " ~ data_type %}
  {{ return({'name': column.name, 'data_type': data_type, 'formatted': formatted}) }}
{%- endmacro -%}
