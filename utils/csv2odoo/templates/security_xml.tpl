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
    <record id="group_{{ group.short_name }}" model="res.groups">
        <field name="name">{{ group.short_name }}</field>
        <field name="category_id" ref="{{ module.name }}.category_{{ module.name }}"/>
        <!-- <field name="implied_ids"
            eval="[
                (4, ref('base.group_no_one')),
                (4, ref('base.group_user'))
            ]"
        />-->
    </record>
{%- endfor %}
</data>
</openerp>