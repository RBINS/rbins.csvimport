#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import io

import plone.z3cform.templates
import z3c.form
import zope.schema
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile
from plone import api
from plone.autoform.form import AutoExtensibleForm
from plone.namedfile.field import NamedFile
from zope import interface

class ICSVImportSchema(interface.Interface):

    csv_data = zope.schema.Text(
        title=u"Texte CSV",
        required=False,
    )

    csv_file = NamedFile(
        title=u"Fichier CSV",
        required=False,
    )


class CSVImportForm(AutoExtensibleForm, z3c.form.form.Form):
    schema = ICSVImportSchema
    ignoreContext = True
    logs = None
    error_logs = None

    @z3c.form.button.buttonAndHandler(u'Importer', name='csv_import')
    def csv_import(self, action):
        self.logs = ''
        self.error_logs = ''
        data, errors = self.extractData()
        if errors:
            return
        if data['csv_data'] is None and data['csv_file'] is None:
            self.error_logs = 'Le CSV doit être fournis soit en texte soit en fichier.'
            return

        if data['csv_data'] is None:
            csv_data = data['csv_file'].data
        else:
            csv_data = data['csv_data'].encode('utf8')
        dialect = csv.Sniffer().sniff(csv_data[:4096])
        csv_io = io.BytesIO(csv_data)
        reader = csv.DictReader(csv_io, dialect=dialect)

        if '@type' not in reader.fieldnames or '@path' not in reader.fieldnames or 'title' not in reader.fieldnames:
            self.error_logs = 'Les colonnes @type, @path et title sont obligatoires.'
            return

        for index, line in enumerate(reader, start=2):
            self.import_line(index, line)

    def add_error(self, error, index):
        self.error_logs += 'Erreur ligne {}: {}\n'.format(index, error)

    def add_log(self, log, index):
        self.logs += 'ligne {}: {}\n'.format(index, log)

    def import_line(self, index, line):
        try:
            folder = self.get_folder(line.pop('@path'))
            path = '/'.join(folder.getPhysicalPath())
        except Exception as e:
            self.add_error(str(e), index)
            return
        if 'id' in line and line['id'] in folder:
            obj = folder[line['id']]
            if obj.portal_type != line['@type']:
                self.add_error('{}/{} est de type {} alors que @type est {}.'
                               .format(path, obj.id, obj.portal_type, line['@type']), index)
            elif line.get('@update', False) == '1':
                # TODO UPDATE
                self.add_log('{}/{} mis à jour.'.format(path, obj.id), index)
            else:
                self.add_log('{}/{} existe déjà et ne sera pas mis à jour.'.format(path, obj.id), index)
        else:
            obj = api.content.create(
                type=line.pop('@type'),
                container=folder,
                **line
            )
            self.add_log('{}/{} a été créé.'.format(path, obj.id), index)

    def get_folder(self, path):
        current_folder = self.context
        for folder in path.split('/'):
            if not folder:
                continue
            if folder in current_folder:
                current_folder = current_folder['folder']
            else:
                current_folder = api.content.create(
                    type='Folder',
                    title=folder,
                    container=current_folder,
                )
        return current_folder


csv_import_form_frame = plone.z3cform.layout.wrap_form(
    CSVImportForm,
    index=FiveViewPageTemplateFile("import.pt"))
