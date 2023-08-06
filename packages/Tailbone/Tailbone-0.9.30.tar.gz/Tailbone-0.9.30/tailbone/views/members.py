# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Member Views
"""

import sqlalchemy as sa

from rattail.db import model
from rattail.db.model import MembershipType, Member

from deform import widget as dfwidget
from webhelpers2.html import tags

from tailbone import grids
from tailbone.views import MasterView


class MembershipTypeView(MasterView):
    """
    Master view for Membership Types
    """
    model_class = MembershipType
    route_prefix = 'membership_types'
    url_prefix = '/membership-types'
    has_versions = True

    labels = {
        'id': "ID",
    }

    grid_columns = [
        'number',
        'name',
    ]

    has_rows = True
    model_row_class = Member
    rows_title = "Members"

    row_grid_columns = [
        '_member_key_',
        'person',
        'active',
        'equity_current',
        'equity_total',
        'joined',
        'withdrew',
    ]

    def configure_grid(self, g):
        super().configure_grid(g)

        g.set_sort_defaults('number')

        g.set_link('number')
        g.set_link('name')

    def get_row_data(self, memtype):
        model = self.model
        return self.Session.query(model.Member)\
                           .filter(model.Member.membership_type == memtype)

    def get_parent(self, member):
        return member.membership_type

    def configure_row_grid(self, g):
        super().configure_row_grid(g)

        g.filters['active'].default_active = True
        g.filters['active'].default_verb = 'is_true'


class MemberView(MasterView):
    """
    Master view for the Member class.
    """
    model_class = model.Member
    is_contact = True
    touchable = True
    has_versions = True
    configurable = True

    labels = {
        'id': "ID",
        'person': "Account Holder",
    }

    grid_columns = [
        '_member_key_',
        'person',
        'membership_type',
        'active',
        'equity_current',
        'joined',
        'withdrew',
    ]

    form_fields = [
        '_member_key_',
        'person',
        'customer',
        'default_email',
        'default_phone',
        'membership_type',
        'active',
        'equity_current',
        'equity_payment_due',
        'joined',
        'withdrew',
    ]

    def configure_grid(self, g):
        super(MemberView, self).configure_grid(g)
        route_prefix = self.get_route_prefix()
        model = self.model

        # member key
        field = self.get_member_key_field()
        g.filters[field].default_active = True
        g.filters[field].default_verb = 'equal'
        g.set_sort_defaults(field)
        g.set_link(field)

        g.set_joiner('person', lambda q: q.outerjoin(model.Person))
        g.set_sorter('person', model.Person.display_name)
        g.set_filter('person', model.Person.display_name)

        g.set_joiner('customer', lambda q: q.outerjoin(model.Customer))
        g.set_sorter('customer', model.Customer.name)
        g.set_filter('customer', model.Customer.name)

        g.filters['active'].default_active = True
        g.filters['active'].default_verb = 'is_true'

        # phone
        g.set_joiner('phone', lambda q: q.outerjoin(model.MemberPhoneNumber, sa.and_(
            model.MemberPhoneNumber.parent_uuid == model.Member.uuid,
            model.MemberPhoneNumber.preference == 1)))
        g.sorters['phone'] = lambda q, d: q.order_by(getattr(model.MemberPhoneNumber.number, d)())
        g.set_filter('phone', model.MemberPhoneNumber.number,
                     factory=grids.filters.AlchemyPhoneNumberFilter)
        g.set_label('phone', "Phone Number")

        # email
        g.set_joiner('email', lambda q: q.outerjoin(model.MemberEmailAddress, sa.and_(
            model.MemberEmailAddress.parent_uuid == model.Member.uuid,
            model.MemberEmailAddress.preference == 1)))
        g.sorters['email'] = lambda q, d: q.order_by(getattr(model.MemberEmailAddress.address, d)())
        g.set_filter('email', model.MemberEmailAddress.address)
        g.set_label('email', "Email Address")

        # membership_type
        g.set_joiner('membership_type', lambda q: q.outerjoin(model.MembershipType))
        g.set_sorter('membership_type', model.MembershipType.name)
        g.set_filter('membership_type', model.MembershipType.name,
                     label="Membership Type Name")

        if (self.request.has_perm('people.view_profile')
            and self.should_link_straight_to_profile()):

            # add View Raw action
            url = lambda r, i: self.request.route_url(
                f'{route_prefix}.view', **self.get_action_route_kwargs(r))
            # nb. insert to slot 1, just after normal View action
            g.main_actions.insert(1, self.make_action(
                'view_raw', url=url, icon='eye'))

        g.set_link('person')
        g.set_link('customer')

    def default_view_url(self):
        if (self.request.has_perm('people.view_profile')
            and self.should_link_straight_to_profile()):
            app = self.get_rattail_app()

            def url(member, i):
                person = app.get_person(member)
                if person:
                    return self.request.route_url(
                        'people.view_profile', uuid=person.uuid,
                        _anchor='member')
                return self.get_action_url('view', member)

            return url

        return super().default_view_url()

    def should_link_straight_to_profile(self):
        return self.rattail_config.getbool('rattail',
                                           'members.straight_to_profile',
                                           default=False)

    def grid_extra_class(self, member, i):
        if not member.active:
            return 'warning'
        if member.equity_current is False:
            return 'notice'

    def configure_form(self, f):
        super(MemberView, self).configure_form(f)
        member = f.model_instance

        # date fields
        f.set_type('joined', 'date_jquery')
        f.set_type('equity_payment_due', 'date_jquery')
        f.set_type('equity_last_paid', 'date_jquery')
        f.set_type('withdrew', 'date_jquery')

        # person
        if self.creating or self.editing:
            if 'person' in f.fields:
                f.replace('person', 'person_uuid')
                people = self.Session.query(model.Person)\
                                     .order_by(model.Person.display_name)
                values = [(p.uuid, str(p))
                          for p in people]
                require = False
                if not require:
                    values.insert(0, ('', "(none)"))
                f.set_widget('person_uuid', dfwidget.SelectWidget(values=values))
                f.set_label('person_uuid', "Person")
        else:
            f.set_readonly('person')
            f.set_renderer('person', self.render_person)

        # customer
        if self.creating or self.editing:
            if 'customer' in f.fields:
                f.replace('customer', 'customer_uuid')
                customers = self.Session.query(model.Customer)\
                                          .order_by(model.Customer.name)
                values = [(c.uuid, str(c))
                          for c in customers]
                require = False
                if not require:
                    values.insert(0, ('', "(none)"))
                f.set_widget('customer_uuid', dfwidget.SelectWidget(values=values))
                f.set_label('customer_uuid', "Customer")
        else:
            f.set_readonly('customer')
            f.set_renderer('customer', self.render_customer)

        # default_email
        f.set_renderer('default_email', self.render_default_email)
        if not self.creating and member.emails:
            f.set_default('default_email', member.emails[0].address)

        # default_phone
        f.set_renderer('default_phone', self.render_default_phone)
        if not self.creating and member.phones:
            f.set_default('default_phone', member.phones[0].number)

        # membership_type
        f.set_renderer('membership_type', self.render_membership_type)

        if self.creating:
            f.remove_fields(
                'equity_total',
                'equity_last_paid',
                'equity_payment_credit',
                'withdrew',
            )

    def render_default_email(self, member, field):
        if member.emails:
            return member.emails[0].address

    def render_default_phone(self, member, field):
        if member.phones:
            return member.phones[0].number

    def render_membership_type(self, member, field):
        memtype = getattr(member, field)
        if not memtype:
            return
        text = str(memtype)
        url = self.request.route_url('membership_types.view', uuid=memtype.uuid)
        return tags.link_to(text, url)

    def configure_get_simple_settings(self):
        return [

            # General
            {'section': 'rattail',
             'option': 'members.key_field'},
            {'section': 'rattail',
             'option': 'members.key_label'},
            {'section': 'rattail',
             'option': 'members.straight_to_profile',
             'type': bool},
        ]


def defaults(config, **kwargs):
    base = globals()

    MembershipTypeView = kwargs.get('MembershipTypeView', base['MembershipTypeView'])
    MembershipTypeView.defaults(config)

    MemberView = kwargs.get('MemberView', base['MemberView'])
    MemberView.defaults(config)


def includeme(config):
    defaults(config)
