<?xml version="1.0" encoding="utf-8"?>
<openerp>
<data>
<!-- 
=========================================================================
 Groups Definition
=========================================================================
-->
    <record model="ir.module.category" id="category_{{ module.name }}">
        <field name="name">{{ module.string }}</field>
        <field name="sequence">0</field>
        <field name="visible" eval="1" />
    </record>
{%- for group in module.groups if group.namespace == module.name %}
    <record id="group_{{ group.short_name | replace('.', '_') }}" model="res.groups">
        <field name="name">{{ group.short_name | replace('.', '_') }}</field>
        <field name="category_id" ref="{{ module.name }}.category_{{ module.name }}"/>
        <!-- <field name="implied_ids"
            eval="[
                (4, ref('base.group_no_one')),
                (4, ref('base.group_user'))
            ]"
        />-->
    </record>
{%- endfor %}
<!--
=============================================================================
 Domain Constraints
=============================================================================
-->
{%- for group in module.groups %}
    <!-- Domain {{ group.name }} -->
    {%- for model_name, acl in group.acls.iteritems() -%}
    {%- if acl.read['param'] %}
    <record id="{{ acl.model.short_name | replace('.', '_') }}_{{ acl.group.name | replace('.', '_') }}_domain_read" model="ir.rule">
        <field name="name">{{ group.name }} {{ model_name }} Read</field>
        <field name="model_id" ref="{{ acl.model.namespace }}.model_{{ acl.model.name | replace('.', '_')}}"/>
        <field name="domain_force">{{ acl.domain_force('read') }}</field>
        <field name="groups" eval="[(4, ref('{{ acl.group_name() }}'))]"/>
        <field name="perm_read" eval="True"/>
        <field name="perm_create" eval="False"/>
        <field name="perm_write" eval="False"/>
        <field name="perm_unlink" eval="False"/>
    </record>
    {%- endif %}
    {%- if acl.create['param'] %}
    <record id="{{ acl.model.short_name | replace('.', '_') }}_{{ acl.group.name | replace('.', '_') }}_domain_create" model="ir.rule">
        <field name="name">{{ group.name }} {{ model_name }} Create</field>
        <field name="model_id" ref="{{ acl.model.namespace }}.model_{{ acl.model.name | replace('.', '_')}}"/>
        <field name="domain_force">{{ acl.domain_force('create') }}</field>
        <field name="groups" eval="[(4, ref('{{ acl.group_name() }}'))]"/>
        <field name="perm_read" eval="False"/>
        <field name="perm_create" eval="True"/>
        <field name="perm_write" eval="False"/>
        <field name="perm_unlink" eval="False"/>
    </record>
    {%- endif %}
    {%- if acl.write['param'] %}
    <record id="{{ acl.model.short_name | replace('.', '_') }}_{{ acl.group.name | replace('.', '_') }}_domain_write" model="ir.rule">
        <field name="name">{{ group.name }} {{ model_name }} Write</field>
        <field name="model_id" ref="{{ acl.model.namespace }}.model_{{ acl.model.name | replace('.', '_')}}"/>
        <field name="domain_force">{{ acl.domain_force('write') }}</field>
        <field name="groups" eval="[(4, ref('{{ acl.group_name() }}'))]"/>
        <field name="perm_read" eval="False"/>
        <field name="perm_create" eval="False"/>
        <field name="perm_write" eval="True"/>
        <field name="perm_unlink" eval="False"/>
    </record>
    {%- endif %}
    {%- if acl.delete['param'] %}
    <record id="{{ acl.model.short_name | replace('.', '_') }}_{{ acl.group.name | replace('.', '_') }}_domain_delete" model="ir.rule">
        <field name="name">{{ group.name }} {{ model_name }} Delete</field>
        <field name="model_id" ref="{{ acl.model.namespace }}.model_{{ acl.model.name | replace('.', '_')}}"/>
        <field name="domain_force">{{ acl.domain_force('delete') }}</field>
        <field name="groups" eval="[(4, ref('{{ acl.group_name() }}'))]"/>
        <field name="perm_read" eval="False"/>
        <field name="perm_create" eval="False"/>
        <field name="perm_write" eval="False"/>
        <field name="perm_unlink" eval="True"/>
    </record>
    {%- endif -%}
    {%- endfor %}
{%- endfor %}
</data>
</openerp>