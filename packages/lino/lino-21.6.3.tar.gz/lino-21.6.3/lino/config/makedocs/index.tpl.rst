{{h1(settings.SITE.title)}}

{{doc2rst(settings.SITE.__doc__)}}

.. toctree::
    :maxdepth: 2
    :hidden:

{% for p in settings.SITE.installed_plugins %}
    {{p.app_label}}
{% endfor  %}
{% for m in get_models() %}
    {{full_model_name(m)}}
{% endfor  %}
{% for a in actors.actors_list %}
    {{a}}
{% endfor  %}


{{header(2, str(_("Plugins")))}}

{% for p in settings.SITE.installed_plugins %}
- :doc:`{{p.app_label}}` (:mod:`{{p.app_name}}`)
  {{makedocs.generate('makedocs/plugin.tpl.rst', p.app_label+'.rst', plugin=p)}}

{% endfor  %}

{{header(2, str(_("Database models")))}}

{% for m in get_models() %}
- :doc:`{{full_model_name(m)}}` :
  {{abstract(m, 2)}}
  {{makedocs.generate('makedocs/model.tpl.rst', full_model_name(m)+'.rst', model=m)}}

{% endfor  %}

{{header(2, str(_("Actors")))}}

{% for a in actors.actors_list %}
- :doc:`{{a}}` :
  {{abstract(a, 2)}}
  {{makedocs.generate('makedocs/actor.tpl.rst', str(a)+'.rst', actor=a)}}

{% endfor  %}
