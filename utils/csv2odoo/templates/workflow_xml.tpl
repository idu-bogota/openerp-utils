<?xml version="1.0" encoding="utf-8"?>
<openerp>
<data>
    <record id="{{ model.short_name | replace('.', '_') }}_workflow" model="workflow">
        <field name="name">{{ model.name }}.workflow</field>
        <field name="osv">{{ model.name }}</field>
        <field name="on_create">True</field>
    </record>
<!--
    ===================================================================================
    Activities
    ===================================================================================
-->
{% for act in model.activities %}
    <record id="{{ model.short_name | replace('.', '_') }}_{{ act.name }}_act" model="workflow.activity">
        <field name="wkf_id" ref="{{ model.short_name | replace('.', '_') }}_workflow"/>
        <field name="name">{{ act.name }}</field>
        <field name="kind">function</field>
        <field name="action">wkf_{{ act.name }}()</field>
        {%- if act.type == 'start' %}
        <field name="flow_start" eval="True"/>
        {%- elif act.type == 'stop' %}
        <field name="flow_stop" eval="True"/>
        {%- endif %}
    </record>
{% endfor %}
    <!--
    ===================================================================================
    Transitions
    ===================================================================================
     -->
{% for tr in model.transitions %}
    <record id="{{ model.short_name | replace('.', '_') }}_{{ tr.act_from.name }}__{{ tr.act_to.name }}_transition" model="workflow.transition">
        <field name="act_from" ref="{{ model.short_name | replace('.', '_') }}_{{ tr.act_from.name }}_act"/>
        <field name="act_to" ref="{{ model.short_name | replace('.', '_') }}_{{ tr.act_to.name }}_act"/>
        <field name="condition">{{ tr.condition }}</field>{% if tr.group_name %}
        <field name="group_id" ref="{{ tr.group_name }}"/>{% endif %}{% if tr.button_label %}
        <field name="signal">{{ tr.signal }}</field>
        {%- endif -%}
    </record>
{% endfor %}
</data>
</openerp>