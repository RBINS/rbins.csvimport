#!/usr/bin/env python
# -*- coding: utf-8 -*-

import plone.z3cform.templates
import z3c.form
import zope.schema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile
from plone.autoform.form import AutoExtensibleForm
from plone.namedfile.field import NamedFile
from zope import interface


class ICSVImportSchema(interface.Interface):

    csv_file = NamedFile(
        title=u"CSV File",
        required=True,
    )


class CSVImportForm(AutoExtensibleForm, z3c.form.form.Form):
    """ A form to output a HTML masschange from chosen parameters """
    schema = ICSVImportSchema
    ignoreContext = True
    logs = None

    @z3c.form.button.buttonAndHandler(_(u'Importer'), name='csv_import')
    def csv_import(self, action):
        self.logs = []
        data, errors = self.extractData()
        if errors:
            return

        csv_file = data['csv_file']

        self.logs = ''


csv_import_form_frame = plone.z3cform.layout.wrap_form(
    CSVImportForm,
    index=FiveViewPageTemplateFile("import.pt"))
