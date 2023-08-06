A few months ago, I ran into this post https://blog.anvileight.com/posts/django-email-templates-with-context-stored-in-database/
and decided to make it into a lib after using it on one of my projects

Quick start
-----------

0. Add it to your Environment using::

    pip install django-proemail-template django-summernote


1. Add "django-email-template" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_summernote'#required
        'EmailTemplate',
    ]

2. Run `python manage.py migrate` to create the polls models.

3. add url for summernote::

    path('summernote/', include('django_summernote.urls')),

You should see it under admin

How to use it
-------------
Create a new template on admin called default, setting the required info. Use "object" as the context to access the variables (like on a view).


And send it from any code::

    EmailTemplate.send('default', {
        'object': your_model_instance,
    })
    
