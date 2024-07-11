from django import template
from django.http import QueryDict
from django.utils.safestring import SafeString

register = template.Library()

@register.filter
def formatear_numero(value):
    value = round(value)
    value = f'{value:,}'
    value = value.replace(',', '.')
    return value

@register.filter
def formatear_dinero(value):
    value = round(value)
    value = f'${value:,}'
    value = value.replace(',', '.')
    return value

@register.filter
def formatear_porcentaje(value):
    return f'{value}%'

@register.filter
def formatear_fecha(value):
    if value == None:
        value = '--/--/----'
    else:
        value = value.strftime("%d/%m/%Y")
    return f'{value}'

@register.filter(is_safe=True)
def add_bootstrap_class(field, exclude_superuser=True):
    widget_type = field.field.widget.__class__.__name__

    if widget_type == 'Select':
        html = field.as_widget(attrs={'class': 'form-select'})
        if exclude_superuser:
            html = html.replace('  <option value="Superusuario">Superusuario</option>\n\n', '')
        html = html.replace('<option value="" selected>', '<option value="">')
        if field.initial:
            html = html.replace(f'<option value="{field.initial}">', f'<option value="{field.initial}" selected>')
    elif widget_type == 'Textarea':
        html = field.as_widget(attrs={'class': 'form-control', 'rows': '5'})
        html = html.replace('>\n<', f'>{field.initial}<' if field.initial else '><')
    elif widget_type == 'CheckboxInput' or widget_type == 'RadioSelect':
        html = field.as_widget(attrs={'class': 'form-check-input'})
        if field.initial:
            html = html.replace('">', '" checked>' if field.initial else '">')
    elif widget_type == 'FileInput':
        html = field.as_widget(attrs={'class': 'form-control', 'value': field.initial if field.initial else ''})
        if field.initial :
            html = field.as_widget(attrs={'class': 'form-control', 'value': field.initial if field.initial else ''})
        else:
            html = field.as_widget(attrs={'class': 'form-control'})
    elif widget_type == 'TextInput' and field.field.widget.input_type == 'submit':
        html = field.as_widget(attrs={'class': 'btn btn-primary', 'value': field.initial if field.initial else ''})
    elif widget_type == 'Button':
        html = field.as_widget(attrs={'class': 'btn btn-primary'})
    else:
        # Sirve para: text, password, email, number, date y cualquier otro que no esté en el listado
        html = field.as_widget(attrs={'class': 'form-control', 'value': field.initial if field.initial else ''})
    return SafeString(html)

HELP_HTML_FORMAT = '''
    <div>
        <small class="form-text text-muted">
            {}
        </small>
    </div>
'''

FIELD_HTML_NORMAL_FORMAT = '''
    <div class="form-group row mb-2">
        <label for="{}" class="col-sm-3 col-form-label">
            {}
        </label>
        <div class="col-sm-9">
            {} {}
        </div>
    </div>
'''

FIELD_HTML_ALIGN_LEFT_FORMAT = '''
    <div class="form-group row mb-2">
        <label for="{}" class="col-sm-3 col-form-label">
            {}
        </label>
        <div class="col-sm-9">
            <div class="row">
                <div class="col">
                    {}
                </div>
                <div class="col-auto">
                    {}
                </div>
            </div>
        </div>
    </div>
'''

FIELD_HTML_ALIGN_RIGHT_FORMAT = '''
    <div class="form-group row mb-2">
        <label for="{}" class="col-sm-3 col-form-label">
            {}
        </label>
        <div class="col-sm-9">
            <div class="row">
                <div class="col-auto">
                    {}
                </div>
                <div class="col">
                    {}
                </div>
            </div>
        </div>
    </div>
'''

@register.filter(is_safe=True)
def as_bootstrap_field(field, args=''):
    
    if field == '':
        return ''

    qs = ''
    help_text = ''
    help_text_align = ''
    help_text_hidden = False

    if args != '':
        qs = QueryDict(args)

    if qs:
        if 'help_text' in qs:
            help_text = qs['help_text']
        if 'help_text_align' in qs:
            help_text_align = qs['help_text_align']
        if 'help_text_hidden' in qs:
            help_text_hidden = qs['help_text_hidden']

    help_html = ''
    field_html = ''
    bootstrap_field = add_bootstrap_class(field)

    if not help_text_hidden:
        if help_text != '':
            help_html = HELP_HTML_FORMAT.format(help_text)
        elif field.help_text != '':
            help_html = HELP_HTML_FORMAT.format(field.help_text)

    if help_text_align == 'left':
        field_html = FIELD_HTML_ALIGN_LEFT_FORMAT.format(field.id_for_label, field.label, help_html, bootstrap_field)
    elif help_text_align == 'right':
        field_html = FIELD_HTML_ALIGN_RIGHT_FORMAT.format(field.id_for_label, field.label, bootstrap_field, help_html)
    else:
        field_html = FIELD_HTML_NORMAL_FORMAT.format(field.id_for_label, field.label, bootstrap_field, help_html)

    return SafeString(field_html)

@register.filter(is_safe=True)
def add_class(field, css_class):
    field.field.widget.attrs['class'] = css_class
    return SafeString(str(field))

@register.filter(is_safe=True)
def as_bootstrap_form(form, args=''):
    form_html = ''
    for field in form:
        form_html += as_bootstrap_field(field, args)
    return SafeString(form_html)
