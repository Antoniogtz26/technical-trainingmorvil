{
    "name": "Estate",  # The name that will appear in the App list
    "version": "17.0.0.0",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base"],  # dependencies
    "data": [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_menu.xml',
        'views/estate_property_tree.xml',
        'views/estate_property_form.xml',
        'views/estate_property_search.xml',
    ],
    "installable": True,
    'license': 'LGPL-3',
}
