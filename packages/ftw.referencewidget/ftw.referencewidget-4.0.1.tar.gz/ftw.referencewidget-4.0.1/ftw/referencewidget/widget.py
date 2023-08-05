# from collective.z3cform.datagridfield.datagridfield import DataGridFieldObjectSubForm
from Acquisition import aq_parent
from ftw.referencewidget import _
from ftw.referencewidget.browser.utils import get_path_from_widget_start
from ftw.referencewidget.browser.utils import get_selectable_types
from ftw.referencewidget.browser.utils import get_traversal_types
from ftw.referencewidget.browser.utils import is_traversable
from ftw.referencewidget.interfaces import IReferenceWidget
from ftw.referencewidget.sources import ReferenceObjSourceBinder
from plone import api
from plone.app.redirector.interfaces import IRedirectionStorage
from Products.CMFCore.Expression import createExprContext
from Products.CMFPlone.resources.webresource import PloneScriptResource
from Products.CMFPlone.utils import safe_unicode
from z3c.form.browser import widget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.widget import FieldWidget
from z3c.form.widget import Widget
from z3c.relationfield.schema import RelationChoice
from zope.component import adapter
from zope.component import queryUtility
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import implementer_only
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import IList
import json


@implementer_only(IReferenceWidget)
class ReferenceBrowserWidget(widget.HTMLTextInputWidget, Widget):
    """ Datepicker widget. """

    klass = u'reference-widget'
    request = None
    block_traversal = None
    allow_traversal = None
    selectable = None
    nonselectable = None
    start = None
    override = None

    traversal_query = None

    def __init__(self,
                 request,
                 block_traversal=[],
                 allow_traversal=[],
                 selectable=[],
                 nonselectable=[],
                 start='',
                 override=False,
                 allow_nonsearched_types=False,
                 traversal_query={}):
        self.request = request
        self.block_traversal = block_traversal
        self.allow_traversal = allow_traversal
        self.selectable = selectable
        self.nonselectable = nonselectable
        self.start = start
        self.override = override
        self.allow_nonsearched_types = allow_nonsearched_types
        self.traversal_query = traversal_query

    def update(self):
        super(ReferenceBrowserWidget, self).update()
        # if isinstance(self.form, DataGridFieldObjectSubForm):
        #     self.context = self.form.__parent__.__parent__.context

        # Make supermodel with keywordwidget (single select) work
        if isinstance(self.field, RelationChoice):
            if not IContextSourceBinder.providedBy(self.field.vocabulary):
                self.field.vocabulary = ReferenceObjSourceBinder()

        widget.addFieldClass(self)

    def input_type(self):
        if IList.providedBy(self.field):
            return 'checkbox'
        else:
            return 'radio'

    def _translate(self, msg):
        return translate(msg, context=self.request)

    def translations(self):
        messages = {
            'Choose content': self._translate(_(u"label_choose_content", default="Choose content")),
            'Search': self._translate(_(u"button_seach", default="Search")),
            'Sort on': self._translate(_(u"label_sort_by", default="Sort by")),
            'Sort order': self._translate(_(u"label_sort_order", default="Sort order")),
            'Position': self._translate(_(u"label_sort_by_pos", default="Position")),
            'Title': self._translate(_(u"label_sort_by_title", default="Title")),
            'Created': self._translate(_(u"label_sort_by_created", default="Created")),
            'Modified': self._translate(_(u"label_sort_by_modified", default="Modified")),
            'Ascending': self._translate(_(u"label_sort_ascending", default="Ascending")),
            'Descending': self._translate(_(u"label_sort_descending", default="Descending")),
            'Reset': self._translate(_(u"label_reset", default="Reset")),
            'Startpage': self._translate(_(u"label_startpage", default="Startpage")),
            'Previous': self._translate(_(u"label_previous", default="Previous")),
            'Next': self._translate(_(u"label_next", default="Next")),
            'Search text': self._translate(_(u"label_searchtext", default="Search text")),
            'Close': self._translate(_(u"label_close", default="Close")),
            'Browse': self._translate(_(u"label_browse", default="Browse")),
            'Total': self._translate(_(u"label_total", default="Total")),
            'Page': self._translate(_(u"label_page", default="Page")),
            'of': self._translate(_(u"label_of", default="of")),
        }
        return json.dumps(messages)

    def get_object_by_path(self, path):
        storage = queryUtility(IRedirectionStorage)

        if isinstance(path, bytes):
            path = path.decode('utf8')

        obj = self.context.unrestrictedTraverse(path, None)
        if obj is None:
            path = storage.get(path)
            obj = self.context.unrestrictedTraverse(path, None)

        return obj

    def get_items(self):
        result = []

        if not self.value:
            return

        def obj_to_dict(obj):
            return {'path': '/'.join(obj.getPhysicalPath()),
                    'title': safe_unicode(obj.Title())}

        if isinstance(self.value, list):
            for item in self.value:
                if not item:
                    continue

                obj = self.get_object_by_path(item)
                if obj:
                    result.append(obj_to_dict(obj))

        else:
            obj = self.get_object_by_path(self.value)
            if obj:
                result.append(obj_to_dict(obj))

        return result

    def get_start_path(self):
        if self.start:
            effective_path = get_path_from_widget_start(self)
        else:
            obj = self.context
            while api.portal.get() != obj and not is_traversable(self, obj):
                obj = aq_parent(obj)
            effective_path = '/'.join(obj.getPhysicalPath())
        return effective_path

    def get_start_url(self):
        path = self.get_start_path()
        return api.portal.get().unrestrictedTraverse(path).absolute_url()

    def portal_path(self):
        return '/'.join(api.portal.get().getPhysicalPath())

    def selectable_types(self):
        return json.dumps(get_selectable_types(self))

    def traversable_types(self):
        return json.dumps(get_traversal_types(self))

    def icon_mapping(self):
        portal = api.portal.get()
        expr_context = createExprContext(
            portal, portal, portal
        )
        mapping = {}
        for fti in api.portal.get_tool('portal_types').objectValues():
            icon = fti.getIconExprObject()
            if icon:
                icon = icon(expr_context)
            mapping[fti.getId()] = icon
        return json.dumps(mapping)

    def script_resource_url(self):
        resource = PloneScriptResource(
            context=self.context,
            name="reference-browser-widget",
            depends="",
            resource='/++resource++ftw.referencewidget/dist/referencewidget.es.js',
            include=True,
            unique=True,
            integrity=True,
        )
        return resource.resource_url(api.portal.get().absolute_url())


@adapter(IReferenceWidget, IFormLayer)
@implementer(IFieldWidget)
def ReferenceWidgetFactory(field,
                           request,
                           block_traversal=[],
                           allow_traversal=[],
                           selectable=[],
                           nonselectable=[],
                           start='',
                           override=False,
                           allow_nonsearched_types=False,
                           traversal_query={}):
    """IFieldWidget factory for DateTimePickerWidget."""
    return FieldWidget(field, ReferenceBrowserWidget(request,
                                                     block_traversal,
                                                     allow_traversal,
                                                     selectable,
                                                     nonselectable,
                                                     start,
                                                     override,
                                                     allow_nonsearched_types,
                                                     traversal_query))
