{{header(1, "``{}`` : {}".format(plugin.app_label, plugin.short_name))}}

See also :mod:`{{plugin.app_name}}`.

Models
======

{% for model in get_models() if model.app_label == plugin.app_label %}
- :doc:`{{full_model_name(model)}}` :
  {{abstract(model, 2)}}

{% endfor %}

Actors
======

{% for actor in actors.actors_list if actor.app_label == plugin.app_label %}
- :doc:`{{actor.label}} <{{actor}}>` :
  {{abstract(actor, 2)}}

{% endfor %}
