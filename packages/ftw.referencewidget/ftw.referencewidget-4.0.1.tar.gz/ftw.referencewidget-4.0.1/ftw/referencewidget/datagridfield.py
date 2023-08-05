from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.interfaces import IDataGridFieldWidget
from collective.z3cform.datagridfield.row import DictRow
from ftw.referencewidget.sources import ReferenceObjSourceBinder
from ftw.referencewidget.widget import ReferenceWidgetFactory
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form import converter
from z3c.relationfield import RelationValue
from z3c.relationfield.event import _setRelation
from z3c.relationfield.interfaces import IRelationChoice
from z3c.relationfield.schema import RelationChoice
from zope import component
from zope import schema
from zope.component import adapts
from zope.interface import provider
from zope.intid.interfaces import IIntIds
from zope.schema.interfaces import IList


class IDataGridRow(model.Schema):
    label = schema.TextLine(
        title=u'Label',
        default=u'I am the default label',
    )

    directives.widget(link=ReferenceWidgetFactory)
    link = RelationChoice(
        title=u'Link',
        source=ReferenceObjSourceBinder(),
        required=False,
    )


@provider(IFormFieldProvider)
class IDataGridFieldExample(model.Schema):
    """Demo behavior containing a DataGridField.

    """
    directives.widget('the_data_grid', DataGridFieldFactory, allow_reorder=True)
    the_data_grid = schema.List(
        title=u'The Data Grid',
        value_type=DictRow(title=u'the_data_grid_row', schema=IDataGridRow),
        required=False,
        missing_value=[],
    )


class GridDataConverter(converter.BaseDataConverter):
    """
    The value of a RelationChoice schema field usually is stored as a relation value
    in the database but the data grid stores the item as-is (an object, not a relation).

    So we need to convert the object to a relation value before storing it in the database
    and convert it to an object when rendering the widget.

    Inspired by https://github.com/collective/collective.z3cform.datagridfield/issues/50.
    """
    adapts(IList, IDataGridFieldWidget)

    def toWidgetValue(self, value):
        if not value:
            return value
        new_value = []
        for row in value:
            new_row = {}
            for key in row:
                new_row[key] = row[key]
                if row[key] and IRelationChoice.providedBy(self.field.value_type.schema[key]):
                    if hasattr(row[key], 'to_object'):
                        new_row[key] = row[key].to_object
            new_value.append(new_row)
        return new_value

    def toFieldValue(self, value):
        if not value:
            return value
        intids = component.queryUtility(IIntIds)
        for row in value:
            for key in row:
                if row[key] and IRelationChoice.providedBy(self.field.value_type.schema[key]):
                    to_id = intids.queryId(row[key])
                    if to_id:
                        relation = RelationValue(to_id)
                        _setRelation(row[key], key, relation)
                        row[key] = relation
        return value
