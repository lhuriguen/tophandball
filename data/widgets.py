from django.forms.widgets import (
    FileInput, CheckboxInput, FILE_INPUT_CONTRADICTION)
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape


class SingleImageInput(FileInput):
    clear_checkbox_label = 'Remove existing'

    template_with_clear = ('<br />%(clear)s '
                           '<label for="%(clear_checkbox_id)s">'
                           '%(clear_checkbox_label)s</label>')

    url_template = '<img src="{0}" class="file-preview-image">'

    def __init__(self, attrs=None, max_size=None):
        super(SingleImageInput, self).__init__(attrs)
        self.max_size = max_size if max_size else None

    def clear_checkbox_name(self, name):
        """
        Given the name of the file input,
        return the name of the clear checkbox
        input.
        """
        return name + '-clear'

    def clear_checkbox_id(self, name):
        """
        Given the name of the clear checkbox input,
        return the HTML id for it.
        """
        return name + '_id'

    def render(self, name, value, attrs=None):
        attrs['class'] = 'file'
        attrs['accept'] = 'image/*'
        attrs['data-show-caption'] = 'false'
        attrs['data-show-upload'] = 'false'
        attrs['data-show-remove'] = 'false'
        attrs['data-max-file-size'] = self.max_size
        attrs['data-browse-label'] = 'Browse'
        attrs['data-browse-icon'] = '<i class="fa fa-image"></i> &nbsp;'
        attrs['data-browse-class'] = 'btn btn-default'

        if value and hasattr(value, "url"):
            attrs['data-initial-preview'] = self.url_template.format(value.url)

        template = '%(input)s%(clear_template)s'
        subs = {
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        subs['input'] = super(SingleImageInput, self).render(
            name, value, attrs)

        if value and hasattr(value, "url") and not self.is_required:
            checkbox_name = self.clear_checkbox_name(name)
            checkbox_id = self.clear_checkbox_id(checkbox_name)
            subs['clear_checkbox_name'] = conditional_escape(checkbox_name)
            subs['clear_checkbox_id'] = conditional_escape(checkbox_id)
            subs['clear'] = CheckboxInput().render(
                checkbox_name, False, attrs={'id': checkbox_id})
            subs['clear_template'] = self.template_with_clear % subs

        return mark_safe(template % subs)

    def value_from_datadict(self, data, files, name):
        upload = super(SingleImageInput, self).value_from_datadict(
            data, files, name)
        if not self.is_required and CheckboxInput().value_from_datadict(
                data, files, self.clear_checkbox_name(name)):
            if upload:
                # If the user contradicts themselves (uploads a new file AND
                # checks the "clear" checkbox), we return a unique marker
                # object that FileField will turn into a ValidationError.
                return FILE_INPUT_CONTRADICTION
            # False signals to clear any existing value,
            # as opposed to just None.
            return False
        return upload
