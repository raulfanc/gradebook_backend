```bash
pip install django-extensions
```

```bash
pip install django-model-utils
```


```python
# settings.py

INSTALLED_APPS = [
    ...
    'django_extensions',
    ...
]

```

```python
# models.py

from django_extensions.db.models import TimeStampedModel
from model_utils import FieldTracker
from django.db.models.signals import post_save

class your_model(TimeStampedModel):
    # TimeStampedModel is the subclass of models.Model, so no need to inherit two models
    ...
    # rest of the code
    tracker = FieldTracker()

```


