{{header(1,"``{}`` ({})".format(str(actor), actor.get_actor_label()))}}

{{actor_overview(actor)}}

{{doc2rst(actor.__doc__)}}

{{header(2, str(_("Filter parameters")))}}

{% if actor.params and actor.params_layout %}
{{doctest.fields_help(actor, all=True)}}
{% endif %}
