#!/usr/bin/env python3

# Libervia: a SàT frontend
# Copyright (C) 2009-2021 Jérôme Poisson (goffi@goffi.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from libervia.server.constants import Const as C
from sat.tools.common import data_format


class RestrictedBridge:
    """Bridge with limited access, which can be used in browser

    Only a few method are implemented, with potentially dangerous argument controlled.
    Security limit is used
    """

    def __init__(self, host):
        self.host = host
        self.security_limit = C.SECURITY_LIMIT

    async def getContacts(self, profile):
        return await self.host.bridgeCall("getContacts", profile)

    async def identityGet(self, entity, metadata_filter, use_cache, profile):
        return await self.host.bridgeCall(
            "identityGet", entity, metadata_filter, use_cache, profile)

    async def identitiesGet(self, entities, metadata_filter, profile):
        return await self.host.bridgeCall(
            "identitiesGet", entities, metadata_filter, profile)

    async def identitiesBaseGet(self, profile):
        return await self.host.bridgeCall(
            "identitiesBaseGet", profile)

    async def psNodeDelete(self, service_s, node, profile):
        return await self.host.bridgeCall(
            "psNodeDelete", service_s, node, profile)

    async def psNodeAffiliationsSet(self, service_s, node, affiliations, profile):
        return await self.host.bridgeCall(
            "psNodeAffiliationsSet", service_s, node, affiliations, profile)

    async def psItemRetract(self, service_s, node, item_id, notify, profile):
        return await self.host.bridgeCall(
            "psItemRetract", service_s, node, item_id, notify, profile)

    async def mbPreview(self, service_s, node, data, profile):
        return await self.host.bridgeCall(
            "mbPreview", service_s, node, data, profile)

    async def listSet(self, service_s, node, values, schema, item_id, extra, profile):
        return await self.host.bridgeCall(
            "listSet", service_s, node, values, "", item_id, "", profile)


    async def fileHTTPUploadGetSlot(
        self, filename, size, content_type, upload_jid, profile):
        return await self.host.bridgeCall(
            "fileHTTPUploadGetSlot", filename, size, content_type,
            upload_jid, profile)

    async def fileSharingDelete(
        self, service_jid, path, namespace, profile):
        return await self.host.bridgeCall(
            "fileSharingDelete", service_jid, path, namespace, profile)

    async def interestsRegisterFileSharing(
        self, service, repos_type, namespace, path, name, extra_s, profile
    ):
        if extra_s:
            # we only allow "thumb_url" here
            extra = data_format.deserialise(extra_s)
            if "thumb_url" in extra:
                extra_s = data_format.serialise({"thumb_url": extra["thumb_url"]})
            else:
                extra_s = ""

        return await self.host.bridgeCall(
            "interestsRegisterFileSharing", service, repos_type, namespace, path, name,
            extra_s, profile
        )

    async def interestRetract(
        self, service_jid, item_id, profile
    ):
        return await self.host.bridgeCall(
            "interestRetract", service_jid, item_id, profile)

    async def psInvite(
        self, invitee_jid_s, service_s, node, item_id, name, extra_s, profile
    ):
        return await self.host.bridgeCall(
            "psInvite", invitee_jid_s, service_s, node, item_id, name, extra_s, profile
        )

    async def FISInvite(
        self, invitee_jid_s, service_s, repos_type, namespace, path, name, extra_s,
        profile
    ):
        if extra_s:
            # we only allow "thumb_url" here
            extra = data_format.deserialise(extra_s)
            if "thumb_url" in extra:
                extra_s = data_format.serialise({"thumb_url": extra["thumb_url"]})
            else:
                extra_s = ""

        return await self.host.bridgeCall(
            "FISInvite", invitee_jid_s, service_s, repos_type, namespace, path, name,
            extra_s, profile
        )

    async def FISAffiliationsSet(
        self, service_s, namespace, path, affiliations, profile
    ):
        return await self.host.bridgeCall(
            "FISAffiliationsSet", service_s, namespace, path, affiliations, profile
        )

    async def invitationSimpleCreate(
        self, invitee_email, invitee_name, url_template, extra_s, profile
    ):
        return await self.host.bridgeCall(
            "invitationSimpleCreate", invitee_email, invitee_name, url_template, extra_s,
            profile
        )
