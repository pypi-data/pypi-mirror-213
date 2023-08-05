# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

"""
    Messenger for client
    ~~~~~~~~~~~~~~~~~~~~

    Transform and send message
"""

from typing import Optional

from dimples import EntityType, ID, EVERYONE
from dimples import Station
from dimples import Envelope, InstantMessage
from dimples import MetaCommand, DocumentCommand

from ..utils import QueryFrequencyChecker
from ..common import HandshakeCommand, ReportCommand, LoginCommand
from ..common import CommonMessenger

from .network import ClientSession

from .group import GroupManager


class ClientMessenger(CommonMessenger):

    @property
    def session(self) -> ClientSession:
        sess = super().session
        assert isinstance(sess, ClientSession), 'session error: %s' % sess
        return sess

    def handshake(self, session_key: Optional[str]):
        """ send handshake command to current station """
        session = self.session
        station = session.station
        srv_id = station.identifier
        if session_key is None:
            # first handshake
            facebook = self.facebook
            user = facebook.current_user
            assert user is not None, 'current user not found'
            env = Envelope.create(sender=user.identifier, receiver=srv_id)
            cmd = HandshakeCommand.start()
            # send first handshake command as broadcast message
            cmd.group = Station.EVERY
            # create instant message with meta & visa
            i_msg = InstantMessage.create(head=env, body=cmd)
            i_msg['meta'] = user.meta.dictionary
            i_msg['visa'] = user.visa.dictionary
            self.send_instant_message(msg=i_msg, priority=-1)
        else:
            # handshake again
            cmd = HandshakeCommand.restart(session=session_key)
            self.send_content(sender=None, receiver=srv_id, content=cmd, priority=-1)

    def handshake_success(self):
        """ callback for handshake success """
        # broadcast current documents after handshake success
        self.broadcast_document()

    def broadcast_login(self, sender: ID, user_agent: str):
        """ send login command to keep roaming """
        # get current station
        station = self.session.station
        assert sender.type != EntityType.STATION, 'station (%s) cannot login: %s' % (sender, station)
        # create login command
        command = LoginCommand(identifier=sender)
        command.agent = user_agent
        command.station = station
        # broadcast to everyone@everywhere
        self.send_content(sender=sender, receiver=EVERYONE, content=command, priority=1)

    def report_online(self, sender: ID = None):
        """ send report command to keep user online """
        command = ReportCommand(title=ReportCommand.ONLINE)
        self.send_content(sender=sender, receiver=Station.ANY, content=command, priority=1)

    def report_offline(self, sender: ID = None):
        """ Send report command to let user offline """
        command = ReportCommand(title=ReportCommand.OFFLINE)
        self.send_content(sender=sender, receiver=Station.ANY, content=command, priority=1)

    def broadcast_document(self, updated: bool = False):
        """ broadcast meta & visa document to all stations """
        facebook = self.facebook
        user = facebook.current_user
        assert user is not None, 'current user not found'
        current = user.identifier
        meta = user.meta
        visa = user.visa
        assert visa is not None, 'visa not found: %s' % user
        command = DocumentCommand.response(identifier=current, meta=meta, document=visa)
        # send to all contacts
        contacts = facebook.contacts(identifier=current)
        for item in contacts:
            self.send_visa(sender=current, receiver=item, content=command, force=updated)
        # broadcast to everyone@everywhere
        self.send_visa(sender=current, receiver=EVERYONE, content=command, force=updated)

    def send_visa(self, sender: Optional[ID], receiver: ID, content: DocumentCommand, force: bool = False):
        checker = QueryFrequencyChecker()
        if checker.document_response_expired(identifier=receiver, force=force):
            self.info(msg='push visa to: %s' % receiver)
            self.send_content(sender=sender, receiver=receiver, content=content, priority=1)
        else:
            # response not expired yet
            self.debug(msg='document response not expired yet: %s' % receiver)

    # Override
    def query_meta(self, identifier: ID) -> bool:
        checker = QueryFrequencyChecker()
        if not checker.meta_query_expired(identifier=identifier):
            # query not expired yet
            self.debug(msg='meta query not expired yet: %s' % identifier)
            return False
        self.info(msg='querying meta: %s from any station' % identifier)
        command = MetaCommand.query(identifier=identifier)
        self.send_content(sender=None, receiver=Station.ANY, content=command, priority=1)
        return True

    # Override
    def query_document(self, identifier: ID) -> bool:
        checker = QueryFrequencyChecker()
        if not checker.document_query_expired(identifier=identifier):
            # query not expired yet
            self.debug(msg='document query not expired yet: %s' % identifier)
            return False
        self.info(msg='querying document: %s from any station' % identifier)
        command = DocumentCommand.query(identifier=identifier)
        self.send_content(sender=None, receiver=Station.ANY, content=command, priority=1)
        return True

    # Override
    def query_members(self, identifier: ID) -> bool:
        checker = QueryFrequencyChecker()
        if not checker.members_query_expired(identifier=identifier):
            # query not expired yet
            self.debug(msg='members query not expired yet: %s' % identifier)
            return False
        self.info(msg='querying members: %s from any station' % identifier)
        man = GroupManager()
        assistants = man.assistants(identifier=identifier)
        if assistants is None or len(assistants) == 0:
            self.error(msg='group assistants not found: %s' % identifier)
            return False
        # querying members from bot
        command = DocumentCommand.query(identifier=identifier)
        for bot in assistants:
            self.send_content(sender=None, receiver=bot, content=command, priority=1)
        return True
